# RUN-004 — One-command functional regression

**4/4 passed** on Linux with Unreal Engine 5.9.0 Preview 2. The runner launched four fresh standalone sessions with rendering disabled and a fixed simulation rate of 30 fps. The gameplay assets match [revision 860519b](https://github.com/ornellasdev/Unreal-Engine-5-Technical-QA-Lab/commit/860519bbc16b9affc790fae743541ba2d3d4ca93). [Run it locally](../../../README.md#run-the-functional-regression)

| Case | Observed |
| --- | --- |
| TC-001 | Power was off. The offline warning appeared in the runtime log and the closed door stopped the player at X = 176.55 cm. |
| TC-002 | Power stayed on. After an out-of-range input the door remained closed and blocked the player at the same position. |
| TC-003 | Returning to the terminal triggered one opening. The player crossed the door plane at X = 220 cm and reached X = 454.55 cm. |
| TC-004 | Three extra presses during motion produced a single completion. The elapsed frame count matched TC-003, and the player crossed the doorway. |

A separate failure check supplied an executable that immediately exited with an error. The runner reported four failures and returned exit code 1. A second check changed the final door state in an in-memory copy of the TC-004 log. The verifier rejected the mismatch. [Gameplay evidence](runtime.txt) · [Regression runner](../../run_functional.py)
