import json
from pathlib import Path
from typing import Dict

from config import PROJECT_PATH

DEFAULT_CHARACTERS = [
    {
        "id": "john",
        "name": "John",
        "age": 17,
        "gender": "male",
        "role": "main_character",
        "appearance": {
            "face": "sharp jaw, thin lips, deep eyes",
            "hair": "short black hair",
            "body": "slim build",
            "clothing": "worn school uniform"
        },
        "emotion_base": "quiet, hurt, restrained",
        "voice_style": "calm, low, slightly tense",
        "reference_image": "data/references/john_ref_01.png",
        "lora_path": "data/loras/john.safetensors",
        "prompt_anchor": "17-year-old male, sharp jaw, thin lips, deep eyes, short black hair, slim build, worn school uniform"
    },
    {
        "id": "bully",
        "name": "Bully",
        "age": 18,
        "gender": "male",
        "role": "antagonist",
        "appearance": {
            "face": "wide grin, sharp eyebrows",
            "hair": "messy blond hair",
            "body": "athletic build",
            "clothing": "expensive school jacket"
        },
        "emotion_base": "mocking, arrogant",
        "voice_style": "loud, contemptuous",
        "reference_image": "data/references/bully_ref_01.png",
        "lora_path": "data/loras/bully.safetensors",
        "prompt_anchor": "18-year-old male, wide grin, sharp eyebrows, messy blond hair, athletic build, expensive school jacket"
    },
    {
        "id": "teacher",
        "name": "Teacher",
        "age": 40,
        "gender": "female",
        "role": "supporting",
        "appearance": {
            "face": "tired but kind",
            "hair": "tied back brown hair",
            "body": "average build",
            "clothing": "plain blouse and skirt"
        },
        "emotion_base": "concerned, observant",
        "voice_style": "soft, steady",
        "reference_image": "data/references/teacher_ref_01.png",
        "lora_path": "data/loras/teacher.safetensors",
        "prompt_anchor": "40-year-old female, tired but kind face, tied back brown hair, average build, plain blouse and skirt"
    }
]


def _default_shot(ep_id: int, shot_id: int, total_shots: int) -> Dict:
    hook_texts = [
        "They laughed at him.",
        "He stayed silent.",
        "Then something inside him woke up.",
        "And the room went cold."
    ]
    emotions = ["humiliated", "mocking", "rage", "ominous"]
    scenes = ["classroom", "hallway", "locker room", "empty corridor"]
    shot_types = ["close-up", "wide shot", "extreme close-up", "medium shot"]
    cameras = ["slow zoom in", "pan", "push in", "static"]
    characters = [
        ["john"],
        ["john", "bully"],
        ["john"],
        ["john", "teacher"]
    ]

    idx = (shot_id - 1) % len(hook_texts)
    return {
        "id": shot_id,
        "scene": scenes[idx],
        "type": shot_types[idx],
        "camera": cameras[idx],
        "emotion": emotions[idx],
        "characters": characters[idx],
        "duration": 3,
        "visual": hook_texts[idx],
        "dialogue": hook_texts[idx] if shot_id == 1 else ("" if shot_id < total_shots else "To be continued...")
    }


def load_or_create_project(project_path: Path, idea: str, style: str, episodes: int, shots_per_episode: int) -> Dict:
    project_path.parent.mkdir(parents=True, exist_ok=True)
    if project_path.exists():
        with open(project_path, "r", encoding="utf-8") as f:
            return json.load(f)

    project = {
        "title": "AI Drama Final",
        "idea": idea,
        "style": style,
        "episodes_count": episodes,
        "shots_per_episode": shots_per_episode,
        "characters": DEFAULT_CHARACTERS,
        "episodes": []
    }
    return project


def generate_story(project: Dict, idea: str, style: str, episodes: int, shots_per_episode: int) -> Dict:
    project["idea"] = idea
    project["style"] = style
    project["episodes_count"] = episodes
    project["shots_per_episode"] = shots_per_episode
    project["episodes"] = []

    for ep_id in range(1, episodes + 1):
        episode = {
            "id": ep_id,
            "title": f"Episode {ep_id}",
            "summary": f"{idea}. {style}. Episode {ep_id} escalates the conflict.",
            "shots": []
        }
        project["episodes"].append(episode)

    return project
