# Validation Methodology

## Evaluation Setup

Each task is evaluated using multiple coding agents. Agents are given only model-visible task artifacts, such as compiled binaries, README/help text, and allowed fixtures.

Hidden tests, expected outputs, official test names, source code, and tests.json are not provided to agents.

## Review Criterion

A task is considered suitable for inclusion if at least two independent coding agents fail or produce incomplete solutions under hidden ProgramBench evaluation.

## Why Multi-Agent Validation Matters

Single-agent failure is not enough to establish difficulty. Multi-agent validation helps identify tasks that expose broader limitations in coding-agent behavior, such as:

- incomplete CLI reconstruction,
- weak edge-case handling,
- poor output-format matching,
- fragile build compatibility,
- insufficient behavioral generalization.

## Reported Fields

Each task records:

- official ProgramBench task identifier,
- number of agents evaluated,
- number of agents failed,
- ProgramBench scores where available,
- short failure reasons,
- missing behaviors or reasoning gaps.

## Limitations

The repository summarizes validation evidence but does not include hidden tests or private expected outputs.
