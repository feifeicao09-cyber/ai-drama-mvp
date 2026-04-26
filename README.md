# AI Drama Final

A GitHub-ready AI short drama pipeline.

## What it does
- Generates a multi-episode story from an idea and style
- Builds storyboard shots per episode
- Renders vertical storyboard images
- Generates subtitle files
- Generates audio tracks (silent fallback by default)
- Assembles episode MP4 files with FFmpeg
- Optionally concatenates a full season video

## Quick start

```bash
pip install -r requirements.txt
python main.py --idea "A bullied boy discovers a dark power" --style "dark revenge cinematic" --episodes 3
```

## Output
- `output/episode_1.mp4`
- `output/episode_2.mp4`
- `output/episode_3.mp4`
- `output/season.mp4`

## Notes
- The default build is fully runnable offline.
- It uses generated storyboard art and silent audio so the full workflow can run in GitHub Actions.
- You can later replace the renderer or voice generator with any external AI service.
