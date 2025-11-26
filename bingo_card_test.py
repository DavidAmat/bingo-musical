#!/usr/bin/env python3
"""
Generate a single musical bingo card for testing styles and design.

This simplified version has hardcoded parameters and outputs a single HTML file
to make it easier to iterate on the design.
"""
import random
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Constants
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "songs.yaml"
TPL_DIR = ROOT / "templates"
OUTPUT_FILE = ROOT / "test_card.html"


def load_songs(path: Path):
    """Load songs from the YAML file."""
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    songs = payload.get("songs", [])
    if len(songs) < 8:
        raise ValueError("Need at least 8 songs in the YAML to sample a card.")
    return songs


def sample_songs(all_songs, k=8):
    """Randomly sample k songs from the list."""
    picks = random.sample(all_songs, k)
    random.shuffle(picks)
    return picks


def main():
    # Hardcoded parameters
    title = "BINGO MUSICAL DE PRUEBA"
    background_color = "#700302"
    card_number = 1
    seed = 42
    images = [str(ROOT / "images" / "hat.png"), str(ROOT / "images" / "notes.png")]

    # Set seed for reproducibility
    random.seed(seed)

    # Load songs
    songs = load_songs(DATA)

    # Set up Jinja environment
    env = Environment(
        loader=FileSystemLoader(str(TPL_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Get template
    card_tpl = env.get_template("card.html.j2")

    # Prepare title decoration images
    title_images = []
    for i, path in enumerate(images):
        # Convert to absolute path to ensure images are found regardless of HTML location
        abs_path = Path(path).resolve()
        title_images.append(
            {
                "src": f"file://{abs_path}",  # Use file:// protocol for absolute paths
                "alt": f"decor-{i+1}",
                "position": "left" if i % 2 == 0 else "right",
                "style": "",
            }
        )

    # Generate card payload
    payload = {
        "title": title,
        "card_number": card_number,
        "background_color": background_color,
        "songs": sample_songs(songs, 8),
        "title_images": title_images,
    }

    # Render and save the card
    html = card_tpl.render(**payload)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    print(f"Done. Test card created at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
