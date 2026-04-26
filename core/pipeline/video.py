import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

from config import OUTPUT_DIR
from core.utils import ensure_dir


class VideoMaker:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        ensure_dir(self.output_dir)

    def make(self, project: Dict):
        episode_outputs = []
        for ep in project.get("episodes", []):
            out = self._make_episode_video(ep)
            ep["video"] = out
            episode_outputs.append(out)

        if episode_outputs:
            self._make_season_video(episode_outputs)

    def _make_episode_video(self, ep: Dict) -> str:
        ep_dir = Path("assets/generated") / f"ep_{ep['id']}"
        img_entries: List[Tuple[str, float]] = []
        for shot in ep.get("shots", []):
            image_path = shot.get("image") or str(ep_dir / f"shot_{shot['id']}.png")
            duration = float(shot.get("duration", 3))
            img_entries.append((image_path, duration))

        concat_path = self.output_dir / f"ep_{ep['id']}_images.txt"
        self._write_concat_list(img_entries, concat_path)

        out_path = self.output_dir / f"episode_{ep['id']}.mp4"
        subtitle_path = ep.get("subtitles")
        audio_path = ep.get("audio")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_path),
        ]
        if audio_path:
            cmd += ["-i", audio_path]

        vf_filters = []
        if subtitle_path:
            vf_filters.append(f"subtitles={subtitle_path}")

        if vf_filters:
            cmd += ["-vf", ",".join(vf_filters)]

        cmd += [
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
        ]
        if audio_path:
            cmd += ["-c:a", "aac", "-shortest"]
        else:
            cmd += ["-an"]
        cmd += [str(out_path)]

        subprocess.run(cmd, check=True)
        return str(out_path)

    def _make_season_video(self, episode_videos: List[str]):
        concat_path = self.output_dir / "season_concat.txt"
        lines = []
        for video in episode_videos:
            lines.append(f"file '{Path(video).as_posix()}'")
        concat_path.write_text("\n".join(lines), encoding="utf-8")

        out_path = self.output_dir / "season.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_path),
            "-c", "copy",
            str(out_path)
        ]
        subprocess.run(cmd, check=True)

    def _write_concat_list(self, entries: List[Tuple[str, float]], path: Path):
        lines = []
        for image_path, duration in entries:
            lines.append(f"file '{Path(image_path).as_posix()}'")
            lines.append(f"duration {duration}")
        if entries:
            lines.append(f"file '{Path(entries[-1][0]).as_posix()}'")
        path.write_text("\n".join(lines), encoding="utf-8")
