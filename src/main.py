from typing import Any, Generator
from pathspec import PathSpec
from pathlib import Path
from dataclasses import dataclass
from src.__version import version
import argparse
import sys


@dataclass
class Params:
    ignorefile: str
    exclusions: list[str]
    invert: bool
    version: bool


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
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        default=False,
        help="Display version information and exit",
    )

    params = parser.parse_args(argv[1:])

    return Params(
        ignorefile=params.ignorefile,
        exclusions=params.exclusions,
        invert=params.invert_match,
        version=params.version,
    )


def yield_paths(params: Params):
    spec = PathSpec.from_lines(
        "gitwildmatch",
        Path(params.ignorefile).read_text().splitlines() + params.exclusions,
    )

    for p in Path(".").rglob("*"):
        if not p.is_file():
            continue

        match = spec.match_file(str(p))

        if not params.invert:
            match = not match

        if match:
            yield p


def print_paths(paths: list[Path] | Generator[Path, Any, None]):
    for path in paths:
        print(str(path))


def main():
    params = parse_args(sys.argv)

    if params.version:
        print(version)
        return

    paths = yield_paths(params)
    print_paths(paths)


if __name__ == "__main__":
    main()
