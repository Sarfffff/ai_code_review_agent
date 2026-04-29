from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class ReviewIssue:
    file: str
    line: int
    severity: str
    rule: str
    message: str
    suggestion: str = ""


@dataclass
class FileReview:
    path: str
    language: str
    issues: List[ReviewIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewReport:
    project_root: str
    files_reviewed: int
    issues: List[ReviewIssue]
    file_reviews: List[FileReview]

    def summary(self) -> Dict[str, int]:
        data = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for issue in self.issues:
            data[issue.severity] = data.get(issue.severity, 0) + 1
        return data
