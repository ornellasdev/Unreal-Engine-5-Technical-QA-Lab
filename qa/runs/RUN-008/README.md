# RUN-008 — Unpowered door in Unreal Automation

**1 native Blueprint functional test passed** on Linux in Unreal Engine 5.9 Preview 2. The Automation Framework discovered `Project.Functional Tests.Maps.ControlRoom.UnpoweredDoor` and reported **Success**, with zero warnings and zero errors for the test. [Selected fields from the exported Automation report](automation-result.json)

The [test Blueprint](../../../Content/Tests/BP_FT_UnpoweredDoor.uasset) inherits from Functional Test and is placed in the playable ControlRoom map. Its Terminal reference points to the same interaction actor used during normal play.

1. On test start, teleport the player pawn to the terminal and allow overlaps to update. Check that power is off and the door display does not already show the expected warning.
2. Press and release E through the game's input system. Wait past the one-second opening duration.
3. Read the terminal's Text Render component and the door's Blueprint state. Finish with Success only if the text is **OFFLINE - NO POWER** and the state is **Closed**. A failed check reports its reason.

This test reads the in-world message in an editor automation session with rendering disabled. [RUN-002](../RUN-002/README.md) covers visual readability, and the local gameplay runner checks physical passage.

### Reproduce

In the editor, open **Session Frontend → Automation**, find **UnpoweredDoor**, select it and run it. Alternatively, use this command from the repository root on Linux:

```bash
"/path/to/Engine/Binaries/Linux/UnrealEditor-Cmd" "$PWD/ControlRoomLab.uproject" \
  -unattended -nullrhi -nosound -nop4 \
  -ExecCmds="Automation RunTests Project.Functional Tests.Maps.ControlRoom.UnpoweredDoor;Quit" \
  -TestExit="Automation Test Queue Empty" -ReportExportPath="$PWD/Saved/QA/NativeDoor"
```

Open the exported `index.json` and check the full test path, result and event message. [Epic's Functional Testing guide](https://dev.epicgames.com/documentation/unreal-engine/functional-testing-in-unreal-engine)
