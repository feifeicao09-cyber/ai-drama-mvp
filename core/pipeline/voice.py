import math
import os
import struct
import wave
from pathlib import Path
from typing import Dict

from config import AUDIO_DIR
from core.utils import ensure_dir


class VoiceGenerator:
    def __init__(self):
        self.output_dir = AUDIO_DIR
        ensure_dir(self.output_dir)

    def generate(self, project: Dict):
        backend = os.getenv("VOICE_BACKEND", "silent").lower()
        for ep in project.get("episodes", []):
            total_seconds = sum(max(shot.get("duration", 3), 1) for shot in ep.get("shots", []))
            audio_path = self.output_dir / f"ep_{ep['id']}.wav"
            if backend == "pyttsx3":
                try:
                    self._pyttsx3_generate(ep, audio_path)
                except Exception:
                    self._silent_wav(audio_path, total_seconds)
            else:
                self._silent_wav(audio_path, total_seconds)
            ep["audio"] = str(audio_path)

    def _silent_wav(self, path: Path, duration_seconds: int, sample_rate: int = 16000):
        frames = duration_seconds * sample_rate
        ensure_dir(path.parent)
        with wave.open(str(path), "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            silence = struct.pack("<h", 0)
            for _ in range(frames):
                wf.writeframesraw(silence)

    def _pyttsx3_generate(self, ep: Dict, audio_path: Path):
        import pyttsx3  # optional
        engine = pyttsx3.init()
        texts = [shot.get("dialogue", "") or shot.get("visual", "") for shot in ep.get("shots", [])]
        text = " ".join(texts)
        engine.save_to_file(text, str(audio_path))
        engine.runAndWait()
