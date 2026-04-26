import json
from typing import Dict

from core.characters.manager import CharacterManager
from core.characters.prompt_builder import PromptBuilder
from core.pipeline.renderer import Renderer


class Director:
    def __init__(self):
        self.character_manager = CharacterManager()
        self.renderer = Renderer()

    def run(self, project: Dict):
        for ep in project.get("episodes", []):
            print(f"\nEpisode {ep['id']}")
            for shot in ep.get("shots", []):
                characters = self.character_manager.load_characters(shot["characters"])
                prompt = PromptBuilder.build_multi_character_prompt(
                    characters=characters,
                    scene_desc=shot["scene"],
                    shot_type=shot["type"],
                    camera_move=shot["camera"],
                    emotion=shot["emotion"],
                )
                image_path = self.renderer.render(prompt, characters, ep["id"], shot["id"])
                shot["image"] = image_path
                shot["prompt"] = prompt
                print(f"  Shot {shot['id']} -> {image_path}")
        return project
