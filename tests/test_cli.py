import subprocess
import sys


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "swarmmerge", "-h"], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0
    assert "AST-aware 3-way merge tool" in result.stdout

def test_cli_merge_no_conflict(tmp_path):
    base = tmp_path / "base.py"
    ours = tmp_path / "ours.py"
    theirs = tmp_path / "theirs.py"
    base.write_text("def foo(): pass")
    ours.write_text("def foo(): pass\ndef bar(): pass")
    theirs.write_text("def foo(): pass\ndef baz(): pass")
    
    result = subprocess.run(
        [sys.executable, "-m", "swarmmerge", "merge", str(base), str(ours), str(theirs)],
        capture_output=True, text=True, check=False
    )
    assert result.returncode == 0
    assert "def bar():" in result.stdout
    assert "def baz():" in result.stdout
