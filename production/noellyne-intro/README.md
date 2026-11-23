# Noellyne introduction — motion test 01

33.96-second vertical draft, H.264/AAC, 540 × 960, 24 fps. Kiswahili speech is synthesized from a user-selected generic `sw` voice; the `sw-TZ` regional audition was unavailable, so a Bongo accent is not guaranteed. Original presenter image and outfit remain unchanged pending redesign.

This is an experimental 2D cutout, not a finished character performance. The hand cutout rotates over a reconstructed background and can show visible seams; whole-image tilt is not a separate neck/head rig. Mouth opens using audio energy, not phonemes; eyes use rough blink overlays and do not have independent gaze. Text cards are editorial beats, not exact captions. Correct Kiswahili timing, facial registration, head and elbow joints, voice performance, and outfit are open work. No motion-capture or 3D claim.

Reproduce from repository root: `python -m pip install -r production/noellyne-intro/requirements.txt`, then `python production/noellyne-intro/render.py`. Source voice and finished draft are retained in this folder. The renderer uses the packaged FFmpeg binary from imageio-ffmpeg and local DejaVu fonts.

## Research consulted
- Rhubarb Lip Sync phonetic recognizer (language-independent, a candidate for non-English speech): https://github.com/DanielSWolf/rhubarb-lip-sync ; Kiswahili results require testing and manual correction.
- PuppetControl: https://github.com/nkcbuilds/PuppetControl — joint-driven arm motion, explicit transitions between compatible pose families, head/gaze timelines and Rhubarb integration. It is an experimental reference, not integrated here.
- https://github.com/FireAmun/remotion-dev-video-kit — example audio-amplitude mouth animation; a useful rough prototype, not phonetic lip sync.
