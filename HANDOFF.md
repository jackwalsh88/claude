# Handoff: Batch Image-to-Image Generation Pipeline

Read this first if you are a Claude Code agent picking this up on a new
machine. Context below is everything the prior session learned; nothing
else is needed except what's called out under "What this PC must still
supply."

## Status

Code is complete, committed, and pushed to this branch. **It has not been
run end-to-end.** The prior session's container had no `GEMINI_API_KEY` and
no real reference photos — only a synthetic test image and a deliberately
invalid key were used, to validate error handling and request shape, not to
produce a real output.

## Repo / branch

- Repo: `jackwalsh88/claude`
- Branch: `claude/new-session-4904nt` (already checked out if you cloned
  this branch directly)
- Clone: `git clone -b claude/new-session-4904nt https://github.com/jackwalsh88/claude`

## Files in the branch

| File | Purpose |
|---|---|
| `run_batch.py` | The batch runner. Read its module docstring and inline comments — the safety/model comments explain the deviations below. |
| `requirements.txt` | `google-genai`, `pillow`, `python-dotenv` |
| `.env.example` | Template for `.env` — copy it, do not commit the real one |
| `.gitignore` | Excludes `.env` and the contents of `input/`/`output/` |
| `README.md` | Full usage docs — flags, exit codes, resumability |
| `input/`, `output/` | Empty except `.gitkeep` |

## Original task

Batch-process ~50 reference photos through Google AI Studio's image API,
generating 9:16 editorial portraits that preserve the model's identity, from
a fixed prompt, resumable and rate-limited. Full original spec was supplied
as a task file in the prior session, not committed to the repo; the details
that matter are captured below and in `README.md`.

## Deviations from the original spec — verified against the live API, not guessed

1. **`imagen-3.0-generate-002` cannot do this task.** It is text-to-image
   only; `generate_images` accepts no reference image, so identity
   preservation is impossible with it. The script uses
   `gemini-2.5-flash-image` instead, which accepts an image + prompt via
   `generate_content`. Override with `--model` if a better image-editing
   model is available by the time this runs.
2. **`person_generation=ALLOW_ADULT` does not exist on this API path.**
   Confirmed via a live 400 response: *"person_generation parameter is only
   supported in Gemini Enterprise Agent Platform mode, not in Gemini
   Developer API mode."* It is Imagen/Vertex-only. The script instead sets
   `HarmBlockThreshold.BLOCK_ONLY_HIGH` on the four configurable safety
   categories — the most permissive setting the Developer API accepts. This
   reduces false positives on fashion/swimwear content but does not disable
   enforcement; **expect some real references to still be refused**, logged
   per-file to `failures.csv` rather than crashing the batch.
3. **Output naming uses the file stem**, not the literal spec pattern —
   `gen_photo.jpg` rather than `gen_photo.png.jpg` for PNG inputs.

## What this PC must still supply

Nothing here is packaged, on purpose:

- **`GEMINI_API_KEY`** — get one at https://aistudio.google.com/apikey,
  put it in a local `.env` (copy `.env.example`). Never commit it.
- **The ~50 reference photos** — copy into `input/` (`.jpg`/`.jpeg`/`.png`/`.webp`).

## Setup (Windows, Python 3.10+ already confirmed present)

```powershell
py -3 -m venv .venv
.venv\Scripts\activate          # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env          # then paste the real key
```

## Run

```powershell
python run_batch.py --dry-run     # confirms files are found, no API calls
python run_batch.py --limit 1     # generate one, inspect output\gen_*.jpg by eye
python run_batch.py --verbose     # full batch — resumable, ~10-20 min for 50 images
```

Exit codes: `0` done clean, `1` no input files found, `2` completed with
some per-file failures (see `failures.csv`), `3` aborted on a fatal
condition (bad key, unknown model), `130` interrupted.

## Not yet validated — do these first on the new machine

1. A real successful generation end-to-end (only the invalid-key error path
   has been exercised so far).
2. Real safety-filter behavior against actual fashion/swimwear references —
   the prompt wording follows the spec's "tested prompt" claim, but that
   claim is unverified against this content; do the `--limit 1` run and
   actually look at the result before starting the full 50-image batch.
