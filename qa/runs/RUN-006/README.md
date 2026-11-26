# RUN-006 — Collision while the door is opening

**6/6 functional cases passed** in fresh, headless Unreal Engine 5.9 Preview 2 sessions on Linux. TC-006 adds a moving-contact check to the [five-case baseline](../RUN-005/README.md). Gameplay assets match [revision d7cfea1](https://github.com/ornellasdev/Unreal-Engine-5-Technical-QA-Lab/commit/d7cfea149e0a9d54f05f50c04d666701b2749661).

### TC-006

With the room powered, the test places the player at (130, −40, 95) cm, facing the door along +X. It holds W against the closed panel and presses E once without releasing W. From that point on, the game's movement and collision systems determine the player's position.

| Simulation frame (30 fps) | Observation |
| --- | --- |
| 20 | The closed door stopped the player's center at X = 176.51 cm. |
| 24–35 | Opening started at frame 24. The player remained against the door at X = 176.55 cm through frame 35. |
| 36–43 | The player began moving under the rising edge at frame 36, crossed the center plane (X = 220 cm) between frames 40 and 41, and fully cleared the far face by frame 43. |
| 53 | The door reached Open. W was still held. |

An initial check assumed that the player's center would stay at Z = 95 cm. The recorded trajectory showed that the spherical pawn slid slightly downward around the rising edge. The final test uses the measured X and Z coordinates to check the distance to the physical panel, allowing 1 cm of contact tolerance. None of the sampled positions exceeded that penetration tolerance. This result covers the specified approach at a fixed simulation rate.

[Runtime observations for all six cases](runtime.txt) · [Run the suite locally](../../../README.md#run-the-functional-regression)
