#!/usr/bin/env python3
"""Git helpers for comparing current files to previous revisions."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

if __package__ in (None, ""):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import repo_root, run_command  # type: ignore
else:
    from ._common import repo_root, run_command


def previous_file_content(path: Path) -> Optional[str]:
    root = repo_root(path.parent)
    rel = path.resolve().relative_to(root)
    result = run_command(["git", "show", f"HEAD~1:{rel.as_posix()}"], cwd=root)
    if result.returncode != 0:
        return None
    return result.stdout
