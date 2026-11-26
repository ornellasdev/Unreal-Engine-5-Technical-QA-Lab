# Unreal Engine 5 Technical QA Lab

An Unreal Engine 5 prototype for testing Blueprint interactions, triggers, and state transitions through functional and exploratory testing.

## Play the current build

Open `ControlRoomLab.uproject` in Unreal Engine 5.9 Preview 2 and press **Play**. Use **WASD** to move and the **mouse** to look. Approach the **DOOR CONTROL** terminal and press **E**. The terminal displays **OFFLINE - NO POWER** and the closed door blocks the player. Press **E** beside **POWER** to switch the room power on. After you leave, the power stays on for the rest of the session. Return to **DOOR CONTROL** and press **E**. The door rises over one second. Once it is open, walk through the doorway.

## First scenario — Control room security door

The player starts in a control room with the power off and the security door closed. One terminal turns on the power. A second terminal controls the door. Leaving either terminal's interaction range preserves the power state. The door accepts an open command only while the player is within range of the door terminal and the power is on.

An accepted command moves the door from **Closed** to **Opening** to **Open**. Further inputs during opening have no effect. Once open, the doorway must allow the player to walk through.

## Functional tests

Start each case in a fresh play session. The first four cases cover door behavior and collision. TC-005 checks the edge of the terminal's interaction range. TC-006 checks collision while the panel rises.

| ID | Player actions | Expected result |
| --- | --- | --- |
| TC-001 | Leave the power off. Approach the door terminal and interact. | The terminal indicates that power is unavailable. The door stays closed and blocks passage. |
| TC-002 | Switch on the power. Approach the door terminal, leave its range, then press interact. | Power stays on. The open command is unavailable outside the terminal's range, and the door stays closed. |
| TC-003 | Switch on the power. Enter the door terminal's range, step out, then return and interact once. | The door begins opening, reaches Open, and lets the player walk through. |
| TC-004 | Switch on the power and activate the door terminal. Press interact several more times while the door is moving, then walk through. | The opening animation finishes once without restarting. The door stays open and the player can pass. |
| TC-005 | Power the room. With the player centered at Y = −140 cm and Z = 95 cm, press E at X = −2 cm, then again at X = 0 cm. | The outside input leaves the door closed. The inside input starts one opening and the player can pass. |
| TC-006 | Power the room, hold W against the door and press E at the edge of the terminal zone. Keep W held as the panel lifts. | The low panel blocks movement. As clearance increases, the player passes underneath without needing to release W. |

### Run the functional regression

From the repository root, run the following command with Python 3 and your local Unreal Engine 5.9 Preview 2 Linux editor binary. If `UnrealEditor-Cmd` is on your PATH, omit `--editor` and its value.

```bash
python3 qa/run_functional.py --editor "/path/to/Engine/Binaries/Linux/UnrealEditor-Cmd"
```

The runner starts one headless game per case and checks Blueprint messages, power, door transitions and player collision. It prints a result for each case and returns a nonzero exit code on failure. Each execution keeps its Unreal logs in a new directory under `Saved/QA/`. For the rendered readability check, see the [RUN-002 screenshots](qa/runs/RUN-002/README.md).

## Test runs and evidence

| Run | Question | Result |
| --- | --- | --- |
| [RUN-001 · Gameplay baseline](qa/runs/RUN-001/README.md) | Do power, range, repeated input and door collision work as specified? | Four functional cases passed. The gameplay clip revealed poor contrast at the terminals and door. |
| [RUN-002 · Visual retest](qa/runs/RUN-002/README.md) | Can the player distinguish the closed door and read the terminal feedback? | Player-view captures verified the fix. All four functional cases passed again. |
| [RUN-003 · Exploratory testing](qa/runs/RUN-003/README.md) | Do terminal feedback, door motion and collision stay consistent across re-entry and a new session? | The door opened once despite repeated input. A fresh session restored the starting prompts, power state and blocked passage. |
| [RUN-004 · Repeatable regression](qa/runs/RUN-004/README.md) | Can one local command run and check all four cases? | Four fresh Unreal processes completed and all four cases passed. |
| [RUN-005 · Terminal range boundary](qa/runs/RUN-005/README.md) | Does moving the player center 2 cm across the trigger boundary change the result of pressing E? | The outside input left the door closed. The inside input opened it. All five cases passed locally. |
| [RUN-006 · Moving door collision](qa/runs/RUN-006/README.md) | What happens when the player keeps pushing against the panel as it lifts? | The player cleared the moving door before opening finished. All six cases passed locally. |
