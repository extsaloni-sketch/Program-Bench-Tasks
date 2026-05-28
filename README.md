# Program-Bench Task Validation Repository

This repository organizes ProgramBench task candidates with validation evidence from multiple coding-agent evaluations.

The goal is to make each task easy to inspect, reproduce, and review by ML researchers working on coding-agent benchmarking, task difficulty analysis, and hidden-test robustness.

## Included Tasks

| Task | Official ProgramBench Task | Agent Validation |
|---|---|---|
| hashcards | eudoxia0__hashcards.48aa136 | 6 agents evaluated, 4 failed |
| BLAKE3 | blake3-team__blake3.15e83a5 | 5 agents evaluated, 2 failed |
| ripgrep | burntsushi__ripgrep.3b7fd44 | 6 agents evaluated, 6 failed |
| parallel-disk-usage | ksxgithub__parallel-disk-usage.96978ed | 6 agents evaluated, 4 failed |
| zstd | facebook__zstd.1168da0 | 6 agents evaluated, 5 failed |

## Repository Structure

```text
tasks/
  <task-name>/
    README.md
    task_metadata.json
    agent_evaluations.md

reports/
  validation_report.txt

scripts/
  validate_repo_structure.py

Add detailed per-task metadata:

```bash
cat > tasks/hashcards/task_metadata.json <<'EOF'
{
  "task_name": "hashcards",
  "official_task_id": "eudoxia0__hashcards.48aa136",
  "official_task_path": "src/programbench/data/tasks/eudoxia0__hashcards.48aa136",
  "official_url": "https://github.com/facebookresearch/ProgramBench/tree/main/src/programbench/data/tasks/eudoxia0__hashcards.48aa136",
  "agents_evaluated": 6,
  "agents_failed": 4,
  "validation_status": "validated",
  "inclusion_reason": "At least two independent coding agents failed or produced incomplete solutions under hidden ProgramBench evaluation."
}
