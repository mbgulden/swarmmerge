import enum
from dataclasses import dataclass


class MergeError(Exception):
    """Base class for merge errors."""

class ConflictError(MergeError):
    """Raised when an unresolvable structural conflict occurs."""

class ConflictType(enum.Enum):
    STRUCTURAL = "structural"
    TEXTUAL = "textual"
    SEMANTIC = "semantic"
    IMPORT = "import"

@dataclass
class Conflict:
    conflict_id: str
    file_path: str
    base_range: tuple[int, int]
    ours_range: tuple[int, int]
    theirs_range: tuple[int, int]
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
    conflicts: list[Conflict]
    stats: MergeStats
