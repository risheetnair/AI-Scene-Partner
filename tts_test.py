import pyttsx3
import time

engine = pyttsx3.init()

lines = [
    "First test line.",
    "Second test line.",
    "Third test line.",
]

for i, text in enumerate(lines):
    print(f"[TEST] Speaking line {i}: {text!r}")
    engine.stop()
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)
