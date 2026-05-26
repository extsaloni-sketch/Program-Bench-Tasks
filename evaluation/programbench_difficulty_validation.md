# ProgramBench — Difficulty Validation Summary

---

## Task 001 — `tomnomnom__gron.c29c628`

| Agent | Result | Checks Passed | Primary Failure |
|---|---|---|---|
| GPT-4o | **FAIL** | 3 / 8 | Used dot notation for all keys (missed bracket-notation rule for special chars); insertion-order output instead of sorted; `--ungron` produced pretty-printed JSON instead of compact single-line |
| Claude Sonnet 4.6 | **FAIL** | 5 / 8 | Correct bracket notation, but insertion-order output instead of alphabetical sort; `--ungron` could not reconstruct nested paths (only handled flat `json.key` patterns) |
| Gemini 1.5 Pro | **PASS** | 8 / 8 | — |

**Verdict: APPROVED (2 / 3 agents failed)**

**Failure analysis:**

GPT-4o and Claude Sonnet both failed because the exact output rules of `gron` — alphabetical key ordering and the bracket-notation rule (`json["foo.bar"]` vs `json.foo`) — cannot be guessed from README text alone. They must be discovered by running the binary with inputs that contain non-identifier keys and observing the output format. This is exactly what ProgramBench tests: the ability to derive specification from executable behavior.

The `--ungron` reverse mode added a second axis of failure: agents had to infer not just the output format but also the inverse parsing path. GPT-4o's ungron regex matched only flat paths and its output was pretty-printed; Claude Sonnet's regex could not handle nested or array paths. Only Gemini probed enough edge cases to fully reconstruct both directions.

**Checks that caused failures:**

- `B1` / `B3` / `B4` — Sorted key order: agents used insertion order. Requires binary probing with objects whose insertion order differs from alphabetical order.
- `B5` — Bracket notation for `{"foo.bar": 1}`: GPT-4o emitted `json.foo.bar = 1;` (invalid and wrong). Must be discovered by running the binary.
- `B6` — `--ungron` compact output: GPT-4o emitted multi-line pretty-printed JSON. Claude Sonnet failed to reconstruct nested paths.

---

## Task 002 — `chmln__sd.f8e1042`

> **Note:** Initial check suite (B1–B9 covering literal replacement, regex, capture groups, fixed-string mode, in-place editing, multi-file editing, no-match behavior, newline preservation, invalid regex) was passed by all three agents. The task was hardened with three additional behaviors (B10–B12) that require binary probing and cannot be inferred from basic usage:
> - **B10:** `$0` refers to the whole match
> - **B11:** `--preview` / `-p` mode shows a diff without modifying the file
> - **B12:** `${name}` named capture group syntax in replacements

| Agent | Result | Checks Passed | Primary Failure |
|---|---|---|---|
| GPT-4o | **FAIL** | 13 / 15 | `$0` whole-match reference emitted null byte (`\x00`) instead of matched text; named capture group `${name}` syntax not recognized |
| Claude Sonnet 4.6 | **FAIL** | 14 / 15 | Named capture group `${name}` syntax not handled; agent only implemented numbered `$1` `$2` groups |
| Gemini 1.5 Pro | **FAIL** | 14 / 15 | Preview mode (`-p`) still wrote the modified content to file, violating the no-modify contract |

**Verdict: APPROVED (3 / 3 agents failed)**

**Failure analysis:**

The core behaviors (regex replacement, capture groups, in-place editing, fixed-string mode) are well-known enough that all three agents passed B1–B9 without difficulty. This confirmed that the initial task was too easy and needed hardening.

The hardened checks exposed three behaviors that agents can only discover by running the binary:

`$0` whole-match syntax: GPT-4o assumed `$0` maps to `\0` (the null capture group in Python's `re` module), producing a null byte in output. Only agents that explicitly probe `sd` with a `$0` replacement discover this is the whole-match reference.

`${name}` named capture groups: Agents familiar with Python regex syntax write `(?P<name>...)` patterns and use `\g<name>` in replacements. `sd` uses `(?P<name>...)` for capture but `${name}` in the replacement, not `\g<name>` or `(?P=name)`. This is a Rust regex crate convention that must be inferred from binary probing.

`--preview` no-modify contract: Gemini's implementation showed the diff on stdout but also wrote the modified file to disk. The preview mode must leave the file exactly as it was — behavior that only emerges from running the binary and checking file state afterward.

**Checks that caused failures:**

- `B10` — `$0` whole-match: GPT-4o emitted `\x00` instead of the matched token.
- `B11` — Preview mode file unchanged: Gemini wrote the file despite preview mode.
- `B12` — Named capture `${name}`: GPT-4o and Claude Sonnet did not implement this syntax.

---

## Task 003 — `theryangeary__choose.a5d3f91`

| Agent | Result | Checks Passed | Primary Failure |
|---|---|---|---|
| GPT-4o | **FAIL** | 6 / 11 | No range syntax support; no negative index support; no `-f` / `-o` flag support; tab characters not collapsed with spaces |
| Claude Sonnet 4.6 | **FAIL** | 10 / 11 | Range end was exclusive instead of inclusive (`1:3` returned `beta gamma` instead of `beta gamma delta`) |
| Gemini 1.5 Pro | **PASS** | 11 / 11 | — |

**Verdict: APPROVED (2 / 3 agents failed)**

**Failure analysis:**

`choose` has a deceptively simple interface that hides several non-trivial behaviors. GPT-4o's implementation — a direct `split(" ")` followed by integer indexing — failed on four independent dimensions: range syntax, negative indexing, flag parsing, and whitespace collapsing. Each failure is a behavior that only emerges from running the binary against specific inputs.

Claude Sonnet probed more carefully and correctly implemented most behaviors. Its only failure was a subtle off-by-one in range semantics: `1:3` includes index 3 (inclusive), producing three fields, but the agent implemented it as exclusive (Python slice behavior), returning only two. This is a prime example of a bias from the agent's training language (Python slices are exclusive) overriding what the binary actually does.

Gemini passed all checks by probing the range behavior with a concrete example that revealed the inclusive endpoint.

**Checks that caused failures:**

- `B3` — Range inclusive: Claude Sonnet returned `beta gamma` (exclusive end) instead of `beta gamma delta` (inclusive end). GPT-4o produced no output (no range parser at all).
- `B4` — Negative index: GPT-4o exited with error; should silently return the last field.
- `B5` / `B6` — Custom delimiter flags: GPT-4o ignored `-f` and `-o` entirely.
- `B8` — Multi-space / tab collapse: GPT-4o used `split(" ")` which does not collapse runs of whitespace.

---

## Task 004 — `XAMPPRocky__tokei.d2c7b84`

| Agent | Result | Checks Passed | Primary Failure |
|---|---|---|---|
| GPT-4o | **FAIL** | 6 / 8 | Counted Python docstrings as code (not comments); JSON output used wrong field names (`total_lines` instead of `lines`; missing `inaccurate` and `reports` fields) |
| Claude Sonnet 4.6 | **FAIL** | 7 / 8 | Docstring counting correct; JSON output missing `inaccurate` and `reports` fields required by schema |
| Gemini 1.5 Pro | **FAIL** | 6 / 8 | Empty file silently skipped instead of showing a zero-count row; JSON output missing `inaccurate` field |

**Verdict: APPROVED (3 / 3 agents failed)**

**Failure analysis:**

All three agents failed on the JSON schema check (B2), confirming that the exact field names and structure of `tokei`'s `--output json` cannot be guessed without running the binary. The schema includes `inaccurate`, `reports`, and per-report `blobs` fields that are specific to tokei's internal architecture. An agent that implements a reasonable-looking JSON output — with `code`, `comments`, `blanks`, and `lines` — will still fail because it omits these fields.

The second axis of failure split agents: GPT-4o failed on docstring classification (counting `"""..."""` blocks as code), while Gemini failed on empty-file behavior (skipping the file rather than showing a zero-count row). Both behaviors must be discovered by probing the binary with the specific fixture — a file containing only a docstring, and a zero-byte file.

These failures validate that the task cannot be solved by implementing a generic line counter. The agent must specifically probe: what does tokei do with a docstring? What does tokei emit for an empty file? What is the exact JSON schema?

**Checks that caused failures:**

- `B1` — Docstring as comment: GPT-4o counted `"""Say hello."""` as code (code=4, comments=1). Correct is code=3, comments=2.
- `B2` — JSON schema: All three agents missing `inaccurate` field; GPT-4o also used wrong key name `total_lines`.
- `B5_empty_file_zero_row` — Gemini silently skipped the empty file; should show Python row with all zeros.

---

## Overall Verdict

| Task | Source | GPT-4o | Claude Sonnet 4.6 | Gemini 1.5 Pro | Approval |
|---|---|---|---|---|---|
| Task 001 | `tomnomnom__gron.c29c628` | FAIL (3/8) | FAIL (5/8) | PASS (8/8) | ✅ APPROVED (2/3 failed) |
| Task 002 | `chmln__sd.f8e1042` | FAIL (13/15) | FAIL (14/15) | FAIL (14/15) | ✅ APPROVED (3/3 failed) |
| Task 003 | `theryangeary__choose.a5d3f91` | FAIL (6/11) | FAIL (10/11) | PASS (11/11) | ✅ APPROVED (2/3 failed) |
| Task 004 | `XAMPPRocky__tokei.d2c7b84` | FAIL (6/8) | FAIL (7/8) | FAIL (6/8) | ✅ APPROVED (3/3 failed) |

**All 4 tasks approved.**

---

## Cross-Task Failure Patterns

**Pattern 1 — Training-language bias overrides binary evidence**
Agents apply Python/sed conventions instead of what the binary actually does. Examples: Python slice semantics (exclusive range end) overriding `choose`'s inclusive range; `\1` sed syntax overriding `sd`'s `$1` syntax; `json.key` dot access overriding `gron`'s bracket-notation rule.

**Pattern 2 — Schema inference without probing**
Agents that guess JSON field names from common convention fail when the binary uses tool-specific names (`inaccurate`, `reports`, `blobs` in tokei; `$0` whole-match reference in sd). JSON output structure must always be discovered by running `--output json` on known inputs.

**Pattern 3 — Edge-case omission**
Agents implement the happy path correctly but miss: empty file handling, out-of-range field handling, no-match exit codes, and mode flags with side-effect constraints (preview no-modify). These require probing with adversarial fixtures, not just normal inputs.

**Pattern 4 — Surface-level mode discovery**
Agents discover a mode flag exists from `--help` but implement the semantics incorrectly. GPT-4o implemented preview mode but still wrote the file. Claude Sonnet implemented ungron but only handled flat `json.key` paths. Modes with non-obvious contracts (no file write, nested path reconstruction) require deep binary probing, not just flag presence detection.
