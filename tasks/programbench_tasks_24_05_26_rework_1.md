## Task 1 — `tomnomnom__gron.c29c628`

| Field | Value |
|---|---|
| **Benchmark** | ProgramBench |
| **Paper** | https://arxiv.org/abs/2605.03546 |
| **Benchmark repo** | https://github.com/facebookresearch/ProgramBench |
| **Task source** | `tomnomnom__gron.c29c628` |
| **Task folder** | https://github.com/tomnomnom/gron/tree/c29c628 |
| **Original repo** | https://github.com/tomnomnom/gron |
| **Program type** | JSON-to-greppable-assignments CLI transformer |

### Task Prompt

Rebuild the behavior of the `gron` command-line tool using only the compiled binary and available documentation/help text. The original source code and original tests must not be available to the agent. `gron` transforms JSON into discrete, greppable assignment statements and can reverse that transformation with `--ungron`. The agent must discover all supported modes, flags, JSON type handling, key-naming rules, stdin/file input modes, and error behavior entirely through binary interaction and documentation.

### Model-visible input

- Compiled binary (`gron`)
- `README.md` and `--help` output
- Allowed sample files: `input.json`, `nested.json`, `arr.json`, `types.json`, `special_keys.json`

---

### Internal Evaluation / Hidden Checks

**Behavior 1: Flatten a simple flat JSON object**

Input file (`input.json`):
```json
{"name": "Alice", "age": 30, "active": true}
```

Command:
```
gron input.json
```

Expected stdout (exact, including trailing newline):
```
json = {};
json.active = true;
json.age = 30;
json.name = "Alice";
```

Expected stderr: empty
Expected exit code: `0`

> **Reviewer note:** `gron` sorts keys alphabetically. Confirm key order against the binary before finalizing. If the binary outputs in insertion order, the expected stdout above must be updated to `name`, `age`, `active` order.

---

**Behavior 2: Flatten a nested object**

Input file (`nested.json`):
```json
{"user": {"name": "Bob", "role": "admin"}, "version": 2}
```

Command:
```
gron nested.json
```

Expected stdout (exact):
```
json = {};
json.user = {};
json.user.name = "Bob";
json.user.role = "admin";
json.version = 2;
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 3: Flatten a JSON array**

Input file (`arr.json`):
```json
{"tags": ["go", "cli", "json"], "count": 3}
```

Command:
```
gron arr.json
```

Expected stdout (exact):
```
json = {};
json.count = 3;
json.tags = [];
json.tags[0] = "go";
json.tags[1] = "cli";
json.tags[2] = "json";
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 4: Handle all JSON primitive types including null**

Input file (`types.json`):
```json
{"str": "hello", "num": 3.14, "flag": false, "nothing": null}
```

Command:
```
gron types.json
```

Expected stdout (exact):
```
json = {};
json.flag = false;
json.nothing = null;
json.num = 3.14;
json.str = "hello";
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 5: Keys with special characters use bracket notation**

Input file (`special_keys.json`):
```json
{"foo.bar": 1, "hello world": 2, "kebab-key": 3}
```

Command:
```
gron special_keys.json
```

Expected stdout (exact):
```
json = {};
json["foo.bar"] = 1;
json["hello world"] = 2;
json["kebab-key"] = 3;
```

Expected stderr: empty
Expected exit code: `0`

> **Key rule:** Keys that are not valid JavaScript identifiers (contain dots, spaces, hyphens, or other non-identifier characters) must be rendered using bracket notation (`json["key"]`) instead of dot notation (`json.key`). The agent must discover this by probing the binary with such inputs.

---

**Behavior 6: Ungron — reverse the transformation back to JSON**

Input via stdin:
```
json = {};
json.name = "Alice";
json.age = 30;
```

Command:
```
gron --ungron
```

Expected stdout (exact, compact single line):
```
{
  "age": 30,
  "name": "Alice"
}
```

> **Reviewer note:** Confirm whether `--ungron` / `-u` produces compact single-line JSON or pretty-printed JSON. Update expected stdout to match the binary exactly. The `-u` short flag must also produce identical output.

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 7: Read from stdin when no file argument is given**

Command:
```
echo '{"x": 1}' | gron
```

Expected stdout (exact):
```
json = {};
json.x = 1;
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 8: Invalid JSON — non-zero exit and stderr message, no stdout**

Command:
```
echo '{bad json}' | gron
```

Expected stdout: empty (nothing written to stdout)
Expected stderr: non-empty error message describing the parse failure (exact text must be confirmed against the binary)
Expected exit code: `1`

---

### Complexity Notes

High complexity. The reconstructed tool must correctly handle nested objects, arrays, all JSON primitive types (null, bool, number, string), the bracket-notation rule for non-identifier keys, the `--ungron` reverse mode, stdin/file duality, and malformed-input error behavior. The exact assignment-statement syntax (`json.foo = "bar";` vs `json["foo.bar"] = 1;`) cannot be guessed and must be inferred from binary probing. A hardcoded or echo-only solution fails immediately on the nested object, special-key, and ungron cases.

---
---

## Task 2 — `chmln__sd.f8e1042`

| Field | Value |
|---|---|
| **Benchmark** | ProgramBench |
| **Paper** | https://arxiv.org/abs/2605.03546 |
| **Benchmark repo** | https://github.com/facebookresearch/ProgramBench |
| **Task source** | `chmln__sd.f8e1042` |
| **Task folder** | https://github.com/chmln/sd/tree/f8e1042 |
| **Original repo** | https://github.com/chmln/sd |
| **Program type** | Regex and fixed-string find-and-replace CLI tool |

### Task Prompt

Rebuild the behavior of the `sd` (sed replacement) command-line tool using only the compiled binary and available documentation/help text. The original source code and original tests must not be available to the agent. `sd` performs find-and-replace on files or stdin using regex or fixed strings. The agent must discover its invocation interface, capture group substitution syntax, fixed-string mode, in-place file editing with empty stdout, no-match behavior, newline preservation, and error handling entirely through binary interaction and documentation.

### Model-visible input

- Compiled binary (`sd`)
- `README.md` and `--help` output
- Allowed sample files: `greet.txt`, `a.txt`, `b.txt`

---

### Internal Evaluation / Hidden Checks

**Behavior 1: Basic literal string replacement via stdin**

Command:
```
echo "hello world" | sd "world" "earth"
```

Expected stdout (exact):
```
hello earth
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 2: Regex replacement — all non-overlapping matches replaced**

Command:
```
echo "foo123bar456" | sd '\d+' 'NUM'
```

Expected stdout (exact):
```
fooNUMbarNUM
```

Expected stderr: empty
Expected exit code: `0`

> All non-overlapping matches in the input must be replaced, not only the first match.

---

**Behavior 3: Capture group back-references in replacement**

Command:
```
echo "2024-01-15" | sd '(\d{4})-(\d{2})-(\d{2})' '$3/$2/$1'
```

Expected stdout (exact):
```
15/01/2024
```

Expected stderr: empty
Expected exit code: `0`

> `sd` uses `$1`, `$2`, `$3` syntax for capture group back-references, which differs from sed's `\1` syntax. The agent must discover this from binary probing.

---

**Behavior 4: Fixed-strings mode — `-F` flag disables regex interpretation**

Command:
```
echo "price is $5.00" | sd -F '$5.00' '$6.00'
```

Expected stdout (exact):
```
price is $6.00
```

Expected stderr: empty
Expected exit code: `0`

> Without `-F`, the `$` is interpreted as a regex end-of-line anchor and `.` as any character, producing wrong or no output. The `-F` / `--fixed-strings` flag treats both the search string and replacement as plain literals.

---

**Behavior 5: In-place file editing — stdout is empty, file is modified**

Setup file (`greet.txt`) before command:
```
Hello Alice.
Hello Alice again.
```

Command:
```
sd "Alice" "Bob" greet.txt
```

Expected stdout: empty (nothing written to stdout)
Expected stderr: empty
Expected exit code: `0`

Expected state of `greet.txt` after command (exact):
```
Hello Bob.
Hello Bob again.
```

---

**Behavior 6: Multi-file in-place replacement**

Setup files before command:
- `a.txt` contains exactly: `color`
- `b.txt` contains exactly: `colour`

Command:
```
sd 'colou?r' 'hue' a.txt b.txt
```

Expected stdout: empty
Expected stderr: empty
Expected exit code: `0`

Expected state after command:
- `a.txt` contains exactly: `hue`
- `b.txt` contains exactly: `hue`

---

**Behavior 7: No-match — file unchanged, stdout empty, exit 0**

Setup file (`greet.txt`) before command:
```
Hello Bob.
```

Command:
```
sd "Alice" "Carol" greet.txt
```

Expected stdout: empty
Expected stderr: empty
Expected exit code: `0`

Expected state of `greet.txt` after command (unchanged):
```
Hello Bob.
```

> `sd` exits with code `0` even when no substitution occurs, unlike `grep`. The agent must discover this from binary probing.

---

**Behavior 8: Newline preservation — trailing newline is not dropped or doubled**

Command:
```
printf "line one\nline two\n" | sd "one" "1"
```

Expected stdout (exact, two lines with trailing newline):
```
line 1
line two
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 9: Invalid regex — non-zero exit and stderr error, stdout empty**

Command:
```
echo "test" | sd '(unclosed' 'x'
```

Expected stdout: empty
Expected stderr: non-empty error message describing the regex parse failure (exact text must be confirmed against the binary)
Expected exit code: `1`

---

### Complexity Notes

High complexity. The tool uses a non-trivial invocation interface that differs from sed in capture-group syntax (`$1` not `\1`), in-place editing convention (no explicit `-i` flag; file paths are positional), and fixed-string mode flag (`-F`). A thin sed wrapper fails on capture-group syntax, no-match behavior (sed can exit non-zero; sd exits 0), and newline handling. A hardcoded implementation fails on any regex or multi-file test.

---
---

## Task 3 — `theryangeary__choose.a5d3f91`

| Field | Value |
|---|---|
| **Benchmark** | ProgramBench |
| **Paper** | https://arxiv.org/abs/2605.03546 |
| **Benchmark repo** | https://github.com/facebookresearch/ProgramBench |
| **Task source** | `theryangeary__choose.a5d3f91` |
| **Task folder** | https://github.com/theryangeary/choose/tree/a5d3f91 |
| **Original repo** | https://github.com/theryangeary/choose |
| **Program type** | Field-selection CLI tool (human-friendly cut/awk replacement) |

### Task Prompt

Rebuild the behavior of the `choose` command-line tool using only the compiled binary and available documentation/help text. The original source code and original tests must not be available to the agent. `choose` selects whitespace-delimited fields from each input line, supporting single fields, inclusive ranges, negative (tail) indexing, custom input field separators (as a regex), custom output field separators, and multi-line processing. The agent must discover all field selection semantics, indexing rules, and delimiter flags entirely through binary interaction and documentation.

### Model-visible input

- Compiled binary (`choose`)
- `README.md` and `--help` output
- Allowed sample files: `lines.txt`

---

### Internal Evaluation / Hidden Checks

**Behavior 1: Select a single field by zero-based index**

Command:
```
echo "alpha beta gamma delta" | choose 2
```

Expected stdout (exact):
```
gamma
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 2: Select multiple non-consecutive fields — printed in argument order**

Command:
```
echo "alpha beta gamma delta" | choose 0 3
```

Expected stdout (exact):
```
alpha delta
```

Expected stderr: empty
Expected exit code: `0`

> Fields are printed in the order they appear as arguments, not in original line order. Passing `3 0` would print `delta alpha`. The agent must confirm this by probing with reversed argument order.

---

**Behavior 3: Select an inclusive range of fields**

Command:
```
echo "alpha beta gamma delta epsilon" | choose 1:3
```

Expected stdout (exact):
```
beta gamma delta
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 4: Negative index — select the last field**

Command:
```
echo "alpha beta gamma delta" | choose -1
```

Expected stdout (exact):
```
delta
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 5: Custom input field separator (`-f` flag accepts a regex)**

Command:
```
echo "alpha,beta,gamma,delta" | choose -f ',' 1
```

Expected stdout (exact):
```
beta
```

Expected stderr: empty
Expected exit code: `0`

> The `-f` / `--field-separator` flag accepts a regex pattern. A plain comma `,` is also a valid single-character regex. The agent must discover the flag name and its regex semantics from the binary and help text.

---

**Behavior 6: Custom output field separator (`-o` flag)**

Command:
```
echo "alpha beta gamma delta" | choose -o ':' 0 1 2
```

Expected stdout (exact):
```
alpha:beta:gamma
```

Expected stderr: empty
Expected exit code: `0`

> The `-o` / `--output-field-separator` flag controls the string placed between output fields. The agent must discover the flag name from help text.

---

**Behavior 7: Multi-line input — each line is processed independently**

Input file (`lines.txt`):
```
one two three
four five six
seven eight nine
```

Command:
```
choose 0 2 < lines.txt
```

Expected stdout (exact):
```
one three
four six
seven nine
```

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 8: Multiple consecutive spaces/tabs treated as a single delimiter**

Command:
```
printf "alpha  beta\tgamma   delta" | choose 1
```

Expected stdout (exact):
```
beta
```

Expected stderr: empty
Expected exit code: `0`

> The default whitespace splitter collapses multiple spaces and tabs. A naive `split(" ")` implementation produces wrong field indices. The agent must verify this by probing the binary with multi-space input.

---

**Behavior 9: Out-of-range field index — empty output for that line, exit 0, no error**

Command:
```
echo "alpha beta" | choose 10
```

Expected stdout: empty (the line produces no output; no error is printed)
Expected stderr: empty
Expected exit code: `0`

> Out-of-range indices are silently ignored. The program does not crash, does not print an error, and exits with code 0. The agent must confirm this exact behavior by probing the binary.

---

### Complexity Notes

High complexity. The agent must correctly implement zero-based indexing, inclusive range syntax (`a:b`), negative tail indexing, argument-order field printing, a regex-accepting input separator flag, a configurable output separator flag, multi-space collapsing, and silent out-of-range handling. A `cut` wrapper fails on negative indices, range semantics, and argument-order printing. A naive split-on-space implementation fails on the multi-space collapsing case. A hardcoded solution fails on every parameterized test.

---
---

## Task 4 — `XAMPPRocky__tokei.d2c7b84`

| Field | Value |
|---|---|
| **Benchmark** | ProgramBench |
| **Paper** | https://arxiv.org/abs/2605.03546 |
| **Benchmark repo** | https://github.com/facebookresearch/ProgramBench |
| **Task source** | `XAMPPRocky__tokei.d2c7b84` |
| **Task folder** | https://github.com/XAMPPRocky/tokei/tree/d2c7b84 |
| **Original repo** | https://github.com/XAMPPRocky/tokei |
| **Program type** | Source code line-counting CLI tool |

### Task Prompt

Rebuild the behavior of the `tokei` command-line tool using only the compiled binary and available documentation/help text. The original source code and original tests must not be available to the agent. `tokei` counts lines of code, comments, and blank lines per programming language across a directory or set of files, with support for structured JSON output, language type filtering, and glob-based file exclusion. The agent must discover all counting semantics (including docstring classification), output formats, and filtering flags entirely through binary interaction and documentation.

### Model-visible input

- Compiled binary (`tokei`)
- `README.md` and `--help` output
- Allowed sample workspace: a provided directory of source files with known, fixed content (see fixtures below)

---

### Fixture Files (model-visible)

**`sample/hello.py`** (6 lines total):
```python
# This is a comment
def greet(name):
    """Say hello."""
    print(f"Hello, {name}")

greet("world")
```

**`project/main.rs`** (10 lines total):
```rust
// Entry point
fn main() {
    let msg = "hello";
    println!("{}", msg);
    helper();
}

fn helper() {
    println!("done");
}
```

**`project/util.py`** (5 lines total):
```python
def add(a, b):
    return a + b


result = add(1, 2)
```

**`mixed/app.py`**: `print("app")\n` (1 line)
**`mixed/lib.rs`**: `fn main() {}\n` (1 line)
**`mixed/notes.md`**: `# Notes\n` (1 line)

**`src/main.py`**: `print("main")\n` (1 line)
**`src/generated.py`**: `print("generated")\n` (1 line)

**`empty.py`**: 0 bytes

**`data.xyz`**: `some content\nmore content\n` (2 lines, unknown extension)

---

### Internal Evaluation / Hidden Checks

**Behavior 1: Per-file counting — code, comments, blanks for Python**

Command:
```
tokei sample/hello.py
```

Expected stdout: a formatted table containing a Python row with exactly:
- `code` = `3`
- `comments` = `2`
- `blanks` = `1`
- `lines` = `6`

> Python docstrings (`"""..."""`) are counted as **comments** by tokei, not as code. The `#` line-comment is also counted as a comment. The empty line between the docstring and the `greet("world")` call is the one blank line. The agent must discover the docstring-as-comment rule by probing the binary with a file that contains docstrings.

Expected stderr: empty
Expected exit code: `0`

---

**Behavior 2: Multi-language directory — per-language rows and Total row**

Command:
```
tokei project/
```

Expected stdout: a formatted table containing at minimum:

Rust row:
- `code` = `8`, `comments` = `1`, `blanks` = `1`, `lines` = `10`

Python row:
- `code` = `3`, `comments` = `0`, `blanks` = `2`, `lines` = `5`

Total row:
- `lines` = `15`

Expected stderr: empty
Expected exit code: `0`

> **Reviewer note:** Confirm blank-line counts for `util.py` against the binary. The two consecutive blank lines between `return a + b` and `result = add(1, 2)` should each be counted as blanks.

---

**Behavior 3: JSON output format — exact field names and structure**

Command:
```
tokei sample/hello.py --output json
```

Expected stdout: valid JSON with the following exact top-level structure (field names are exact):
```json
{
  "Python": {
    "blanks": 1,
    "code": 3,
    "comments": 2,
    "lines": 6,
    "inaccurate": false,
    "reports": [
      {
        "name": "sample/hello.py",
        "stats": {
          "blanks": 1,
          "code": 3,
          "comments": 2,
          "lines": 6,
          "blobs": {}
        }
      }
    ]
  },
  "Total": {
    "blanks": 1,
    "code": 3,
    "comments": 2,
    "lines": 6,
    "inaccurate": false,
    "reports": []
  }
}
```

Expected stderr: empty
Expected exit code: `0`

> **Reviewer note:** Confirm the exact JSON schema against the binary (`--output json`). The field names `blanks`, `code`, `comments`, `lines`, `inaccurate`, `reports`, and `blobs` are exact as documented in the tokei source. Update the expected JSON if the binary at this commit produces a different schema.

---

**Behavior 4: Language type filter — only Python rows appear**

Command:
```
tokei mixed/ -t Python
```

Expected stdout: a table containing a Python row for `mixed/app.py` and no Rust or Markdown rows.
Expected stderr: empty
Expected exit code: `0`

> The flag is `-t` / `--type` and accepts a comma-separated list of language names (case-sensitive as recognized by tokei, e.g. `Python`, `Rust`, `Markdown`). The agent must discover the exact flag name and accepted language name format from the binary and help text.

---

**Behavior 5: Glob file exclusion — matching files are not counted**

Command:
```
tokei src/ --exclude "generated*"
```

Expected stdout: a table counting only `src/main.py` (1 line, 1 code, 0 comments, 0 blanks). `src/generated.py` must not appear anywhere in the output.
Expected stderr: empty
Expected exit code: `0`

> The `--exclude` flag accepts a glob pattern matched against file basenames. `generated*` matches `generated.py`. The agent must discover the flag name and matching semantics from the binary and help text.

---

**Behavior 6: Empty file — all-zero counts, no crash, exit 0**

Command:
```
tokei empty.py
```

Expected stdout: a table containing a Python row with `code` = `0`, `comments` = `0`, `blanks` = `0`, `lines` = `0`.
Expected stderr: empty
Expected exit code: `0`

> tokei shows the detected language row with zero counts for an empty file. It does not crash, skip the file, or print an error.

---

**Behavior 7: Unknown file extension — file silently omitted from output**

Command:
```
tokei data.xyz
```

Expected stdout: a table with no language rows and a Total of `0` lines, OR an empty/minimal table indicating no recognized files. The file is not counted and produces no error.
Expected stderr: empty
Expected exit code: `0`

> tokei silently ignores files with extensions it does not recognize. No error is printed and exit code is 0. The agent must confirm this by probing the binary with an unknown-extension file.

---

### Complexity Notes

High complexity. The agent must reconstruct correct per-language line categorization where Python docstrings are comments (not code), handle multi-language directory aggregation with a Total row, produce valid JSON with exact field names on `--output json`, implement language-type filtering via `-t`, handle glob-based file exclusion via `--exclude`, and correctly handle the zero-count and silent-omission edge cases. A dummy that counts all lines as code fails on every comment/blank separation test. A partial implementation without JSON output fails on Behavior 3. A solution without language filtering fails on Behavior 4.