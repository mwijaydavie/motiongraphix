# Independent head pivot: first test

The existing wave image is separated into an approximate head layer and background-reconstructed body. The head rotates about a neck pivot while the body remains stationary. This demonstrates a real independent 2D layer and pivot, not 3D, face tracking or a production-ready character rig. The generated clip is silent and loops a simple motion for four seconds. Hair masking and jaw/neck seams are not clean; the arms, eyes and mouth do not yet have independent joints in this test. This is exploratory, not approved quality.

Rebuild with `python character/rig-experiments/head-test/render.py` (Pillow and numpy). This produces a GIF; the MP4 was transcoded with imageio-ffmpeg. Rebuilding from separate, properly painted layers rather than cutting a flat image is required to eliminate visible neck seams and generate reliable hand articulation.
