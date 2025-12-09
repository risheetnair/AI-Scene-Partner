"""
Data models for the AI Scene Partner project.
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class ScriptLine:
    """
    Represents a single line in the script.

    Example:
        ScriptLine(character='JAMIE', text='I can’t believe you did that.')
    """
    character: str
    text: str


StepType = Literal["AI", "YOU"]


@dataclass
class PlayStep:
    """
    Represents one step in the sequence during playback.

    type:
        - "AI"  -> the partner speaks this line
        - "YOU" -> performer speaks this line

    For AI steps, `character` and `text` should be set.
    For YOU steps, `character` could be actor's character name or None, but `text` should exist.
    """
    type: StepType
    text: str
    character: Optional[str] = None
