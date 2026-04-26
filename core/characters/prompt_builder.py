from typing import Dict, List


class PromptBuilder:
    @staticmethod
    def build_character_prompt(
        character: Dict,
        scene_desc: str,
        shot_type: str,
        camera_move: str,
        emotion: str,
        lighting: str = "cinematic lighting",
        style: str = "anime cinematic, ultra detailed, high quality"
    ) -> str:
        anchor = character.get("prompt_anchor", character["name"])
        appearance = character.get("appearance", {})
        clothing = appearance.get("clothing", "")
        hair = appearance.get("hair", "")
        face = appearance.get("face", "")
        body = appearance.get("body", "")

        return (
            f"{anchor}, {face}, {hair}, {body}, {clothing}, "
            f"{scene_desc}, {shot_type}, {camera_move}, {emotion}, {lighting}, {style}"
        )

    @staticmethod
    def build_multi_character_prompt(
        characters: List[Dict],
        scene_desc: str,
        shot_type: str,
        camera_move: str,
        emotion: str,
        style: str = "anime cinematic, ultra detailed, high quality"
    ) -> str:
        anchors = [c.get("prompt_anchor", c["name"]) for c in characters]
        character_block = ", ".join(anchors)
        return (
            f"{character_block}, {scene_desc}, {shot_type}, {camera_move}, "
            f"{emotion}, cinematic lighting, {style}"
        )
