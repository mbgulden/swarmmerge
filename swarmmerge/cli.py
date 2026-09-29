import argparse
import sys
from pathlib import Path

from .merger import ASTMerger


def main():
    parser = argparse.ArgumentParser(description="AST-aware 3-way merge tool.")
    subparsers = parser.add_subparsers(dest="command")
    
    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("base", type=Path)
    merge_parser.add_argument("ours", type=Path)
    merge_parser.add_argument("theirs", type=Path)
    
    diff_parser = subparsers.add_parser("diff")
    diff_parser.add_argument("a", type=Path)
    diff_parser.add_argument("b", type=Path)
    
    conflicts_parser = subparsers.add_parser("conflicts")
    conflicts_parser.add_argument("base", type=Path)
    conflicts_parser.add_argument("ours", type=Path)
    conflicts_parser.add_argument("theirs", type=Path)
    
    args = parser.parse_args()
    
    if args.command == "merge":
        merger = ASTMerger()
        res = merger.merge_files(args.base, args.ours, args.theirs)
        if res.conflicts:
            print(f"Conflicts found: {len(res.conflicts)}")
            sys.exit(1)
        print(res.merged_source)
    elif args.command == "diff":
        pass  # implement later
    elif args.command == "conflicts":
        merger = ASTMerger()
        res = merger.merge_files(args.base, args.ours, args.theirs)
        for c in res.conflicts:
            print(c)

if __name__ == "__main__":
    main()
