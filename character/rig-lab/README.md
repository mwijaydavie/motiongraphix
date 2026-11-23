# Rig Lab 01

Serve repository root: `python3 -m http.server 8000 --bind 0.0.0.0`, then open `/character/rig-lab/`. No dependencies.

This is a deliberately rough interactive study, NOT a production facial rig: the full flattened neutral image is tilted (not an independently articulated head), eyes are drawn blink overlays (not separate gaze controls), mouth shapes are vector placeholders and the demo cycles shapes without audio. The hand menu swaps complete AI-generated pose images, not bones or joint animation. Face controls only work on the neutral master, since other poses are not aligned. Overlays will not perfectly match rendered skin; use the lab to judge direction and find alignment problems, not as final video assets.

Next: create isolated aligned head, eyelids and mouth states in the same lighting, cut and rebuild upper/lower arms and hands with pivots, then implement proper gaze, sync to actual audio and test the result on a real spoken line.
