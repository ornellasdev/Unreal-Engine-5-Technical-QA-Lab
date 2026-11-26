# RUN-005 — Door terminal range boundary

**5/5 local functional cases passed** in Unreal Engine 5.9 Preview 2 on Linux. Each case ran in a fresh headless game process at 30 simulated frames per second. The suite adds TC-005 to the [four-case baseline](../RUN-004/README.md). The map and Blueprint match [revision 36ce101](https://github.com/ornellasdev/Unreal-Engine-5-Technical-QA-Lab/commit/36ce101433d8bc8414b41e86d67d8da2cf39ea19).

### TC-005

The two probe positions bracket the near face of the interaction range along X. The harness powers the room, leaves the terminal, positions the player at each point and presses E once per point. Both samples use the same player-center Y (−140 cm), Z (95 cm) and facing direction.

| Player-center X | Expected | Observed |
| --- | --- | --- |
| −2 cm | Ignore the input. | Power was on. The door remained Closed after E. |
| 0 cm | Accept the input and allow passage after opening. | One opening began at frame 31 and completed at frame 60. From the near side of the doorway, forward movement took the player past the door at X = 220 cm to X = 454.55 cm. |

The 2 cm interval brackets the change in behavior on this approach. Exact contact and the other faces of the trigger were outside this run. [Runtime evidence](runtime.txt) · [Run the five cases locally](../../../README.md#run-the-functional-regression)
