# Unreal-Engine-5-Technical-QA-Lab

An Unreal Engine 5 prototype for testing Blueprint interactions, triggers, and state transitions through functional and exploratory testing.

## Play the current build

Open `ControlRoomLab.uproject` in Unreal Engine 5.9 Preview 2 and press **Play**. Use **WASD** to move and the **mouse** to look. Approach the **DOOR CONTROL** terminal and press **E**. The terminal reports `Door offline - no power.` and the closed door blocks the player. Press **E** beside **POWER** to switch the room power on. After you leave, the power stays on for the rest of the session. Pressing **E** back at **DOOR CONTROL** now reports `Door terminal online.` The door remains closed in this build.

## First scenario — Control room security door

The player starts in a control room with the power off and the security door closed. One terminal turns on the power. A second terminal controls the door. Leaving either terminal's interaction range preserves the power state. The door accepts an open command only while the player is within range of the door terminal and the power is on.

An accepted command moves the door from **Closed** to **Opening** to **Open**. Further inputs during opening have no effect. Once open, the doorway must allow the player to walk through.

## Planned functional tests

Start each case in a fresh play session. TC-001 has been checked in headless gameplay on Linux using simulated key input. The Blueprint logged the warning in range and stayed silent at spawn. With forward input held against the closed door, the player stopped at X = 176.55 cm in front of the door centered at X = 220 cm. On-screen presentation still awaits visual review.

TC-002 was also checked in a headless Linux session with simulated key input. After powering the room, the player entered and left the door terminal's range. Pressing **E** outside the range produced no terminal response, and the runtime value of `PowerOn` remained true. When the player moved forward against the door, their X position held at 176.55 cm. Returning to the door terminal and pressing **E** produced the online message.

TC-003 and TC-004 await implementation of the door's opening sequence.

| ID | Player actions | Expected result |
| --- | --- | --- |
| TC-001 | Leave the power off. Approach the door terminal and interact. | The terminal indicates that power is unavailable. The door stays closed and blocks passage. |
| TC-002 | Switch on the power. Approach the door terminal, leave its range, then press interact. | Power stays on. The open command is unavailable outside the terminal's range, and the door stays closed. |
| TC-003 | Switch on the power. Enter the door terminal's range, step out, then return and interact once. | The door begins opening, reaches Open, and lets the player walk through. |
| TC-004 | Switch on the power and activate the door terminal. Press interact several more times while the door is moving, then walk through. | The opening animation finishes once without restarting. The door stays open and the player can pass. |
