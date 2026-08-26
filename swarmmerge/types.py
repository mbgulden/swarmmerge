import enum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

class MergeError(Exception):
    """Base class for merge errors."""
    pass

class ConflictError(MergeError):
    """Raised when an unresolvable structural conflict occurs."""
    pass

class ConflictType(enum.Enum):
    STRUCTURAL = "structural"
    TEXTUAL = "textual"
    SEMANTIC = "semantic"
    IMPORT = "import"

@dataclass
class Conflict:
    conflict_id: str
    file_path: str
    base_range: Tuple[int, int]
    ours_range: Tuple[int, int]
    theirs_range: Tuple[int, int]
    conflict_type: ConflictType
    description: str

@dataclass
class MergeStats:
    total_nodes_merged: int = 0
    auto_resolved: int = 0
    conflicts_found: int = 0
    imports_synthesized: int = 0

@dataclass
class DiffHunk:
    start_line: int
    end_line: int
    operation: str  # 'add', 'delete', 'modify'
    content: str
    symbol_name: str

@dataclass
class MergeResult:
    merged_source: str
    conflicts: List[Conflict]
    stats: MergeStats
