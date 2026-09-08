#!/usr/bin/env python3
"""Batch image-to-image generation via the Google AI Studio (Gemini) API.

Reads reference photos from input/, sends each one to an image-capable Gemini
model together with a fixed editorial prompt, and writes a 9:16 result to
output/gen_<original_stem>.jpg.

The run is resumable: existing outputs are skipped, and per-file failures are
logged without aborting the batch.
"""

from __future__ import annotations

import argparse
import csv
import io
import logging
import mimetypes
import os
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types

# --- Configuration -----------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "input"
OUTPUT_DIR = PROJECT_DIR / "output"
LOG_PATH = PROJECT_DIR / "run_batch.log"
FAILURE_CSV = PROJECT_DIR / "failures.csv"

# Image-to-image (identity-preserving) editing requires a model that accepts an
# image as *input*. The Imagen `imagen-3.0-generate-002` endpoint is
# text-to-image only and cannot take a reference photo, so it is not usable here.
DEFAULT_MODEL = "gemini-2.5-flash-image"

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
ASPECT_RATIO = "9:16"
TARGET_RATIO = 9 / 16

PROMPT = (
    "Vertical 9:16 medium portrait of the woman from the reference image. "
    "She is standing poolside at a luxury hotel, wearing a neon two-piece "
    "summer resort set with an open linen shirt, relaxed standing pose holding "
    "sunglasses. Warm natural sunlight, candid expression, 35mm film "
    "photography aesthetic, shallow depth of field."
)

# Fashion/swimwear reference photos draw false positives from the default
# thresholds. BLOCK_ONLY_HIGH is the most permissive setting the Developer API
# accepts; it reduces false positives but cannot disable policy enforcement.
#
# There is no ALLOW_ADULT knob on this path: `person_generation` exists only on
# Imagen/Vertex and the Developer API rejects it outright with
# "person_generation parameter is only supported in ... Platform mode".
SAFETY_SETTINGS = [
    types.SafetySetting(category=c, threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH)
    for c in (
        types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    )
]

MAX_INPUT_EDGE = 1536  # downscale references before upload to save bandwidth
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

log = logging.getLogger("run_batch")


# --- Errors ------------------------------------------------------------------


class GenerationError(RuntimeError):
    """A per-file failure that should be logged and skipped, not fatal."""


class BlockedError(GenerationError):
    """The request or response was stopped by a safety filter."""


class FatalError(RuntimeError):
    """A condition that will fail identically for every remaining file."""


# --- Helpers -----------------------------------------------------------------


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_PATH)],
    )


def load_api_key() -> str:
    """Read GEMINI_API_KEY from .env or the environment, failing loudly."""
    load_dotenv(PROJECT_DIR / ".env")
    key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    if not key:
        raise SystemExit(
            "GEMINI_API_KEY is not set.\n"
            f"Create {PROJECT_DIR / '.env'} containing:\n"
            "    GEMINI_API_KEY=<your key>\n"
            "Get a key at https://aistudio.google.com/apikey"
        )
    if key in {"your_key_here", "..."}:
        raise SystemExit("GEMINI_API_KEY is still the placeholder value.")
    log.info("API key loaded (%d chars, ends %s).", len(key), key[-4:])
    return key


def discover_inputs() -> list[Path]:
    if not INPUT_DIR.is_dir():
        raise SystemExit(f"Input directory not found: {INPUT_DIR}")
    files = sorted(
        p
        for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )
    return files


def output_path_for(src: Path) -> Path:
    return OUTPUT_DIR / f"gen_{src.stem}.jpg"


def load_reference(path: Path) -> types.Part:
    """Open, EXIF-orient and downscale a reference photo into an inline Part."""
    with Image.open(path) as im:
        im = im.convert("RGB")
        try:
            from PIL import ImageOps

            im = ImageOps.exif_transpose(im)
        except Exception:  # pragma: no cover - EXIF is optional
            pass
        im.thumbnail((MAX_INPUT_EDGE, MAX_INPUT_EDGE), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=92)
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")


def extract_image_bytes(response) -> bytes:
    """Pull the first inline image out of a generate_content response."""
    feedback = getattr(response, "prompt_feedback", None)
    if feedback is not None and getattr(feedback, "block_reason", None):
        raise BlockedError(f"prompt blocked: {feedback.block_reason}")

    for candidate in response.candidates or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", None) or []:
            blob = getattr(part, "inline_data", None)
            if blob is not None and blob.data:
                return blob.data
        reason = str(getattr(candidate, "finish_reason", "") or "")
        if reason and reason.upper() not in {"STOP", "FINISH_REASON_STOP"}:
            raise BlockedError(f"no image, finish_reason={reason}")

    text = (getattr(response, "text", None) or "").strip()
    raise GenerationError(f"response contained no image{': ' + text[:200] if text else ''}")


def enforce_aspect(data: bytes) -> bytes:
    """Guarantee a 9:16 JPEG regardless of what the model returned."""
    with Image.open(io.BytesIO(data)) as im:
        im = im.convert("RGB")
        w, h = im.size
        if abs((w / h) - TARGET_RATIO) > 0.01:
            if (w / h) > TARGET_RATIO:  # too wide -> crop sides
                new_w = round(h * TARGET_RATIO)
                left = (w - new_w) // 2
                im = im.crop((left, 0, left + new_w, h))
            else:  # too tall -> crop top/bottom, biased toward the head
                new_h = round(w / TARGET_RATIO)
                top = (h - new_h) // 3
                im = im.crop((0, top, w, top + new_h))
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=95, subsampling=0)
    return buf.getvalue()


def is_fatal(exc: Exception) -> bool:
    """Bad credentials or a bad model name will fail for all 50 files alike."""
    if isinstance(exc, genai_errors.APIError):
        if getattr(exc, "code", None) in {401, 403, 404}:
            return True
        return getattr(exc, "code", None) == 400 and "API key not valid" in str(exc)
    return False


def is_retryable(exc: Exception) -> bool:
    if isinstance(exc, genai_errors.APIError):
        return getattr(exc, "code", None) in RETRYABLE_STATUS
    return isinstance(exc, (TimeoutError, ConnectionError))


# --- Core --------------------------------------------------------------------


@dataclass
class Stats:
    generated: int = 0
    skipped: int = 0
    failed: int = 0


def generate_one(client: genai.Client, model: str, src: Path, attempts: int) -> bytes:
    """Call the API for one reference image, retrying transient errors."""
    reference = load_reference(src)
    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        safety_settings=SAFETY_SETTINGS,
        image_config=types.ImageConfig(aspect_ratio=ASPECT_RATIO),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = client.models.generate_content(
                model=model, contents=[reference, PROMPT], config=config
            )
            return extract_image_bytes(response)
        except BlockedError:
            raise  # a safety block will not resolve on retry
        except Exception as exc:  # noqa: BLE001 - classified below
            last = exc
            if attempt == attempts or not is_retryable(exc):
                raise
            backoff = min(2 ** attempt, 30) + random.uniform(0, 1)
            log.warning(
                "  attempt %d/%d failed (%s); retrying in %.1fs",
                attempt, attempts, type(exc).__name__, backoff,
            )
            time.sleep(backoff)
    raise GenerationError(str(last))


def record_failure(src: Path, exc: Exception) -> None:
    new = not FAILURE_CSV.exists()
    with FAILURE_CSV.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if new:
            writer.writerow(["filename", "error_type", "message"])
        writer.writerow([src.name, type(exc).__name__, str(exc)[:500]])


def run(args: argparse.Namespace) -> int:
    api_key = load_api_key()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = discover_inputs()
    if not files:
        log.error(
            "No images found in %s (looked for %s).",
            INPUT_DIR, ", ".join(sorted(SUPPORTED_SUFFIXES)),
        )
        return 1
    if args.limit:
        files = files[: args.limit]

    client = genai.Client(api_key=api_key)
    stats = Stats()
    log.info("Model %s | %d candidate file(s) | delay %.1fs", args.model, len(files), args.delay)

    for index, src in enumerate(files, start=1):
        dest = output_path_for(src)
        if dest.exists() and not args.force:
            stats.skipped += 1
            log.info("[%d/%d] skip %s (already generated)", index, len(files), src.name)
            continue

        log.info("[%d/%d] %s -> %s", index, len(files), src.name, dest.name)
        if args.dry_run:
            stats.skipped += 1
            continue

        started = time.monotonic()
        try:
            data = enforce_aspect(generate_one(client, args.model, src, args.attempts))
        except Exception as exc:  # noqa: BLE001 - per-file isolation is the point
            if is_fatal(exc):
                log.error("Aborting batch: %s", exc)
                raise FatalError(str(exc)) from exc
            stats.failed += 1
            log.error("  FAILED %s: %s: %s", src.name, type(exc).__name__, exc)
            record_failure(src, exc)
        else:
            tmp = dest.with_suffix(".jpg.part")
            tmp.write_bytes(data)
            tmp.replace(dest)  # atomic: a partial write never looks "done"
            stats.generated += 1
            log.info("  ok in %.1fs (%.0f KB)", time.monotonic() - started, len(data) / 1024)

        if index < len(files):
            time.sleep(args.delay)

    log.info(
        "Done. generated=%d skipped=%d failed=%d", stats.generated, stats.skipped, stats.failed
    )
    if stats.failed:
        log.info("Failures listed in %s. Re-run to retry only those.", FAILURE_CSV.name)
    return 0 if stats.failed == 0 else 2


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=os.getenv("GEMINI_IMAGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--delay", type=float, default=2.5, help="seconds between API calls")
    parser.add_argument("--attempts", type=int, default=3, help="tries per image on transient errors")
    parser.add_argument("--limit", type=int, default=0, help="process at most N images (0 = all)")
    parser.add_argument("--force", action="store_true", help="regenerate even if output exists")
    parser.add_argument("--dry-run", action="store_true", help="list work without calling the API")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


if __name__ == "__main__":
    ns = parse_args()
    configure_logging(ns.verbose)
    try:
        sys.exit(run(ns))
    except FatalError:
        sys.exit(3)
    except KeyboardInterrupt:
        log.warning("Interrupted. Re-run to resume from the last completed image.")
        sys.exit(130)
