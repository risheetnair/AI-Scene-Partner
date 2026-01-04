import time
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

from src.parser import parse_scene_text
from src.scheduler import build_sequence

def estimate_tts_seconds(text: str, rate: float = 1.0) -> float:
    """
    Rough estimate of how long the browser will take to speak `text`.

    - Typical speaking rate ~ 2.5 words/second at rate=1.0
    - Adjust by the Web Speech API rate multiplier
    - Add a small fixed overhead so short lines don't flash
    """
    words = len(text.split())
    words_per_second = 2.5 * max(rate, 0.6)
    base = words / words_per_second if words_per_second else 0.0

    return max(1.0, base + 0.35)


def speak_in_browser(text: str, voice: Optional[str] = None, rate: float = 1.0) -> None:
    """
    Speak text in the user's browser using the Web Speech API (free).
    Note: Voice selection is browser-dependent.
    """
    js = f"""
    <script>
      const text = {text!r};
      const rate = {rate};

      function pickVoice(nameHint) {{
        const voices = window.speechSynthesis.getVoices();
        if (!nameHint) return null;
        const hint = nameHint.toLowerCase();
        return voices.find(v => v.name.toLowerCase().includes(hint)) || null;
      }}

      const u = new SpeechSynthesisUtterance(text);
      u.rate = rate;

      const v = pickVoice({(voice or "")!r});
      if (v) u.voice = v;

      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    </script>
    """
    components.html(js, height=0)


st.set_page_config(page_title="AI Scene Partner", page_icon="🎭", layout="centered")
st.title("🎭 AI Scene Partner")
st.caption("AI lines auto-advance to your turn. You click Next only on your lines.")

default_scene = """JAMIE: I can’t believe you did that.
ALEX: Someone had to.
JAMIE: That’s not an excuse.
ALEX: Maybe not. But it’s the truth.
"""

scene_text = st.text_area("Paste scene (NAME: line per row)", value=default_scene, height=200)

colA, colB = st.columns(2)
with colA:
    my_character = st.text_input("Who are you playing?", value="JAMIE")
with colB:
    auto_speak = st.toggle("Auto-speak AI lines", value=True)

with st.expander("Voice settings (browser-dependent)"):
    browser_voice_hint = st.text_input("Voice hint (optional)", value="")
    browser_rate = st.slider("Speech rate", min_value=0.6, max_value=1.4, value=1.0, step=0.1)

col1, col2 = st.columns(2)
build_clicked = col1.button("Build scene")
reset_clicked = col2.button("Reset")

if reset_clicked:
    st.session_state.pop("steps", None)
    st.session_state.pop("idx", None)
    st.rerun()

if build_clicked or ("steps" not in st.session_state):
    lines = parse_scene_text(scene_text)
    steps = build_sequence(lines, my_character)
    st.session_state["steps"] = steps
    st.session_state["idx"] = 0

steps = st.session_state.get("steps", [])
idx = st.session_state.get("idx", 0)

if not steps:
    st.warning("No valid lines found. Make sure each line is like: NAME: dialogue")
    st.stop()

# End of scene
if idx >= len(steps):
    st.success("✅ End of scene.")
    if st.button("Restart"):
        st.session_state["idx"] = 0
        st.rerun()
    st.stop()

step = steps[idx]
st.subheader(f"Step {idx + 1} / {len(steps)}")

# AI step: speak + auto-advance to YOUR line (no click)
if step.type == "AI":
    st.markdown(f"**AI ({step.character})**: {step.text}")

    if auto_speak:
        speak_in_browser(step.text, voice=browser_voice_hint or None, rate=browser_rate)

    # Keep the AI line visible while it's being spoken (approximate duration)
    wait_seconds = estimate_tts_seconds(step.text, rate=browser_rate)
    time.sleep(wait_seconds)

    st.session_state["idx"] = idx + 1
    st.rerun()


# YOU step: wait for you to click Next
else:
    st.markdown(f"**YOU ({step.character})**: {step.text}")
    st.info("Say your line (pauses/beats are fine). Click Next when you're ready.")

    c1, c2 = st.columns([1, 1])
    if c1.button("Next ▶️"):
        st.session_state["idx"] = idx + 1
        st.rerun()
    if c2.button("Restart"):
        st.session_state["idx"] = 0
        st.rerun()
