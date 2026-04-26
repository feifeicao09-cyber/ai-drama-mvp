from typing import Dict


def generate_storyboard(project: Dict) -> Dict:
    for ep in project.get("episodes", []):
        shots = []
        total = project.get("shots_per_episode", 4)
        for shot_id in range(1, total + 1):
            idx = (shot_id - 1) % 4
            if idx == 0:
                shot = {
                    "id": shot_id,
                    "scene": "dark classroom",
                    "type": "close-up",
                    "camera": "slow zoom in",
                    "emotion": "humiliated",
                    "characters": ["john"],
                    "duration": 3,
                    "visual": "John sits alone while the class stares.",
                    "dialogue": "They laughed at him..."
                }
            elif idx == 1:
                shot = {
                    "id": shot_id,
                    "scene": "classroom aisle",
                    "type": "wide shot",
                    "camera": "pan",
                    "emotion": "mocking",
                    "characters": ["john", "bully"],
                    "duration": 3,
                    "visual": "The bully points and laughs as others join in.",
                    "dialogue": "Everyone mocked him."
                }
            elif idx == 2:
                shot = {
                    "id": shot_id,
                    "scene": "hallway shadows",
                    "type": "extreme close-up",
                    "camera": "push in",
                    "emotion": "rage",
                    "characters": ["john"],
                    "duration": 3,
                    "visual": "John's eyes glow with rising power.",
                    "dialogue": "Until something changed."
                }
            else:
                shot = {
                    "id": shot_id,
                    "scene": "empty corridor",
                    "type": "medium shot",
                    "camera": "static",
                    "emotion": "ominous",
                    "characters": ["john", "teacher"],
                    "duration": 4,
                    "visual": "The teacher senses something dangerous.",
                    "dialogue": "And that was only the beginning."
                }
            shots.append(shot)
        ep["shots"] = shots
    return project
