import pytest
from swarmmerge import ConflictResolver, ConflictType

def test_resolve_no_conflict():
    resolver = ConflictResolver()
    base = "def foo(): pass"
    ours = "def foo(): pass\ndef bar(): pass"
    theirs = "def foo(): pass\ndef baz(): pass"
    resolved, conflicts = resolver.resolve(base, ours, theirs, [])
    assert len(conflicts) == 0

def test_resolve_structural_conflict():
    resolver = ConflictResolver()
    base = "def foo(): pass"
    ours = "def foo(): return 1"
    theirs = "def foo(): return 2"
    resolved, conflicts = resolver.resolve(base, ours, theirs, [])
    assert len(conflicts) == 1
    assert conflicts[0].conflict_type == ConflictType.STRUCTURAL
    assert conflicts[0].description == "Concurrent modification of symbol 'foo'"
