# 🔀 SwarmMerge

[![CI](https://github.com/mbgulden/swarmmerge/actions/workflows/ci.yml/badge.svg)](https://github.com/mbgulden/swarmmerge/actions)
[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/swarmmerge/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Semantic 3-way AST conflict resolution and code synthesizer for the Prismatic Engine swarm ecosystem.**
>
> When several agents edit the same file at the same time, a line-based merge drowns in false conflicts. SwarmMerge merges at the AST level — diffing, resolving, and synthesizing Python *symbols* (functions, classes, imports) instead of text lines — so concurrent multi-agent code mutations compose cleanly.

---

## 💡 Why SwarmMerge?

Two agents both touch `utils.py`: one appends a helper at the bottom, the other reformats the docstring at the top. A text merge flags a conflict because the lines moved. SwarmMerge sees the same two facts as *structural* operations on two different symbols — no overlap, no conflict — and synthesizes a clean merged file automatically.

SwarmMerge exists for the same reason the whole swarm toolkit does: autonomous agents need infrastructure that behaves deterministically. Give it a **base** and two changed versions (**ours** / **theirs**), and it returns merged source plus a list of real structural conflicts, with stats on what was merged.

## 🏛️ How it works

```
    base.py  ┬─ ours.py       theirs.py ─┬  base.py
             │                           │
             ▼                           ▼
      ASTDiffer.diff()            ASTDiffer.diff()
        hunks_ours                 hunks_theirs
             │                           │
             └─────────┬─────────────────┘
                       ▼
            ConflictResolver.resolve()
            - same symbol modified differently → STRUCTURAL conflict
            - everything else → auto-resolvable
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
    Synthesizer.synthesize()     MergeResult("", conflicts, stats)
    merged Python source         (conflicts reported; nothing
    + MergeStats                  synthesized while unresolved)
```

1. **ASTDiffer** — extracts top-level symbols (functions, classes, imports) from each file via `ast`, and produces `DiffHunk`s: `add`, `delete`, or `modify` per symbol.
2. **ConflictResolver** — compares both diffs against base. The only true conflict today: both sides modified (or deleted) the *same symbol* in different ways → a `ConflictType.STRUCTURAL` conflict.
3. **Synthesizer** — applies both hunk sets to the base symbol map, deduplicates and sorts the import block, and reassembles valid Python source. Imports always land first, sorted.
4. **PythonMergeStrategy** — the language driver wired through `ASTMerger`. (Architecture supports additional language strategies; Python is the only one shipped in v0.1.0.)

## 📦 Installation

```bash
pip install swarmmerge
```

*Zero runtime dependencies. Pure Python standard library. Ships typed (`py.typed`).*

## 🚀 Quick Start

```bash
# Merge two diverged copies of the same file against their common base
swarmmerge merge base.py ours.py theirs.py > merged.py

# Inspect conflicts instead of merging
swarmmerge conflicts base.py ours.py theirs.py
```

`merge` prints the merged source and exits `0` when there are no conflicts; it prints a conflict count and exits `1` when there are.

A 5-minute end-to-end example:

```bash
cat > base.py <<'EOF'
def greet():
    print("hello")
EOF

cat > ours.py <<'EOF'
def greet():
    print("hello")

def farewell():
    print("goodbye")
EOF

cat > theirs.py <<'EOF'
def greet():
    print("hello")

def bonjour():
    print("bonjour")
EOF

swarmmerge merge base.py ours.py theirs.py
# def greet():
#     print('hello')
#
# def farewell():
#     print('goodbye')
#
# def bonjour():
#     print('bonjour')
```

Both sides added different functions → no conflict, everything composed. Now make them disagree:

```bash
cat > ours2.py <<'EOF'
def greet():
    print("hi")
EOF

cat > theirs2.py <<'EOF'
def greet():
    print("howdy")
EOF

swarmmerge merge base.py ours2.py theirs2.py; echo "exit=$?"
# Conflicts found: 1
# exit=1
```

## 🐍 Python API

```python
from swarmmerge import ASTMerger, ConflictType

merger = ASTMerger()

# In-memory 3-way merge
result = merger.merge(base_src, ours_src, theirs_src)

if result.conflicts:
    for c in result.conflicts:
        print(c.conflict_id, c.conflict_type, c.description,
              c.base_range, c.ours_range, c.theirs_range)
else:
    print(result.merged_source)

# MergeStats: total_nodes_merged, auto_resolved, conflicts_found, imports_synthesized
print(result.stats)

# File-based API (stamps conflict file paths)
result = merger.merge_files(Path("base.py"), Path("ours.py"), Path("theirs.py"))
```

The lower-level pieces are exported for custom pipelines:

```python
from swarmmerge import ASTDiffer, ConflictResolver, Synthesizer, PythonMergeStrategy

differ = ASTDiffer()
hunks = differ.diff(base_src, ours_src)          # List[DiffHunk]: add/delete/modify per symbol

resolver = ConflictResolver()
_, conflicts = resolver.resolve(base_src, ours_src, theirs_src, [])

synth = Synthesizer()
merged = synth.synthesize(base_src, hunks_ours, hunks_theirs)
```

Public types: `MergeResult`, `Conflict`, `ConflictType` (`STRUCTURAL` / `TEXTUAL` / `SEMANTIC` / `IMPORT`), `MergeStats`, `DiffHunk`, `MergeError`, `ConflictError`.

## 📋 CLI reference

```
swarmmerge merge     base ours theirs   # merge 3 files, print merged source (exit 1 on conflict)
swarmmerge conflicts base ours theirs   # print each conflict on its own line
swarmmerge -h                            # help
```

(`swarmmerge diff` exists as a placeholder subcommand and is not yet implemented.)

## 🧪 Testing

```bash
pip install -e ".[test]"
pytest tests/ -v
```

The suite covers the differ, resolver, synthesizer, merger facade, and CLI, including the conflicting-modification path (same symbol changed differently on both sides → one `STRUCTURAL` conflict, no synthesized output).

## 🗺️ Swarm Ecosystem

SwarmMerge is part of the **Swarm Primitives Ecosystem** for autonomous agent swarms, alongside the Prismatic Engine:

- 🔒 **SwarmLock**: Tokenized, non-blocking distributed advisory locks.
- ⏱️ **SwarmCron**: Native high-precision background cron scheduling.
- 🛡️ **SwarmProof**: Truth Oracle, evidence ledgers, and anti-hallucination gates.
- 🔀 **SwarmMerge**: Semantic AST 3-way merge for concurrent agent code edits.
- 🧠 **SwarmCurator**: Long-term memory distillation and context compaction *(coming soon)*.

## 📄 License

MIT © Michael Gulden
