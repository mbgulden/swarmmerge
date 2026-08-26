import pytest
from swarmmerge import Synthesizer, DiffHunk

def test_synthesize_add():
    synth = Synthesizer()
    base = "def foo(): pass"
    hunks_ours = [DiffHunk(1, 1, 'add', 'def bar():\n    pass', 'bar')]
    hunks_theirs = []
    res = synth.synthesize(base, hunks_ours, hunks_theirs)
    assert "def foo():" in res
    assert "def bar():" in res

def test_synthesize_imports():
    synth = Synthesizer()
    base = ""
    hunks_ours = [DiffHunk(1, 1, 'add', 'import os', 'import_os')]
    hunks_theirs = [DiffHunk(1, 1, 'add', 'import sys', 'import_sys')]
    res = synth.synthesize(base, hunks_ours, hunks_theirs)
    assert "import os" in res
    assert "import sys" in res
    # Should be sorted
    assert res.index("import os") < res.index("import sys")

def test_synthesize_delete():
    synth = Synthesizer()
    base = "def foo(): pass"
    hunks_ours = [DiffHunk(1, 1, 'delete', '', 'foo')]
    res = synth.synthesize(base, hunks_ours, [])
    assert "def foo():" not in res
