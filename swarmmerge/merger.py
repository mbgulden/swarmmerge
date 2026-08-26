from pathlib import Path
from .types import MergeResult, Conflict, ConflictType, MergeStats, DiffHunk, MergeError, ConflictError
from .languages.python import PythonMergeStrategy

class ASTMerger:
    """Main facade for 3-way merge."""
    
    def __init__(self):
        self.python_strategy = PythonMergeStrategy()

    def merge(self, base: str, ours: str, theirs: str) -> MergeResult:
        """Full 3-way merge pipeline."""
        # Assume Python for now
        return self.python_strategy.merge(base, ours, theirs)
        
    def merge_files(self, base_path: Path, ours_path: Path, theirs_path: Path) -> MergeResult:
        """File-based API."""
        base_src = base_path.read_text(encoding="utf-8")
        ours_src = ours_path.read_text(encoding="utf-8")
        theirs_src = theirs_path.read_text(encoding="utf-8")
        
        result = self.merge(base_src, ours_src, theirs_src)
        for conflict in result.conflicts:
            conflict.file_path = str(base_path)
            
        return result
