from pathlib import Path
from typing import Iterable
from .config import ReviewConfig


def iter_source_files(root: Path, config: ReviewConfig) -> Iterable[Path]:
    root = root.resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.relative_to(root).parts)
        if any(excluded in parts for excluded in config.exclude_dirs):
            continue
        if path.suffix.lower() not in config.include_extensions:
            continue
        if path.stat().st_size > config.max_file_size_kb * 1024:
            continue
        yield path


def detect_language(path: Path) -> str:
    mapping = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".java": "Java",
        ".cpp": "C++", ".c": "C", ".h": "C/C++ Header", ".cs": "C#", ".go": "Go",
        ".php": "PHP", ".rb": "Ruby"
    }
    return mapping.get(path.suffix.lower(), "Unknown")
