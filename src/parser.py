"""
Script parser.

Goal:
    Take a plain-text file with lines like:

        JAMIE: I can’t believe you did that.
        ALEX: Someone had to.

    And return a list[ScriptLine].
"""

from typing import List
from .models import ScriptLine


def parse_script(path: str) -> List[ScriptLine]:
    """
    Parse a script file at `path` into ScriptLine objects.

    Assumptions for v1:
        - Each non-empty line has the format "NAME: dialogue"
        - Lines starting with "#" or "//" are comments and should be ignored 
        - Blank lines should be skipped

    """
    # TODO: implement this function
    # Pseudocode:
    lines: List[ScriptLine] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue
            if ":" not in line:
                continue
            name, text = line.split(":", 1)
            name = name.strip().upper()
            text = text.strip()
            if not name or not text:
                continue
            lines.append(ScriptLine(character=name, text=text))
    return lines

def parse_scene_text(scene_text: str) -> List[ScriptLine]:
    """
    Parse scene text from a textbox (Streamlit) into ScriptLine objects.

    Expected format per line:
        NAME: dialogue

    Skips blank lines and comment lines starting with # or //
    """
    lines: List[ScriptLine] = []

    for raw in scene_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("//"):
            continue
        if ":" not in line:
            continue

        name_part, text_part = line.split(":", 1)
        character = name_part.strip().upper()
        text = text_part.strip()

        if not character or not text:
            continue

        lines.append(ScriptLine(character=character, text=text))

    return lines
