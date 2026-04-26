import json
from pathlib import Path
from typing import Dict, List, Optional

from config import CHARACTER_DIR


class CharacterManager:
    def __init__(self, character_dir: Path = CHARACTER_DIR):
        self.character_dir = character_dir
        self.character_dir.mkdir(parents=True, exist_ok=True)

    def load_character(self, character_id: str) -> Dict:
        path = self.character_dir / f"{character_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Character file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_characters(self, character_ids: List[str]) -> List[Dict]:
        return [self.load_character(cid) for cid in character_ids]

    def save_character(self, character_data: Dict) -> None:
        character_id = character_data["id"]
        path = self.character_dir / f"{character_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(character_data, f, ensure_ascii=False, indent=2)

    def list_characters(self) -> List[str]:
        return sorted([p.stem for p in self.character_dir.glob("*.json")])

    def get_reference_image(self, character_id: str) -> Optional[str]:
        return self.load_character(character_id).get("reference_image")

    def get_lora_path(self, character_id: str) -> Optional[str]:
        return self.load_character(character_id).get("lora_path")

    def build_anchor_text(self, character_id: str) -> str:
        data = self.load_character(character_id)
        return data.get("prompt_anchor", data["name"])
