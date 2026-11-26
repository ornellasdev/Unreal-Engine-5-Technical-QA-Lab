# RUN-007 — Moving door collision at three simulation rates

**TC-006 passed at 30, 60 and 120 simulated fps** in separate headless Unreal Engine 5.9 Preview 2 sessions on Linux. In all three runs the low panel blocked the player, and sustained forward input carried the player underneath before the door finished opening. Gameplay assets match [the tested baseline](https://github.com/ornellasdev/Unreal-Engine-5-Technical-QA-Lab/tree/e4c0b9791245eb87873ffe20706a8147cce6a26a).

| Fixed simulation rate | Opening to Open | First sample across door center | First sample fully clear | Minimum surface gap |
| --- | ---: | ---: | ---: | ---: |
| [30 fps](30.txt) | 0.9667 s | 0.5667 s | 0.6333 s | +0.4489 cm |
| [60 fps](60.txt) | 1.0000 s | 0.5500 s | 0.6167 s | +0.1122 cm |
| [120 fps](120.txt) | 1.0000 s | 0.5583 s | 0.6167 s | +0.0803 cm |

**How to read the measurements.** Times start at the Blueprint's opening event. Crossing times identify the first qualifying sample, so their precision is one simulation step. At 30 fps the two door messages were 29 steps apart, within one step of the one-second animation. The largest spread in measured full-clearance time was about 17 ms. The positive minimum gaps show that none of the sampled positions penetrated the panel.

**Controls.** Each session powered the room and positioned the pawn at (130, −40, 95) cm facing +X. The runner scheduled the same movement and interaction inputs at the same simulated times, including the duration of each key press. It held W throughout opening and sampled the player and door every simulation step from 20/30 to 62/30 seconds after startup. The player center crosses the door plane at X > 220 cm. The entire 35 cm-radius pawn clears the far face at X > 263 cm. Surface gap is the distance from the pawn center to the panel box minus the pawn radius. The collision check permits 1 cm of penetration. The linked tables contain every sample.

**Verifier correction.** The first 60 fps run reported an end height of 369.999925 cm against an expected 370 cm. Exact equality classified the opening as a failure. The endpoint check now accepts a 0.01 cm difference. All three rates were rerun after the correction. This experiment covers one approach with a fixed simulation step and rendering disabled.

### Reproduce

From the repository root on Linux, run:

```bash
python3 -B qa/compare_collision_rates.py --editor "/path/to/Engine/Binaries/Linux/UnrealEditor-Cmd"
```

The runner prints the result for each rate and stores fresh logs and measurement tables under `Saved/QA/`. A failed check returns a nonzero exit code. [Original TC-006 investigation](../RUN-006/README.md)
