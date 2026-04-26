import argparse
import json
from pathlib import Path

from core.story import generate_story, load_or_create_project
from core.storyboard import generate_storyboard
from core.pipeline.director import Director
from core.pipeline.voice import VoiceGenerator
from core.pipeline.subtitle import SubtitleGenerator
from core.pipeline.video import VideoMaker
from config import PROJECT_PATH


def parse_args():
    parser = argparse.ArgumentParser(description="AI Drama Final")
    parser.add_argument("--idea", default="A bullied boy discovers a dark power", help="Story idea")
    parser.add_argument("--style", default="dark revenge cinematic", help="Style prompt")
    parser.add_argument("--episodes", type=int, default=3, help="Number of episodes")
    parser.add_argument("--shots", type=int, default=4, help="Shots per episode")
    return parser.parse_args()


def run():
    args = parse_args()
    project = load_or_create_project(PROJECT_PATH, args.idea, args.style, args.episodes, args.shots)
    project = generate_story(project, args.idea, args.style, args.episodes, args.shots)
    project = generate_storyboard(project)

    director = Director()
    project = director.run(project)

    VoiceGenerator().generate(project)
    SubtitleGenerator().generate(project)
    VideoMaker().make(project)

    PROJECT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROJECT_PATH, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=2)

    print("Done. Check the output/ folder.")


if __name__ == "__main__":
    run()
