# Noellyne intro v2 — pose-cut prototype

34-second 540 × 960, 24 fps MP4; reuses the selected Swahili voice from `../noellyne-intro/voice.mp3`. The edit uses five complete pose images with deliberate cuts rather than a detached hand; an AI-edited mouth patch is softly blended at each pose, driven by audio energy. The original outfit remains unchanged.

Not a finished performance: hand/head movements are still cuts between flattened poses, not joint animation. The mouth only reacts to audio loudness; it is not phoneme-aligned and mouth shapes remain limited. Gaze/blink and subtitles are not implemented, and voice accent is not guaranteed Tanzanian. Review image registration and audio sync before any release. A rigged character with isolated head, eyes, jaw and arm geometry is needed for true continuous movement.

Run `python production/noellyne-intro-v2/render.py` with requirements in `../noellyne-intro/requirements.txt`. `qc.jpg` samples poses, not a substitute for playback review.
