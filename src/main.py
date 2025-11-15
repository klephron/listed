from pathspec import PathSpec
from pathlib import Path
from dataclasses import dataclass
import argparse
import sys


@dataclass
class Args:
    ignorefile: str
    exclusions: list[str]
    invert: bool


def parse_args(argv: list[str]):
    parser = argparse.ArgumentParser(
        description="List files with respect to ignore files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "ignorefile",
        nargs="?",
        type=str,
        default=".gitignore",
        help="Ignore file path",
    )
    parser.add_argument(
        "-e",
        dest="exclusions",
        action="append",
        type=str,
        default=[],
        help="Exclusion patterns (repeated)",
    )
    parser.add_argument(
        "-v",
        "--invert-match",
        action="store_true",
        default=False,
        help="Invert match",
    )

    args = parser.parse_args(argv[1:])

    return Args(
        ignorefile=args.ignorefile,
        exclusions=args.exclusions,
        invert=args.invert_match,
    )


def list_paths(args: Args):
    paths: list[Path] = []

    spec = PathSpec.from_lines(
        "gitwildmatch", Path(args.ignorefile).read_text().splitlines() + args.exclusions
    )

    for p in Path(".").rglob("*"):
        if not p.is_file():
            continue

        match = spec.match_file(str(p))

        if not args.invert:
            match = not match

        if match:
            paths.append(p)

    return paths


def print_paths(paths: list[Path]):
    for path in paths:
        print(str(path))


def main():
    args = parse_args(sys.argv)
    paths = list_paths(args)
    print_paths(paths)


if __name__ == "__main__":
    main()
