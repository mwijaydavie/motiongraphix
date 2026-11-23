# Noellyne: animation plan

## Approved direction
A warm, witty Tanzanian Afro presenter. Bongo Kiswahili with a little Swanglish; observational humour, smart twist, expressive side-eye. One consistent voice and face, no joke copying. She is a separate character from the earlier Noellyne host rig in the other repo, even though they share a name.

## Pose library
| Key | Intent | Visual reference |
|---|---|---|
| open | welcoming / explain | poses/presenter-open.png |
| wave | opening and greeting | poses/presenter-wave.png |
| point | refer to card at frame left | poses/presenter-point.png |
| peace | two items | poses/presenter-peace.png |
| like | approve | poses/presenter-like.png |
| ok | agreement | poses/presenter-ok.png |
| pray | thank you / CTA, hands together | poses/presenter-thanks.png |
| surprise | twist / reaction | poses/presenter-surprised.png |
| side-eye | sarcastic reaction | poses/side-eye.png |
| think | curiosity | poses/thinking.png |
| laugh | joy | poses/laughing.png |

These are separate AI images: their limb positions and face pixels are not registered, so crossfading them is not a genuine articulated gesture. Keep them as concepts, not interchangeable sprite layers.

## Rig construction (not yet built)
1. Choose one neutral pose as rig master. Prepare separate aligned transparent layers: torso, neck, head/hair, front and rear upper arms, forearms, and hand variants. Include hidden-area paint and fixed shoulder, elbow, neck and wrist pivots. Use the same canvas coordinates for every part.
2. From that exact head create aligned blink/eyes-open, eyebrow expressions and at least eight mouth/viseme states with identical face proportions and lighting. Test seams and lip registration at native size. Independently generated full poses cannot safely be cut together without cleanup.
3. Animate head turn/tilt modestly around neck pivot; independent blinks and gaze; gestures rotate from actual joints with ease/spring, avoiding disconnected wrists. Preserve hair silhouette and avoid painting over the face.
4. Time mouth shapes from a recorded/consented voice performance, manually correcting Kiswahili consonants and vowels. Test aligner output with native speakers; English phoneme assumptions are not a guarantee. Add rests and expression holds, not constant flapping.
5. Build deterministic frame-based scene in Remotion/React; separate presenter motion from motion-graphics cards, give comic pauses room. First test: greeting, side-eye, point, short punchline, laugh. Evaluate head seams, hands, speech sync and naturalness before full episodes.

## Constraints
No layered rig, facial assets, voice recording, lip-sync test, or animated video is included yet. Images are visual explorations; pose consistency and hand anatomy need close review. Preserve original sources and document versions; never substitute the previous host's rig without explicit approval.
