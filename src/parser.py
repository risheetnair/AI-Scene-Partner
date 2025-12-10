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
