#!/usr/bin/env python3
"""
Generate 30 musical bingo cards (8 songs each) from data/songs.yaml,
render single-card HTML files, and assemble them into A4 2x2 sheets.

Usage:
  python generate_bingo.py --title "Bingo musical LA SIRENA" \
      --bg "#FFEAB3" --images images/hat.png images/notes.png
"""
import random
import math
import argparse
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "songs.yaml"
TPL_DIR = ROOT / "templates"
OUT_CARDS = ROOT / "output" / "cards"
OUT_SHEETS = ROOT / "output" / "sheets"

def load_songs(path: Path):
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    songs = payload.get("songs", [])
    if len(songs) < 8:
        raise ValueError("Need at least 8 songs in the YAML to sample a card.")
    return songs

def sample_songs(all_songs, k=8):
    picks = random.sample(all_songs, k)
    random.shuffle(picks)
    return picks

def chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="BINGO MUSICAL")
    parser.add_argument("--bg", dest="background_color", default="#FFEAB3")
    parser.add_argument("--count", type=int, default=30, help="How many card permutations to create")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility")
    parser.add_argument("--images", nargs="*", default=[], help="List of image paths to decorate the title")
    args = parser.parse_args()

    random.seed(args.seed)

    songs = load_songs(DATA)

    env = Environment(
        loader=FileSystemLoader(str(TPL_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    card_tpl = env.get_template("card.html.j2")
    sheet_tpl = env.get_template("sheet_2x2.html.j2")

    OUT_CARDS.mkdir(parents=True, exist_ok=True)
    OUT_SHEETS.mkdir(parents=True, exist_ok=True)

    # Prepare title decoration images (left/right alternation)
    title_images = []
    for i, path in enumerate(args.images):
        # Convert to absolute path to ensure images are found regardless of HTML location
        abs_path = Path(path).resolve()
        title_images.append({
            "src": f"file://{abs_path}",  # Use file:// protocol for absolute paths
            "alt": f"decor-{i+1}",
            "position": "left" if i % 2 == 0 else "right",
            "style": "",
        })

    # Generate cards
    cards_payload = []
    for i in range(1, args.count + 1):
        payload = {
            "title": args.title,
            "card_number": i,
            "background_color": args.background_color,
            "songs": sample_songs(songs, 8),
            "title_images": title_images,
        }
        cards_payload.append(payload)
        html = card_tpl.render(**payload)
        (OUT_CARDS / f"card_{i:02d}.html").write_text(html, encoding="utf-8")

    # Assemble sheets: 4 cards per sheet
    for idx, group in enumerate(chunk(cards_payload, 4), start=1):
        sheet_html = sheet_tpl.render(
            sheet_title=f"{args.title} — Sheet {idx}",
            cards=group,
        )
        (OUT_SHEETS / f"sheet_{idx:02d}.html").write_text(sheet_html, encoding="utf-8")

    print(f"Done. Cards -> {OUT_CARDS}, Sheets -> {OUT_SHEETS}")

if __name__ == "__main__":
    main()
