from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class ReviewConfig:
    max_file_size_kb: int = 512
    fail_on: str = "high"
    include_extensions: List[str] = field(default_factory=lambda: [
        ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".cs", ".go", ".php", ".rb"
    ])
    exclude_dirs: List[str] = field(default_factory=lambda: [
        ".git", ".idea", ".vscode", "node_modules", "dist", "build", "target", "__pycache__", ".venv", "venv"
    ])

    @classmethod
    def load_default(cls) -> "ReviewConfig":
        return cls()

    def should_fail(self, severity: str) -> bool:
        order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        return order.get(severity, 0) >= order.get(self.fail_on, 3)
