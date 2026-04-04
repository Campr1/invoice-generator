#!/usr/bin/env python3
"""Turn rough job notes into polished invoice-scope bullet points."""

import argparse
import os
import sys
from pathlib import Path

from openai import OpenAI


DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert rough renovation or job notes into invoice-ready scope bullets."
    )
    parser.add_argument(
        "notes",
        nargs="?",
        help="Rough notes as a single quoted string. If omitted, the script reads from stdin.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use. Defaults to {DEFAULT_MODEL}.",
    )
    return parser.parse_args()


def read_notes(args):
    if args.notes:
        return args.notes.strip()

    if not sys.stdin.isatty():
        return sys.stdin.read().strip()

    print("Paste rough notes, then press Ctrl-D when finished:\n")
    return sys.stdin.read().strip()


def build_prompt(rough_notes):
    return f"""You rewrite rough contractor or job notes into a polished invoice scope.

Requirements:
- Return only bullet points.
- Keep the wording professional, concise, and client-safe.
- Preserve the actual work described in the notes.
- Remove slang, fragments, and repetition.
- Do not invent pricing, dates, or materials that were not mentioned.
- Make each bullet suitable to paste directly into an invoice.

Rough notes:
{rough_notes}
"""


def load_env_file(env_path=".env"):
    path = Path(env_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def generate_scope(client, model, rough_notes):
    response = client.responses.create(
        model=model,
        input=build_prompt(rough_notes),
    )
    return response.output_text.strip()


def main():
    args = parse_args()
    rough_notes = read_notes(args)
    if not rough_notes:
        raise SystemExit("No notes provided. Pass notes as an argument or pipe them through stdin.")

    load_env_file()
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Export it before running this script.")

    client = OpenAI()
    polished_scope = generate_scope(client, args.model, rough_notes)
    print(polished_scope)


if __name__ == "__main__":
    main()
