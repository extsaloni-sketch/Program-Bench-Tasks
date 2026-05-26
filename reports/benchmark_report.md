# ProgramBench Benchmark Report

## Executive summary

This report summarizes four ProgramBench task samples and their difficulty validation. The tasks are designed to test whether coding agents can reconstruct real command-line program behavior from compiled binaries, documentation/help text, and allowed fixtures.

The four evaluated tasks are:

1. `tomnomnom__gron.c29c628`
2. `chmln__sd.f8e1042`
3. `theryangeary__choose.a5d3f91`
4. `XAMPPRocky__tokei.d2c7b84`

All four tasks meet the approval rule: at least two coding agents failed each task.

## Benchmark objective

ProgramBench evaluates end-to-end program reconstruction. The agent is not given original source code or original tests. Instead, it must infer program behavior by interacting with the compiled executable and reading allowed documentation/help text.

A good ProgramBench task should test observable behavior such as:

- exact stdout and stderr
- exit codes
- file modifications
- JSON or structured output schema
- binary/raw byte behavior
- edge cases
- invalid input behavior
- mode/flag semantics
- hidden side-effect constraints

## Evaluation setup

Agents were evaluated against hidden behavioral checks. The checks were not included in the model-visible prompt.

### Model-visible input

Agents were allowed to see:

- compiled binary
- README / help text
- allowed sample fixtures

### Hidden evaluator data

Agents were not allowed to see:

- hidden checks
- expected stdout/stderr
- expected exit codes
- failure analysis
- validation notes

## Overall results

| Task | Program | GPT-4o | Claude Sonnet 4.6 | Gemini 1.5 Pro | Approval |
|---|---|---:|---:|---:|---|
| Task 001 | gron | Fail | Fail | Pass | Approved |
| Task 002 | sd | Fail | Fail | Fail | Approved |
| Task 003 | choose | Fail | Fail | Pass | Approved |
| Task 004 | tokei | Fail | Fail | Fail | Approved |

## Task 001: gron

### Program type

JSON-to-greppable-assignment CLI transformer.

### Why the task is strong

`gron` looks simple at first, but exact behavior depends on output ordering, key formatting rules, JSON primitive handling, stdin/file input, and reverse transformation through `--ungron`.

### Key hidden checks

The evaluator checks:

- flattening of flat JSON objects
- nested object flattening
- array flattening
- primitive values including null
- bracket notation for non-identifier keys
- `--ungron` reverse mode
- stdin mode
- invalid JSON behavior

### Agent failures

| Agent | Result | Main failure |
|---|---|---|
| GPT-4o | Fail | Used dot notation for all keys, missed bracket notation, wrong key order, incorrect ungron formatting |
| Claude Sonnet 4.6 | Fail | Correct bracket notation but used insertion order and failed nested ungron reconstruction |
| Gemini 1.5 Pro | Pass | Passed all checks |

### Why this validates difficulty

The failing agents guessed common JSON-flattening behavior instead of probing exact binary behavior. The key-order and bracket-notation rules are not safely inferable without running the binary.

## Task 002: sd

### Program type

Regex and fixed-string find-and-replace CLI.

### Why the task is strong

The initial behaviors were too easy for strong agents, so the task was hardened with extra checks that require probing actual `sd` behavior.

### Key hidden checks

The evaluator checks:

- literal replacement
- regex replacement
- capture groups
- fixed-string mode
- in-place editing
- multi-file editing
- no-match behavior
- newline preservation
- invalid regex
- `$0` whole-match replacement
- preview mode with no file modification
- named capture group replacement with `${name}` syntax

### Agent failures

| Agent | Result | Main failure |
|---|---|---|
| GPT-4o | Fail | `$0` emitted null byte; named capture syntax not recognized |
| Claude Sonnet 4.6 | Fail | Named capture replacement syntax not handled |
| Gemini 1.5 Pro | Fail | Preview mode still modified the file |

### Why this validates difficulty

The failures show that agents can pass common sed-like behavior but still fail on program-specific semantics such as `$0`, `${name}`, and preview no-modify behavior.

## Task 003: choose

### Program type

Field-selection CLI tool.

### Why the task is strong

`choose` has a simple interface but tricky semantics: zero-based indexing, inclusive ranges, negative indexes, delimiter flags, argument-order output, and whitespace collapsing.

### Key hidden checks

The evaluator checks:

- single-field selection
- multiple-field selection
- inclusive ranges
- negative indexing
- custom input separator
- custom output separator
- multi-line processing
- whitespace collapsing
- out-of-range behavior

### Agent failures

| Agent | Result | Main failure |
|---|---|---|
| GPT-4o | Fail | No range support, no negative index support, no delimiter flag support, wrong whitespace handling |
| Claude Sonnet 4.6 | Fail | Implemented range end as exclusive instead of inclusive |
| Gemini 1.5 Pro | Pass | Passed all checks |

### Why this validates difficulty

The task exposes common training-language bias. Claude used Python slice semantics, but the binary uses inclusive range semantics. GPT-4o implemented a naive split/index approach and missed core CLI features.

## Task 004: tokei

### Program type

Source code line-counting CLI.

### Why the task is strong

`tokei` requires exact per-language counting behavior, JSON schema reconstruction, docstring classification, filtering, exclusion, and edge-case handling.

### Key hidden checks

The evaluator checks:

- Python code/comment/blank counts
- docstring-as-comment behavior
- multi-language aggregation
- exact JSON output schema
- language type filtering
- glob exclusion
- empty file behavior
- unknown extension behavior

### Agent failures

| Agent | Result | Main failure |
|---|---|---|
| GPT-4o | Fail | Counted Python docstrings as code; wrong JSON field names |
| Claude Sonnet 4.6 | Fail | JSON output missing required fields |
| Gemini 1.5 Pro | Fail | Empty file skipped; JSON output missing required field |

### Why this validates difficulty

All three agents failed the JSON schema check. This confirms that agents cannot simply guess a reasonable JSON structure. They must probe the binary and reproduce tool-specific fields such as `inaccurate`, `reports`, and `blobs`.

## Cross-task failure patterns

### 1. Training-language bias

Agents often used familiar conventions from Python, sed, or common CLI tools instead of the target binary’s actual behavior.

Examples:
- `choose` range implemented as Python-style exclusive end
- `sd` replacement syntax confused with sed/Python syntax
- `gron` non-identifier keys flattened with dot notation

### 2. Schema guessing

Agents guessed JSON output structures instead of discovering them.

Examples:
- `tokei` missing `inaccurate`, `reports`, and `blobs`
- incorrect field names such as `total_lines`

### 3. Edge-case omission

Agents handled happy paths but failed on edge cases.

Examples:
- empty file handling
- out-of-range field selection
- invalid input behavior
- preview mode file side effects
- special-key formatting

### 4. Mode semantics misunderstood

Agents detected a flag but implemented the wrong behavior.

Examples:
- `sd --preview` produced diff output but still modified the file
- `gron --ungron` handled only flat paths
- `sd` named capture replacement syntax not implemented

## Final verdict

All four tasks are valid ProgramBench tasks and meet the difficulty approval rule.

| Task | Approval basis |
|---|---|
| gron | 2 of 3 agents failed |
| sd | 3 of 3 agents failed |
| choose | 2 of 3 agents failed |
| tokei | 3 of 3 agents failed |

## Recommended status

`approved_after_difficulty_validation`

## Final recommendation

These tasks are ready to share for review and can be pushed to GitHub alongside the task definitions and difficulty-validation file. The repository should remain private if it includes hidden checks, expected outputs, or detailed failure analysis.
