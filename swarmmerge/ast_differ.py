import ast
from typing import Dict, List
from .types import DiffHunk

class ASTDiffer:
    """Computes structural differences between two ASTs."""
    
    def diff(self, source_a: str, source_b: str) -> List[DiffHunk]:
        """Compute the AST-level diff between two source strings."""
        hunks: List[DiffHunk] = []
        syms_a = self.extract_symbols(source_a)
        syms_b = self.extract_symbols(source_b)
        
        # Identify deleted and modified
        for name, node_a in syms_a.items():
            if name not in syms_b:
                hunks.append(DiffHunk(
                    start_line=node_a.lineno,
                    end_line=node_a.end_lineno or node_a.lineno,
                    operation='delete',
                    content='',
                    symbol_name=name
                ))
            else:
                node_b = syms_b[name]
                src_a = ast.unparse(node_a)
                src_b = ast.unparse(node_b)
                if src_a != src_b:
                    hunks.append(DiffHunk(
                        start_line=node_a.lineno,
                        end_line=node_a.end_lineno or node_a.lineno,
                        operation='modify',
                        content=src_b,
                        symbol_name=name
                    ))
                    
        # Identify added
        for name, node_b in syms_b.items():
            if name not in syms_a:
                hunks.append(DiffHunk(
                    start_line=node_b.lineno,
                    end_line=node_b.end_lineno or node_b.lineno,
                    operation='add',
                    content=ast.unparse(node_b),
                    symbol_name=name
                ))
                
        return hunks

    def extract_symbols(self, source: str) -> Dict[str, ast.AST]:
        """Extract top-level symbol map (functions, classes, imports)."""
        symbols: Dict[str, ast.AST] = {}
        if not source.strip():
            return symbols
            
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return symbols
            
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                symbols[node.name] = node
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    symbols[f"import_{alias.name}"] = node
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    symbols[f"from_{module}_{alias.name}"] = node
        return symbols
