# Batch Image-to-Image Pipeline

Sends each reference photo in `input/` to an image-capable Gemini model on
Google AI Studio with a fixed editorial prompt, and writes a 9:16 JPEG to
`output/gen_<original_stem>.jpg`.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env      # then paste your key from https://aistudio.google.com/apikey
```

Drop the reference photos (`.jpg`, `.jpeg`, `.png`, `.webp`) into `input/`.

## Run

```bash
python run_batch.py --dry-run       # list the work, no API calls
python run_batch.py --limit 1       # single-image test run
python run_batch.py                 # full batch
```

Useful flags: `--model`, `--delay` (default 2.5s between calls), `--attempts`
(default 3 on transient errors), `--force` (regenerate existing outputs),
`--verbose`.

Exit codes: `0` all good, `1` nothing to do, `2` finished with per-file
failures (see `failures.csv`), `3` aborted on a fatal condition (bad key or
model), `130` interrupted.

## Behaviour

- **Resumable.** Existing `output/gen_*.jpg` files are skipped. Output is
  written to a `.part` file and renamed, so an interrupted run never leaves a
  truncated JPEG that looks finished.
- **Rate limited.** 2.5s between calls, plus exponential backoff with jitter on
  429/5xx.
- **Isolated failures.** A safety block or API error is logged to
  `run_batch.log` and appended to `failures.csv`; the batch continues.
  Conditions that would fail identically for all files (invalid key, unknown
  model) abort immediately instead of burning the whole batch.
- **Aspect enforced.** `9:16` is requested via `image_config`, then verified and
  centre-cropped with Pillow as a fallback.

## Notes on the original specification

Three points in the spec do not hold against the live API:

1. **`imagen-3.0-generate-002` cannot do this.** It is text-to-image only; the
   `generate_images` endpoint accepts no reference image, so identity
   preservation is impossible with it. This script uses
   `gemini-2.5-flash-image`, which accepts an image plus a prompt on
   `generate_content`. Override with `--model` if needed.
2. **`ALLOW_ADULT` is not available here.** `person_generation` is an
   Imagen/Vertex parameter; the Developer API rejects it with
   *"person_generation parameter is only supported in ... Platform mode"*
   (verified). The closest available control is
   `HarmBlockThreshold.BLOCK_ONLY_HIGH` on the four configurable categories,
   which is what the script sets. It reduces false positives on fashion content
   but does not disable policy enforcement — expect some references to be
   refused regardless of prompt wording.
3. **Naming.** The spec's `gen_[original_filename].jpg` would yield
   `gen_photo.png.jpg` for PNG inputs. The script uses the stem:
   `photo.png` → `gen_photo.jpg`.
