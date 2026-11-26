# RUN-003 — Terminal re-entry and session reset

**Charter.** Try to make the two terminal displays disagree with the room's power, the moving door or the player's ability to cross the doorway. Two local standalone sessions ran on Linux on November 25, 2026, using Unreal Engine 5.9.0 Preview 2 at 30 simulated frames per second. [Tested revision](https://github.com/ornellasdev/Unreal-Engine-5-Technical-QA-Lab/commit/2dd415b59243a7cf4e2cb714648e91572135e6c7)

| Probe | Player actions | Observed |
| --- | --- | --- |
| Recover from an offline attempt | Use the door terminal first. Visit the power terminal and press E twice. | The door display changed from OFFLINE - NO POWER to [E] OPEN DOOR. The power display read POWER ON. The door stayed closed at Z = 120 cm. |
| Leave during motion | Start opening, leave the trigger, press E outside, then return and press E while the door is rising. | The display read OPENING at both samples. Door height rose from 203.33 to 311.67 cm. A single opening event at frame 27 was followed by a single completion at frame 56. |
| Interact after completion | Press E again at the door terminal after it reads OPEN. Move forward from X = 20 cm. | The panel remained at Z = 370 cm and the display stayed OPEN. The player crossed the door plane at X = 220 cm and reached X = 454.55 cm. |
| Start a new session | Exit the first game. Launch the same map in a new process, try the door without power and hold forward against it. | The room started with power off, the panel at Z = 120 cm and both interaction prompts restored. The door reported OFFLINE - NO POWER and stopped the player at X = 176.55 cm on two successive samples. |

**Outcome.** No mismatch was observed in these sequences. The harness repositioned the player at the terminals, issued key inputs and sampled the text components, Blueprint state and actor positions. Collision was checked by moving forward against the closed and open door. These sessions ran with rendering disabled. [Runtime evidence](runtime.txt) · [Rendered terminal states from RUN-002](../RUN-002/player-view.jpg)
