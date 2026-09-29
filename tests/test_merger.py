from swarmmerge import ASTMerger


def test_merge_no_conflict():
    merger = ASTMerger()
    base = "def foo(): pass"
    ours = "def foo(): pass\ndef bar(): pass"
    theirs = "def foo(): pass\ndef baz(): pass"
    res = merger.merge(base, ours, theirs)
    assert len(res.conflicts) == 0
    assert "def bar():" in res.merged_source
    assert "def baz():" in res.merged_source

def test_merge_conflict():
    merger = ASTMerger()
    base = "def foo(): pass"
    ours = "def foo(): return 1"
    theirs = "def foo(): return 2"
    res = merger.merge(base, ours, theirs)
    assert len(res.conflicts) == 1
    assert "return 1" not in res.merged_source  # not synthesized due to conflict

def test_merge_identical():
    merger = ASTMerger()
    base = "def foo(): pass"
    res = merger.merge(base, base, base)
    assert len(res.conflicts) == 0
    assert "def foo():" in res.merged_source
