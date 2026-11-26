"""Replay TC-006 at three fixed simulation rates and measure the moving contact."""

import argparse
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from run_functional import MOTION_FRAMES, POSITION, PROJECT, check, moving_door_steps, verify

PANEL_POSITIONS = "getall StaticMeshComponent RelativeLocation"
FRAME = r"\]\[\s*(\d+)\]"
XYZ = r"\(X=([-\d.]+),Y=([-\d.]+),Z=([-\d.]+)\)"


def measure(log, fps):
    scale = fps // 30
    panels = re.findall(r"\.DoorPanel = [^\n]*?PersistentLevel\.(\w+)", log)
    check("assigned panel count", len(panels), 1)
    player_component = "DefaultPawn_" + r"\d+\.CollisionComponent0"
    door_component = re.escape(panels[0]) + r"\.StaticMeshComponent0"
    frames = list(range(20 * scale, 62 * scale + 1))

    def positions(component):
        rows = re.findall(FRAME + r"[^\n]*PersistentLevel\." + component +
                          r"\.RelativeLocation = " + XYZ, log)
        check("sample frames", [int(row[0]) for row in rows], frames)
        return [tuple(map(float, row[1:])) for row in rows]

    player = positions(player_component)
    panel = positions(door_component)
    # Reuse TC-006's state, input and collision checks at the original sampling times.
    checkpoints = {frame * scale for frame in MOTION_FRAMES}
    lines = []
    for line in log.splitlines():
        if ".RelativeLocation = " in line:
            match = re.search(FRAME, line)
            if match and int(match[1]) not in checkpoints:
                continue
        lines.append(line)
    verify(6, "\n".join(lines))

    events = re.findall(FRAME + r"LogBlueprintUserMessages: \[BP_DoorInteraction_C_\d+\] Door (opening|open)\.", log)
    start, end = [int(frame) for frame, _ in events]
    if abs((end - start) - fps) > 1:
        raise ValueError(f"opening exceeded one frame of timing tolerance: {end - start} frames at {fps} fps")
    gaps = []
    evidence = ["frame  player_x_cm  player_y_cm  player_z_cm  panel_z_cm  surface_gap_cm"]
    for frame, (x, y, z), (door_x, door_y, door_z) in zip(frames, player, panel):
        dx = max(abs(x - door_x) - 8, 0)
        dy = max(abs(y - door_y) - 80, 0)
        dz = max(abs(z - door_z) - 120, 0)
        gap = math.sqrt(dx * dx + dy * dy + dz * dz) - 35
        gaps.append(gap)
        evidence.append(f"{frame:5} {x:12.5f} {y:12.5f} {z:12.5f} {door_z:11.5f} {gap:15.5f}")
        if gap < -1:
            raise ValueError(f"panel penetration at frame {frame}: {-gap:.3f} cm")
    crossed = next(frame for frame, point in zip(frames, player) if point[0] > 220)
    cleared = next(frame for frame, point in zip(frames, player) if point[0] > 263)
    return start, end, crossed, cleared, min(gaps), evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--editor", default=shutil.which("UnrealEditor-Cmd"))
    args = parser.parse_args()
    if not args.editor or not Path(args.editor).is_file():
        parser.error("supply the path to UnrealEditor-Cmd with --editor")
    parent = PROJECT.parent / "Saved" / "QA"
    parent.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix="collision-rates-", dir=parent))
    print(f"Logs and per-frame measurements: {output}", flush=True)
    failed = False
    for fps in (30, 60, 120):
        scale = fps // 30
        steps = [(frame * scale, cmd) for frame, cmd in moving_door_steps()
                 if cmd not in (POSITION, PANEL_POSITIONS)]
        for frame in range(20 * scale, 62 * scale + 1):
            steps.extend([(frame, POSITION), (frame, PANEL_POSITIONS)])
        # Unreal's exec macro path resolver recognizes paths containing "Binaries".
        macro = tempfile.NamedTemporaryFile(mode="w", prefix="qa-Binaries-", suffix=".txt",
                                            dir="/tmp", delete=False)
        with macro:
            macro.writelines("DEFER " * frame + cmd + "\n" for frame, cmd in sorted(steps))
        log = output / f"{fps}.log"
        try:
            with (output / f"{fps}.stdout").open("wb") as stdout:
                subprocess.run([str(Path(args.editor).resolve()), str(PROJECT), "-game", "-nullrhi",
                                "-nosound", "-unattended", "-UseFixedTimeStep", f"-FPS={fps}",
                                f"-ExecCmds=exec {macro.name}", f"-abslog={log}"],
                               stdout=stdout, stderr=subprocess.STDOUT, timeout=120, check=True)
            start, end, crossed, cleared, gap, rows = measure(log.read_text(errors="replace"), fps)
            summary = (f"{fps} fps | opening frames {start} to {end} ({(end-start)/fps:.4f} s) | "
                       f"center crossed at {crossed} (+{(crossed-start)/fps:.4f} s) | "
                       f"fully clear at {cleared} (+{(cleared-start)/fps:.4f} s) | min gap {gap:.4f} cm")
            (output / f"{fps}.txt").write_text(summary + "\n" + "\n".join(rows) + "\n")
            print("PASS", summary, flush=True)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            print(f"FAIL {fps} fps: {error}", flush=True)
            failed = True
        finally:
            Path(macro.name).unlink(missing_ok=True)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
