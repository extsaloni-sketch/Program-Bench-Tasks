# Difficulty Taxonomy

This repository uses agent failure rate as the primary signal for task difficulty.

## Difficulty Buckets

| Level | Definition |
|---|---|
| Easy | Fewer than 33.3% of evaluated agents fail |
| Medium | 33.3% to 66.6% of evaluated agents fail |
| Difficult | More than 66.6% of evaluated agents fail |

## Current Task Classification

| Task | Agents Evaluated | Agents Failed | Failure Rate | Difficulty | Main Failure Reasons |
|---|---:|---:|---:|---|---|
| hashcards | 6 | 4 | 66.7% | Difficult | Export JSON shape, command-specific help behavior, card parsing, validation, stats, and export metadata |
| BLAKE3 | 5 | 2 | 40.0% | Medium | Full CLI compatibility, exact output formatting, check-file behavior, advanced flag combinations, and build compatibility |
| ripgrep | 6 | 6 | 100.0% | Difficult | Advanced flags, recursive search behavior, glob handling, output modes, shell completion, threading, and multiline options |
| parallel-disk-usage | 6 | 4 | 66.7% | Difficult | Hidden behavioral checks, output correctness, CLI behavior, and build/compile compatibility |
| zstd | 6 | 5 | 83.3% | Difficult | Compression/decompression behavior, stdin/stdout handling, corrupted input detection, round-trip correctness, and build compatibility |

## Failure Reason Notes

- **hashcards:** Agents struggled with matching the exact CLI behavior and export format. The common gaps were incomplete JSON export structure, card parsing, validation edge cases, stats handling, and metadata fields.
- **BLAKE3:** Failures were mostly around compatibility with the full BLAKE3 CLI surface. Agents missed exact formatting, check-file behavior, advanced flag combinations, robustness cases, or failed to build correctly.
- **ripgrep:** This task showed broad failures across agents. Common missing behavior included advanced flags, recursive traversal, glob handling, output formatting, shell completion generation, threading, and multiline modes.
- **parallel-disk-usage:** Agents failed on hidden behavioral checks, output correctness, and build compatibility. Some solutions passed baseline cases but did not fully match the expected CLI behavior.
- **zstd:** Agents missed important compression/decompression behavior, stdin/stdout handling, corrupted input detection, and round-trip correctness. Some failures were also due to compile/build issues.
