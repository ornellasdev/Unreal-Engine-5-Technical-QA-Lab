# RUN-001 — Control room security door

**Result:** 4 of 4 functional cases passed on November 25, 2026.

**Build:** [f9c5d85](https://github.com/ornellasdev/Unreal-Engine-5-Technical-QA-Lab/commit/f9c5d853db169e359626f05fd0f29d1ce0a5f5f5), Unreal Engine 5.9.0 Preview 2, Linux, standalone game mode launched from the editor binary. Each case used a fresh process at 30 simulated frames per second with rendering disabled.

| Case | Expected | Observed |
| --- | --- | --- |
| TC-001 · Unpowered door | The terminal warns the player and the door blocks movement. | Interacting beside the terminal logged `Door offline - no power.` The door remained Closed. With forward input held, the player stopped at X = 176.55 cm on both samples. |
| TC-002 · Out of range | Power persists after leaving the terminal. An outside interaction leaves the door closed. | After leaving the door terminal and pressing E, no door message appeared. The state was Closed, power was true, and the player stopped at X = 176.55 cm. |
| TC-003 · Return and open | One interaction after returning opens the door and allows passage. | The state progressed from Closed to Opening to Open. Forward movement took the player beyond the door plane at X = 220 cm to X = 454.55 cm. |
| TC-004 · Repeated input | Additional presses during opening neither restart the motion nor block passage. | Three additional presses produced a single opening message and a single completion. Completion occurred on frame 60 in both TC-003 and TC-004. The player crossed to X = 454.55 cm. |

### Reproduction and evidence

Open the tested revision and follow the [case steps](../../../README.md#functional-tests) in a fresh play session for each row. In the recorded runs, the harness positioned the player at each interaction point, simulated E for interaction, and held W to test collision. Every crossing measurement began at X = 20 cm on the near side. [Selected runtime observations](runtime.txt)

### Visual review

A separate Vulkan run captured the unpowered interaction, power activation, door opening, and passage from the player's view. The clip samples gameplay at 10 fps. Captions identify the actions, and camera cuts reposition the player between test points. [Gameplay video · 6 seconds](control-room.mp4)

**Open finding — low contrast at the door and terminals.** From the door terminal, the closed panel blends into the bright surround. Both terminal labels are difficult to read from the captured interaction points. The offline warning was verified in the runtime log. Its on-screen legibility remains unverified. To retest, approach each terminal from spawn and check whether its label, the closed panel's edges, and the interaction feedback are readable before and after pressing E.
