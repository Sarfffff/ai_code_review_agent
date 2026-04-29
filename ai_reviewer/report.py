import json
from pathlib import Path
from .models import ReviewReport


def to_markdown(report: ReviewReport) -> str:
    summary = report.summary()
    lines = [
        "# AI 自动代码审查报告",
        "",
        f"- 项目路径：`{report.project_root}`",
        f"- 审查文件数：{report.files_reviewed}",
        f"- 问题总数：{len(report.issues)}",
        f"- 严重程度统计：critical={summary.get('critical', 0)}, high={summary.get('high', 0)}, medium={summary.get('medium', 0)}, low={summary.get('low', 0)}, info={summary.get('info', 0)}",
        "",
    ]

    if not report.issues:
        lines.append("未发现明显问题。")
        return "\n".join(lines)

    lines.extend(["## 问题列表", ""])
    for i, issue in enumerate(report.issues, start=1):
        lines.extend([
            f"### {i}. [{issue.severity.upper()}] {issue.file}:{issue.line}",
            f"- 规则：`{issue.rule}`",
            f"- 问题：{issue.message}",
            f"- 建议：{issue.suggestion or '请结合上下文确认。'}",
            "",
        ])
    return "\n".join(lines)


def to_json(report: ReviewReport) -> str:
    return json.dumps({
        "project_root": report.project_root,
        "files_reviewed": report.files_reviewed,
        "summary": report.summary(),
        "issues": [issue.__dict__ for issue in report.issues],
        "files": [
            {
                "path": f.path,
                "language": f.language,
                "metrics": f.metrics,
                "issues": [issue.__dict__ for issue in f.issues],
            }
            for f in report.file_reviews
        ],
    }, ensure_ascii=False, indent=2)


def save_report(report: ReviewReport, output: Path, fmt: str = "markdown") -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        output.write_text(to_json(report), encoding="utf-8")
    else:
        output.write_text(to_markdown(report), encoding="utf-8")
