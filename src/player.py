"""
Playback logic using text-to-speech and user prompts.

This is where the "scene partner" comes alive.
"""

from typing import List
import time

import pyttsx3

from .models import PlayStep
from .config import (
    DEFAULT_AI_PAUSE_SECONDS,
    WAIT_FOR_USER_ON_THEIR_LINES,
    TTS_VOICE_NAME,
    TTS_RATE,
    TTS_VOLUME,
)


def init_tts_engine() -> pyttsx3.Engine:
    """
    Initialize and configure the pyttsx3 engine.
    """
    engine = pyttsx3.init()
    if TTS_RATE is not None:
        engine.setProperty("rate", TTS_RATE)

    if TTS_VOLUME is not None:
        engine.setProperty("volume", TTS_VOLUME)

    if TTS_VOICE_NAME is not None:
        for voice in engine.getProperty("voices"):
            if TTS_VOICE_NAME.lower() in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

    return engine


def speak_line(engine: pyttsx3.Engine, text: str) -> None:
    """
    Use the TTS engine to speak the given text.

    TODO:
        - Call engine.say(text)
        - Call engine.runAndWait()
    """
    engine.say(text)
    engine.runAndWait()
    


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
                  maybe sleep for a fixed amount of time (optional)
    """
    engine = init_tts_engine()

    print("\n--- Starting scene ---\n")

    for step in steps:
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
