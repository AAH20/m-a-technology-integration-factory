from __future__ import annotations

import argparse
import json
from pathlib import Path

from .factory import DealFactory
from .io import load_case


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an M&A integration or carve-out case")
    parser.add_argument("case")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = DealFactory().analyze(*load_case(args.case))
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
