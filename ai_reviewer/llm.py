import json
import os
from typing import List
from urllib import request, error
from .models import ReviewIssue


SYSTEM_PROMPT = """你是一个严格但务实的代码审查 Agent。
请只输出 JSON 数组，每个元素包含：line,severity,rule,message,suggestion。
severity 只能是 critical/high/medium/low/info。
重点关注：安全漏洞、异常处理、边界条件、可维护性、性能问题。
"""


def review_with_openai_compatible_api(file_path: str, language: str, code: str) -> List[ReviewIssue]:
    """Optional LLM reviewer using an OpenAI-compatible chat completions endpoint.

    Required env vars:
    - AI_REVIEW_API_KEY
    Optional env vars:
    - AI_REVIEW_BASE_URL, default: https://api.openai.com/v1/chat/completions
    - AI_REVIEW_MODEL, default: gpt-4o-mini
    """
    api_key = os.getenv("AI_REVIEW_API_KEY")
    if not api_key:
        return []

    url = os.getenv("AI_REVIEW_BASE_URL", "https://api.openai.com/v1/chat/completions")
    model = os.getenv("AI_REVIEW_MODEL", "gpt-4o-mini")

    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"文件：{file_path}\n语言：{language}\n代码：\n```{language}\n{code[:12000]}\n```"},
        ],
    }

    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=40) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "[]")
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.lower().startswith("json"):
            content = content[4:].strip()

    try:
        raw_issues = json.loads(content)
    except json.JSONDecodeError:
        return []

    issues: List[ReviewIssue] = []
    for item in raw_issues:
        issues.append(ReviewIssue(
            file=file_path,
            line=int(item.get("line", 1)),
            severity=str(item.get("severity", "info")).lower(),
            rule=str(item.get("rule", "llm-review")),
            message=str(item.get("message", "LLM 审查发现问题")),
            suggestion=str(item.get("suggestion", "")),
        ))
    return issues
