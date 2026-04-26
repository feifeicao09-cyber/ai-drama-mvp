import hashlib
import textwrap
from pathlib import Path
from typing import Iterable, List, Tuple


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value).strip("_")


def prompt_color_seed(text: str) -> Tuple[int, int, int]:
    digest = hashlib.md5(text.encode("utf-8")).hexdigest()
    return tuple(int(digest[i:i+2], 16) for i in (0, 2, 4))


def wrap_text(text: str, width: int = 36) -> List[str]:
    return textwrap.wrap(text, width=width) if text else [""]


def format_srt_timestamp(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    ms = int(round((seconds - int(seconds)) * 1000))
    total = int(seconds)
    hh = total // 3600
    mm = (total % 3600) // 60
    ss = total % 60
    return f"{hh:02}:{mm:02}:{ss:02},{ms:03}"


def concat_episode_list_file(entries: Iterable[Tuple[str, float]], out_path: Path) -> None:
    lines = []
    for file_path, duration in entries:
        lines.append(f"file '{Path(file_path).as_posix()}'")
        lines.append(f"duration {duration}")
    if entries:
        last_path = Path(list(entries)[-1][0]).as_posix()
        lines.append(f"file '{last_path}'")
    out_path.write_text("\n".join(lines), encoding="utf-8")
