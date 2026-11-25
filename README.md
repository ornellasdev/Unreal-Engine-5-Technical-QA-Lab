# Unreal-Engine-5-Technical-QA-Lab

A planned Unreal Engine 5 prototype for testing Blueprint interactions, triggers, and state transitions through functional and exploratory testing.

## First scenario — Control room security door

The player starts in a control room with the power off and the security door closed. One terminal turns on the power. A second terminal controls the door. Leaving either terminal's interaction range preserves the power state. The door accepts an open command only while the player is within range of the door terminal and the power is on.

An accepted command moves the door from **Closed** to **Opening** to **Open**. Further inputs during opening have no effect. Once open, the doorway must allow the player to walk through.

## Planned functional tests

Start each case in a fresh play session. All four cases await implementation and execution.

| ID | Player actions | Expected result |
| --- | --- | --- |
| TC-001 | Leave the power off. Approach the door terminal and interact. | The terminal indicates that power is unavailable. The door stays closed and blocks passage. |
| TC-002 | Switch on the power. Approach the door terminal, leave its range, then press interact. | Power stays on. The open command is unavailable outside the terminal's range, and the door stays closed. |
| TC-003 | Switch on the power. Enter the door terminal's range, step out, then return and interact once. | The door begins opening, reaches Open, and lets the player walk through. |
| TC-004 | Switch on the power and activate the door terminal. Press interact several more times while the door is moving, then walk through. | The opening animation finishes once without restarting. The door stays open and the player can pass. |
