"""
Builds a playback sequence from parsed script lines.
"""

from typing import List
from .models import ScriptLine, PlayStep


def build_sequence(lines: List[ScriptLine], my_character: str) -> List[PlayStep]:
    """
    Given parsed script lines and the name of the character you’re playing,
    build a sequence of PlayStep objects.

    Example:
        If my_character == "JAMIE":

        JAMIE: I can’t believe you did that.
        ALEX: Someone had to.

        -> [
              PlayStep(type="YOU", text="I can’t believe you did that.", character="JAMIE"),
              PlayStep(type="AI",  text="Someone had to.", character="ALEX"),
           ]
    """
    steps: List[PlayStep] = []
    my_character = my_character.strip().upper()
    for line in lines:
        line = line.character.strip().upper()
        if line == my_character:
            steps.append(PlayStep(type="YOU", text=line.text, character=line.character))
        else:
            steps.append(PlayStep(type="AI", text=line.text, character=line.character))
    return steps