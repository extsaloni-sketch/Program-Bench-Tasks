from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TASKS = {
    "hashcards",
    "blake3",
    "ripgrep",
    "parallel-disk-usage",
    "zstd",
}

REQUIRED_ROOT_FILES = [
    "README.md",
    "DATASET_CARD.md",
    "METHODOLOGY.md",
    "TASK_INDEX.md",
]

REQUIRED_TASK_FILES = [
    "README.md",
    "task_metadata.json",
    "agent_evaluations.md",
]

ok = True

print("Checking root files...")
for file_name in REQUIRED_ROOT_FILES:
    path = ROOT / file_name
    if not path.exists():
        print(f"  MISSING: {file_name}")
        ok = False

tasks_dir = ROOT / "tasks"
found_tasks = {p.name for p in tasks_dir.iterdir() if p.is_dir()}

if found_tasks != EXPECTED_TASKS:
    print("Task folder mismatch")
    print("  Expected:", sorted(EXPECTED_TASKS))
    print("  Found:", sorted(found_tasks))
    ok = False

print("\nChecking task folders...")
for task in sorted(EXPECTED_TASKS):
    task_dir = tasks_dir / task
    print(f"  {task}")

    for file_name in REQUIRED_TASK_FILES:
        path = task_dir / file_name
        if not path.exists():
            print(f"    MISSING: {file_name}")
            ok = False

    metadata_path = task_dir / "task_metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text())
            required_keys = [
                "task_name",
                "official_task_id",
                "agents_evaluated",
                "agents_failed",
                "validation_status",
            ]
            for key in required_keys:
                if key not in metadata:
                    print(f"    MISSING metadata key: {key}")
                    ok = False
        except Exception as exc:
            print(f"    INVALID JSON: {exc}")
            ok = False

report_path = ROOT / "reports" / "validation_report.txt"
if not report_path.exists():
    print("\nMISSING: reports/validation_report.txt")
    ok = False

if not ok:
    raise SystemExit(1)

print("\nRepository structure is valid.")
