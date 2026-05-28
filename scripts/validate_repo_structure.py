from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
tasks_dir = root / "tasks"

required_files = ["README.md", "task_metadata.json", "agent_evaluations.md"]

ok = True

for task_dir in sorted(tasks_dir.iterdir()):
    if not task_dir.is_dir():
        continue

    print(f"Checking {task_dir.name}")

    for f in required_files:
        path = task_dir / f
        if not path.exists():
            print(f"  MISSING: {f}")
            ok = False

    metadata_path = task_dir / "task_metadata.json"
    if metadata_path.exists():
        try:
            json.loads(metadata_path.read_text())
        except Exception as e:
            print(f"  INVALID JSON: {e}")
            ok = False

if not ok:
    raise SystemExit(1)

print("All task folders look valid.")
