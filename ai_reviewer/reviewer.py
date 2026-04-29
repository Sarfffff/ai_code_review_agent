from pathlib import Path
from .config import ReviewConfig
from .models import ReviewReport, FileReview
from .scanner import iter_source_files, detect_language
from .rules import run_builtin_rules
from .llm import review_with_openai_compatible_api


def review_project(root: Path, use_ai: bool = False, config: ReviewConfig | None = None) -> ReviewReport:
    config = config or ReviewConfig.load_default()
    root = root.resolve()
    file_reviews: list[FileReview] = []
    all_issues = []

    for path in iter_source_files(root, config):
        rel = str(path.relative_to(root)).replace("\\", "/")
        language = detect_language(path)
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        issues = run_builtin_rules(path, text, rel)
        if use_ai:
            issues.extend(review_with_openai_compatible_api(rel, language, text))

        metrics = {
            "lines": len(text.splitlines()),
            "size_kb": round(path.stat().st_size / 1024, 2),
        }
        file_review = FileReview(path=rel, language=language, issues=issues, metrics=metrics)
        file_reviews.append(file_review)
        all_issues.extend(issues)

    return ReviewReport(str(root), len(file_reviews), all_issues, file_reviews)
