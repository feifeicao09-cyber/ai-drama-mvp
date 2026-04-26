from pathlib import Path
from typing import Dict, List

from PIL import Image, ImageDraw, ImageFont

from config import GENERATED_DIR
from core.utils import ensure_dir, prompt_color_seed, wrap_text


class Renderer:
    def __init__(self):
        self.output_dir = GENERATED_DIR
        ensure_dir(self.output_dir)

    def render(self, prompt: str, characters: List[Dict], ep_id: int, shot_id: int) -> str:
        folder = self.output_dir / f"ep_{ep_id}"
        ensure_dir(folder)

        path = folder / f"shot_{shot_id}.png"
        self._render_image(prompt, characters, ep_id, shot_id, path)
        return str(path)

    def _render_image(self, prompt: str, characters: List[Dict], ep_id: int, shot_id: int, out_path: Path) -> None:
        img = Image.new("RGB", (720, 1280), color=prompt_color_seed(prompt))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        title = f"EP {ep_id} / SHOT {shot_id}"
        draw.rounded_rectangle((30, 30, 690, 120), radius=20, fill=(0, 0, 0))
        draw.text((50, 48), title, fill=(255, 255, 255), font=font)

        y = 160
        lines = ["PROMPT:"] + wrap_text(prompt, 34)
        for line in lines:
            draw.text((40, y), line, fill=(255, 255, 255), font=font)
            y += 24

        y += 20
        draw.text((40, y), "CHARACTERS:", fill=(255, 255, 255), font=font)
        y += 24
        for c in characters:
            draw.text((40, y), f"- {c['name']}", fill=(255, 255, 255), font=font)
            y += 22

        # Decorative lower panel
        draw.rounded_rectangle((30, 1040, 690, 1230), radius=24, fill=(10, 10, 10))
        draw.text((50, 1070), "AI DRAMA FINAL", fill=(255, 255, 255), font=font)
        draw.text((50, 1100), "Generated storyboard frame", fill=(255, 255, 255), font=font)
        draw.text((50, 1130), "Replace this renderer with your AI image API later.", fill=(255, 255, 255), font=font)

        img.save(out_path)
