# ProgramBench Task Evaluation Report

This repository contains four ProgramBench task samples, their difficulty validation, and a readable benchmark report summarizing why the tasks are suitable for approval.

## What is included

```text
.
├── README.md
├── reports/
│   └── benchmark_report.md
├── tasks/
│   └── programbench_tasks_24_05_26_rework_1.md
├── evaluation/
│   └── programbench_difficulty_validation.md
└── validation/
    └── validation_summary.md
```

## Task set

| Task ID | Program | Source | Language | Practical Complexity | Approval Status |
|---|---|---|---|---|---|
| Task 001 | gron | tomnomnom__gron.c29c628 | Go | High | Approved |
| Task 002 | sd | chmln__sd.f8e1042 | Rust | High | Approved |
| Task 003 | choose | theryangeary__choose.a5d3f91 | Rust | High | Approved |
| Task 004 | tokei | XAMPPRocky__tokei.d2c7b84 | Rust | High | Approved |

## Approval rule

A task is considered strong enough if at least two coding agents fail the hidden behavioral checks.

All four tasks satisfy this rule:

| Task | GPT-4o | Claude Sonnet 4.6 | Gemini 1.5 Pro | Result |
|---|---|---|---|---|
| gron | Fail | Fail | Pass | Approved |
| sd | Fail | Fail | Fail | Approved |
| choose | Fail | Fail | Pass | Approved |
| tokei | Fail | Fail | Fail | Approved |

## Important privacy note

Keep this repository private if it contains hidden checks, expected outputs, model failure details, or evaluator-only notes.

The model-visible task prompt should include only:
- compiled binary
- README / help text
- allowed fixtures

The agent should not see:
- hidden checks
- expected outputs
- failure analysis
- evaluator notes
- validation summary

## Recommended review flow

1. Review `tasks/programbench_tasks_24_05_26_rework_1.md`.
2. Review `evaluation/programbench_difficulty_validation.md`.
3. Review `reports/benchmark_report.md`.
4. Confirm that hidden checks are not exposed to the coding agents during evaluation.
5. Keep the repository private if it includes internal validation details.
