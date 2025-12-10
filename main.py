"""
CLI entry point for the AI Scene Partner.

Steps:
    1. Ask user who they're playing.
    2. Parse a script from data/sample_scene.txt (for now).
    3. Build the sequence.
    4. Play the sequence.
"""

import os

from src.parser import parse_script
from src.scheduler import build_sequence
from src.player import play_sequence
from src.config import DEFAULT_MY_CHARACTER


def main() -> None:
    script_path = os.path.join("data", "sample_scene.txt")

    raw_name = input(
        f"Who are you playing? (default: {DEFAULT_MY_CHARACTER}) "
    ).strip()
    my_character = raw_name or DEFAULT_MY_CHARACTER

    lines = parse_script(script_path)

    steps = build_sequence(lines, my_character)

    play_sequence(steps)


if __name__ == "__main__":
    main()
