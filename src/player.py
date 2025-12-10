"""
Playback logic using system TTS (`say` on macOS) and user prompts.
"""

from typing import List
import time
import subprocess
import shlex

from .models import PlayStep
from .config import (
    DEFAULT_AI_PAUSE_SECONDS,
    WAIT_FOR_USER_ON_THEIR_LINES,
    TTS_VOICE_NAME,
    TTS_RATE,
    TTS_VOLUME,  # not used with `say` but kept for future
)


def init_tts_engine():
    """
    Placeholder to match previous interface.
    With system `say`, we don't need an engine object.
    """
    return None


def speak_line(engine, text: str) -> None:
    """
    Use macOS `say` command to speak the given text.

    - If TTS_VOICE_NAME is set, we pass `-v <voice>`
    - If TTS_RATE is set, we pass `-r <rate>` (roughly words per minute)
    """
    if not text:
        return

    cmd = ["say"]

    if TTS_VOICE_NAME:
        cmd += ["-v", TTS_VOICE_NAME]

    if TTS_RATE:
        cmd += ["-r", str(TTS_RATE)]

    cmd.append(text)

    # print(f"[system say] {' '.join(shlex.quote(c) for c in cmd)}")

    subprocess.run(cmd)


def play_sequence(steps: List[PlayStep]) -> None:
    """
    Play through the sequence of steps.

    Behavior:
        - For AI steps:
            * Print the character + text
            * Call speak_line(...)
            * Sleep for DEFAULT_AI_PAUSE_SECONDS
        - For YOU steps:
            * Print "YOU: <text>"
            * If WAIT_FOR_USER_ON_THEIR_LINES:
                  wait for input("Press Enter when you've said your line...")
              else:
                  estimate a rough time based on line length and sleep
    """
    engine = init_tts_engine()  # not used, but keeps interface consistent

    print(f"Total steps: {len(steps)}")
    print("Step types:", [step.type for step in steps])

    print("\n--- Starting scene ---\n")

    for idx, step in enumerate(steps):
        # print(f"\n[play_sequence] Step {idx}: type={step.type}, character={step.character}")

        if step.type == "AI":
            speaker = step.character or "AI"
            print(f"{speaker}: {step.text}")
            speak_line(engine, step.text)

            # Short pause after AI speaks
            time.sleep(DEFAULT_AI_PAUSE_SECONDS)

        else:
            speaker = step.character or "YOU"
            print(f"{speaker} (YOU): {step.text}")

            if WAIT_FOR_USER_ON_THEIR_LINES:
                input("Say your line now, then press Enter to continue...")
            else:
                # Rough estimate: assume ~2.5 words per second, minimum 1.5 seconds
                num_words = len(step.text.split())
                estimated_seconds = max(1.5, num_words / 2.5)
                time.sleep(estimated_seconds)

    print("\n--- End of scene ---\n")
