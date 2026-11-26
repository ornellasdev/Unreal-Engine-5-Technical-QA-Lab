"""Run the control-room regression cases in standalone Unreal sessions."""

import argparse
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1] / "ControlRoomLab.uproject"
DOOR = "BugItGo 104 -140 95 0 0 0"
POWER = "BugItGo -305 260 95 0 0 0"
HALL = "BugItGo 20 0 95 0 0 0"
STATE = "getall BP_DoorInteraction_C DoorState"
POSITION = "getall SphereComponent RelativeLocation"
POWER_STATE = "getall BP_DoorInteraction_C PowerOn"
CASES = range(1, 6)


def interact(frame):
    return [(frame, "Input.+key E"), (frame + 1, "Input.-key E")]


def commands(case):
    if case == 1:
        steps = [(2, DOOR), *interact(5), (9, STATE), (10, POWER_STATE), (12, HALL)]
    else:
        outside = "BugItGo -2 -140 95 0 0 0" if case == 5 else HALL
        steps = [(2, POWER), *interact(5), (10, DOOR), (14, outside),
                 *interact(17), (21, STATE), (22, POWER_STATE)]

    if case <= 2:
        steps.extend([(26, "Input.+key W"), (49, POSITION), (58, POSITION),
                      (59, "Input.-key W"), (61, "quit")])
    else:
        inside = "BugItGo 0 -140 95 0 0 0" if case == 5 else DOOR
        steps.extend([(26, inside), *interact(29), (44, STATE), (65, STATE),
                      (68, HALL), (70, "Input.+key W"), (95, POSITION),
                      (96, "Input.-key W"), (98, "quit")])
    if case == 5:
        steps.extend([(16, POSITION), (28, POSITION)])
    if case == 4:
        for frame in (36, 42, 50):
            steps.extend(interact(frame))
    return ",".join("DEFER " * frame + command for frame, command in sorted(steps))


def check(label, actual, expected):
    if actual != expected:
        raise ValueError(f"{label}: expected {expected!r}, observed {actual!r}")


def verify(case, log):
    errors = [line for line in log.splitlines() if ": Error:" in line]
    if errors:
        raise ValueError(errors[0])
    check("clean shutdown", "LogExit: Exiting." in log, True)
    states = re.findall(r"BP_DoorInteraction_C_\d+\.DoorState = (\w+)", log)
    power = re.findall(r"BP_DoorInteraction_C_\d+\.PowerOn = (\w+)", log)
    events = re.findall(
        r"\]\[\s*(\d+)\]LogBlueprintUserMessages: \[BP_DoorInteraction_C_\d+\] ([^\r\n]+)", log
    )
    samples = re.findall(
        r"DefaultPawn_\d+\.CollisionComponent0\.RelativeLocation = "
        r"\(X=([-\d.]+),Y=([-\d.]+),Z=([-\d.]+)\)", log
    )
    positions = [tuple(map(float, point)) for point in samples]

    expected_messages = ["Door offline - no power." if case == 1 else "Control room power on."]
    if case >= 3:
        expected_messages.extend(["Door opening.", "Door open."])
    check("messages", [message for _, message in events], expected_messages)
    check("power", power, ["False" if case == 1 else "True"])
    check("door states", states, ["Closed"] if case <= 2 else ["Closed", "Opening", "Open"])

    if case <= 2:
        check("blocked position samples", len(positions), 2)
        if any(abs(x - 176.55) > 1 for x, _, _ in positions):
            raise ValueError(f"closed door should stop the player near X=176.55 cm, got {positions}")
        return None
    if case == 5:
        check("terminal boundary probes (cm)", positions[:2], [(-2, -140, 95), (0, -140, 95)])
        if int(events[1][0]) < 29:
            raise ValueError("door started opening before the inside input was processed")
        positions = positions[2:]
    check("crossing position samples", len(positions), 1)
    if positions[0][0] <= 255:
        raise ValueError(f"player did not clear the door at X=220 cm: X={positions[0][0]}")
    return int(events[-1][0]) - int(events[-2][0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--editor", default=shutil.which("UnrealEditor-Cmd"),
                        help="path to UnrealEditor-Cmd (defaults to PATH)")
    args = parser.parse_args()
    if not args.editor or not os.access(args.editor, os.X_OK) or not Path(args.editor).is_file():
        parser.error("provide an executable UnrealEditor-Cmd with --editor")

    saved = PROJECT.parent / "Saved" / "QA"
    saved.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="regression-", dir=saved))
    print(f"Logs: {run_dir}", flush=True)
    passed = 0
    reference_duration = None
    for case in CASES:
        name = f"TC-{case:03}"
        log_path = run_dir / f"{name}.log"
        try:
            with (run_dir / f"{name}.stdout").open("wb") as output:
                subprocess.run(
                    [str(Path(args.editor).resolve()), str(PROJECT), "-game", "-nullrhi",
                     "-nosound", "-unattended", "-UseFixedTimeStep", "-FPS=30",
                     "-ExecCmds=" + commands(case), "-abslog=" + str(log_path)],
                    stdout=output, stderr=subprocess.STDOUT, timeout=240, check=True,
                )
            duration = verify(case, log_path.read_text(errors="replace"))
            if case == 3:
                reference_duration = duration
            if case == 4:
                check("opening duration compared with TC-003 (frames)", duration, reference_duration)
        except subprocess.CalledProcessError as error:
            print(f"{name} FAIL — Unreal exited with code {error.returncode}", flush=True)
        except subprocess.TimeoutExpired:
            print(f"{name} FAIL — Unreal exceeded the 240-second timeout", flush=True)
        except (OSError, ValueError) as error:
            print(f"{name} FAIL — {error}", flush=True)
        else:
            passed += 1
            print(f"{name} PASS", flush=True)
    print(f"{passed}/{len(CASES)} passed")
    return int(passed != len(CASES))


if __name__ == "__main__":
    raise SystemExit(main())
