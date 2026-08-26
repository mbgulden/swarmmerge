import ast
from typing import List, Dict, Set
from .types import DiffHunk
from .ast_differ import ASTDiffer

class Synthesizer:
    """Combines resolved hunks into final source."""
    
    def __init__(self):
        self.differ = ASTDiffer()

    def synthesize(self, base: str, hunks_ours: List[DiffHunk], hunks_theirs: List[DiffHunk]) -> str:
        """Produce merged output from base and hunks."""
        base_symbols = self.differ.extract_symbols(base)
        
        # Apply hunks to a map of symbols
        merged_symbols: Dict[str, str] = {}
        for name, node in base_symbols.items():
            merged_symbols[name] = ast.unparse(node)
            
        # Process ours
        for hunk in hunks_ours:
            if hunk.operation == 'delete':
                merged_symbols.pop(hunk.symbol_name, None)
            else:
                merged_symbols[hunk.symbol_name] = hunk.content
                
        # Process theirs
        for hunk in hunks_theirs:
            if hunk.operation == 'delete':
                merged_symbols.pop(hunk.symbol_name, None)
            else:
                merged_symbols[hunk.symbol_name] = hunk.content
                
        # Synthesize import block and sort
        imports = []
        others = []
        for name, content in merged_symbols.items():
            if name.startswith("import_") or name.startswith("from_"):
                imports.append(content)
            else:
                others.append(content)
                
        # Deduplicate and sort imports
        imports = sorted(list(set(imports)))
        
        final_lines = []
        if imports:
            final_lines.extend(imports)
            final_lines.append("")
        final_lines.extend(others)
        
        return "\n\n".join(final_lines) + "\n"
