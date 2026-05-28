# Program-Bench Task Validation Repository

This repository organizes ProgramBench task candidates with structured validation evidence from multi-agent coding evaluations.

The goal is to make task curation transparent, reproducible, and easy to review for ML researchers working on coding-agent benchmarking, hidden-test robustness, and task difficulty analysis.

## Overview

ProgramBench tasks evaluate whether coding agents can reconstruct executable behavior from model-visible artifacts such as compiled binaries, README/help text, and allowed fixtures. This repository focuses on task-level validation evidence: which agents were evaluated, how many failed, what failure modes were observed, and why the task is useful for benchmark inclusion.

## Included Tasks

| Task | Official ProgramBench Task | Agents Evaluated | Agents Failed | Status |
|---|---|---:|---:|---|
| hashcards | `eudoxia0__hashcards.48aa136` | 6 | 4 | Validated |
| BLAKE3 | `blake3-team__blake3.15e83a5` | 5 | 2 | Validated |
| ripgrep | `burntsushi__ripgrep.3b7fd44` | 6 | 6 | Validated |
| parallel-disk-usage | `ksxgithub__parallel-disk-usage.96978ed` | 6 | 4 | Validated |
| zstd | `facebook__zstd.1168da0` | 6 | 5 | Validated |

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
python3 scripts/validate_repo_structure.py

Now add a stronger `DATASET_CARD.md`:

```bash
cat > DATASET_CARD.md <<'EOF'
# Dataset Card: ProgramBench Validated Task Set

## Dataset Summary

This repository contains a curated set of ProgramBench task candidates validated through multi-agent coding evaluations. Each task includes metadata and per-agent failure summaries to support benchmark review and reproducibility.

## Task Selection Criteria

A task is included when:

- it has been evaluated by multiple independent coding agents,
- agents were only given model-visible inputs,
- hidden ProgramBench checks were run privately,
- at least two agents failed or produced incomplete solutions.

## Included Tasks

| Task | Agents Evaluated | Agents Failed | Failure Rate |
|---|---:|---:|---:|
| hashcards | 6 | 4 | 66.7% |
| BLAKE3 | 5 | 2 | 40.0% |
| ripgrep | 6 | 6 | 100.0% |
| parallel-disk-usage | 6 | 4 | 66.7% |
| zstd | 6 | 5 | 83.3% |

## Intended Use

This task set is intended for:

- coding-agent benchmark curation,
- model robustness analysis,
- failure-mode analysis,
- task difficulty estimation,
- research on executable program reconstruction.

## Not Intended For

This repository does not expose hidden tests, official expected outputs, or private ProgramBench evaluation internals.

## Evaluation Notes

The reported scores summarize agent outcomes under hidden ProgramBench checks. They should be interpreted as task-difficulty signals, not as complete public benchmark results.
