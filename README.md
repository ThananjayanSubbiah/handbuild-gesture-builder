# HandBuild ✋🧱

A rebuilt, GitHub-ready **2D** gesture-controlled block sandbox. Webcam hand tracking lets you pinch to create, select and drag blocks. Optional simplified gravity and stacking make the blocks fall and settle.

> This is a fresh reconstruction, **not** the original project source. Rotation is visual and the simplified physics uses axis-aligned collision, not a full 3D physics engine.

## Quick start

Install **Python 3.11**, connect a webcam and double-click `START.bat` on Windows. On macOS/Linux: `python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python main.py`.

## Controls

- **Pinch** thumb + index to spawn a new block, or select and drag a nearby existing block. Release to drop.
- `E`: rotate the most recently created block 15° (reliable keyboard fallback).
- `1`/`2`/`3`: choose the color of new blocks; `P`: toggle gravity and stacking; `R`: clear blocks; `Q`/`Esc`: quit.
- If camera 0 is unavailable: `python main.py --camera 1`.

## Tech
Python, OpenCV, MediaPipe, NumPy. No API key or cloud service.

## Notes
The physics solver is intentionally lightweight, supports vertical stacking, and does not implement realistic rotation collisions or full 3D objects. Webcam tracking, frame rate and MediaPipe installation need testing on your hardware.

## GitHub
Create a repository named `handbuild-gesture-builder` and upload this folder's **contents**. `.venv/` is excluded by `.gitignore`. MIT license.
