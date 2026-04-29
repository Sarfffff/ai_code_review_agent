import argparse
import sys
from pathlib import Path
from .config import ReviewConfig
from .reviewer import review_project
from .report import save_report, to_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="AI 自动代码审查 Agent")
    parser.add_argument("path", nargs="?", default=".", help="要审查的项目目录")
    parser.add_argument("--ai", action="store_true", help="启用大模型审查，需要配置 AI_REVIEW_API_KEY")
    parser.add_argument("--output", default="review_report.md", help="报告输出路径")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="报告格式")
    parser.add_argument("--fail-on", choices=["critical", "high", "medium", "low", "info"], default="high", help="达到该级别时返回非 0 状态码")
    args = parser.parse_args()

    config = ReviewConfig.load_default()
    config.fail_on = args.fail_on

    report = review_project(Path(args.path), use_ai=args.ai, config=config)
    output = Path(args.output)
    save_report(report, output, args.format)
    print(to_markdown(report))
    print(f"\n报告已保存：{output.resolve()}")

    return 1 if any(config.should_fail(issue.severity) for issue in report.issues) else 0


if __name__ == "__main__":
    sys.exit(main())
