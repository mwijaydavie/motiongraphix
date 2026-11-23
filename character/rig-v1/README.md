# Noellyne rig study v1

Independent layered 2D rig test: cleaned AI-generated background/body plates, extracted head and raised arm layers rotating around separate neck and elbow/cuff pivots, masked mouth and blink artwork, original selected Swahili voice excerpt. The render is 8 seconds, 540x960, 24 fps, H.264/AAC. `render.py` rebuilds the layers procedurally from the stored assets and the earlier intro voice.

Limitations: derived from flattened image, segmentation/AI-generated plates can produce small edge or shoulder artifacts. Head and arm rotate as rigid 2D layers; no separate hand/wrist/upper arm articulation, 3D head rotation or eye gaze. There are only open/closed mouth states, driven by audio intensity rather than phonemes, so this is not accurate speech lip sync. Eyelid blink is a single edited state. Voice uses generic Swahili, not guaranteed Tanzanian accent. Outfit intentionally unchanged. This is a focused rig test, not the finished 30-second video.

Run `python character/rig-v1/render.py`, after installing `production/noellyne-intro/requirements.txt`.
