from pathlib import Path
from typing import Dict

from config import SUBTITLE_DIR
from core.utils import ensure_dir, format_srt_timestamp


class SubtitleGenerator:
    def __init__(self):
        self.output_dir = SUBTITLE_DIR
        ensure_dir(self.output_dir)

    def generate(self, project: Dict):
        for ep in project.get("episodes", []):
            srt_lines = []
            current = 0.0
            index = 1
            for shot in ep.get("shots", []):
                duration = float(shot.get("duration", 3))
                start = format_srt_timestamp(current)
                current += duration
                end = format_srt_timestamp(current)
                text = shot.get("dialogue") or shot.get("visual") or ""
                srt_lines.extend([
                    str(index),
                    f"{start} --> {end}",
                    text,
                    ""
                ])
                index += 1

            srt_path = self.output_dir / f"ep_{ep['id']}.srt"
            srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
            ep["subtitles"] = str(srt_path)
