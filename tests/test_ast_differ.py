from swarmmerge import ASTDiffer


def test_extract_symbols():
    differ = ASTDiffer()
    syms = differ.extract_symbols("def foo(): pass\nclass Bar: pass")
    assert "foo" in syms
    assert "Bar" in syms

def test_extract_imports():
    differ = ASTDiffer()
    syms = differ.extract_symbols("import os\nfrom sys import path")
    assert "import_os" in syms
    assert "from_sys_path" in syms

def test_diff_add():
    differ = ASTDiffer()
    hunks = differ.diff("", "def foo(): pass")
    assert len(hunks) == 1
    assert hunks[0].operation == "add"
    assert hunks[0].symbol_name == "foo"

def test_diff_delete():
    differ = ASTDiffer()
    hunks = differ.diff("def foo(): pass", "")
    assert len(hunks) == 1
    assert hunks[0].operation == "delete"
    assert hunks[0].symbol_name == "foo"

def test_diff_modify():
    differ = ASTDiffer()
    hunks = differ.diff("def foo(): pass", "def foo(): return 1")
    assert len(hunks) == 1
    assert hunks[0].operation == "modify"
    assert hunks[0].symbol_name == "foo"
