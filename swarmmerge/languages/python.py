from ..ast_differ import ASTDiffer
from ..resolver import ConflictResolver
from ..synthesizer import Synthesizer
from ..types import MergeResult, MergeStats


class PythonMergeStrategy:
    """Python-specific AST merge logic."""
    
    def __init__(self):
        self.differ = ASTDiffer()
        self.resolver = ConflictResolver()
        self.synthesizer = Synthesizer()
        
    def merge(self, base: str, ours: str, theirs: str) -> MergeResult:
        hunks_ours = self.differ.diff(base, ours)
        hunks_theirs = self.differ.diff(base, theirs)
        
        _, unresolved = self.resolver.resolve(base, ours, theirs, [])
        
        stats = MergeStats(
            conflicts_found=len(unresolved)
        )
        
        if unresolved:
            # If conflicts exist, we don't return synthesized output yet, or we return conflict markers.
            # Simplified for now.
            return MergeResult("", unresolved, stats)
            
        merged_source = self.synthesizer.synthesize(base, hunks_ours, hunks_theirs)
        stats.total_nodes_merged = len(hunks_ours) + len(hunks_theirs)
        
        return MergeResult(merged_source, unresolved, stats)
