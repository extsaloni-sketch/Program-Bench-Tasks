# ProgramBench Validation Summary

## Validation rule

A task is approved if at least two coding agents fail the hidden behavioral checks.

## Evaluated agents

- GPT-4o
- Claude Sonnet 4.6
- Gemini 1.5 Pro

## Results

| Task | Source | GPT-4o | Claude Sonnet 4.6 | Gemini 1.5 Pro | Approval |
|---|---|---|---|---|---|
| Task 001 | tomnomnom__gron.c29c628 | Fail | Fail | Pass | Approved |
| Task 002 | chmln__sd.f8e1042 | Fail | Fail | Fail | Approved |
| Task 003 | theryangeary__choose.a5d3f91 | Fail | Fail | Pass | Approved |
| Task 004 | XAMPPRocky__tokei.d2c7b84 | Fail | Fail | Fail | Approved |

## Approval summary

All four tasks satisfy the difficulty requirement.

## Notes

The task definitions and hidden evaluator checks should be kept separate from the model-visible prompt. If this repository is public, remove hidden expected outputs and detailed failure analysis before publishing.
