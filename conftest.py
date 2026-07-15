import sys
from pathlib import Path

"""
Test-only path hack: add repository root to `sys.path` so tests
can import sibling packages when running from subdirectories.

Why this exists:
- Running `pytest` from nested test folders sets `sys.path[0]` to
	that folder, hiding the project root and causing `ModuleNotFoundError`.
- Mutating `sys.path` here keeps local developer experience simple
	(no repeated `pip install -e .`).

Tradeoffs and recommendations:
- This is a test-time convenience only. Do not rely on it in
	production code or as a substitute for proper packaging.
- CI and release pipelines should still install the package
	(`python -m pip install -e .`) to validate packaging and imports.
"""

# Find repository root by looking for pyproject.toml or .git
# _repo_start = Path(__file__).resolve().parent
# _repo_root = None
# for p in (_repo_start,) + tuple(_repo_start.parents):
# 		if (p / "pyproject.toml").exists() or (p / ".git").exists():
# 				_repo_root = p
# 				break
# if _repo_root is None:
# 		_repo_root = _repo_start
# if str(_repo_root) not in sys.path:
# 		sys.path.insert(0, str(_repo_root))

from config.logging_config import configure_logging

# Configure logging early during pytest collection so tests show logs.
configure_logging("DEBUG", force=True)