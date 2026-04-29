import re
from pathlib import Path
from typing import List
from .models import ReviewIssue


SECRET_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}['\"]"), "疑似硬编码密钥或密码"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "疑似 AWS Access Key"),
    (re.compile(r"-----BEGIN (RSA|OPENSSH|DSA|EC) PRIVATE KEY-----"), "疑似私钥内容"),
]

DANGEROUS_CALLS = [
    ("eval(", "避免使用 eval，可能造成代码注入风险"),
    ("exec(", "避免使用 exec，可能造成代码注入风险"),
    ("os.system(", "避免直接调用 os.system，建议使用 subprocess 并校验参数"),
    ("subprocess.Popen(", "使用 subprocess.Popen 时需要注意 shell 注入风险"),
    ("shell=True", "shell=True 存在命令注入风险，除非必要请关闭"),
]


def run_builtin_rules(path: Path, text: str, rel_path: str) -> List[ReviewIssue]:
    issues: List[ReviewIssue] = []
    lines = text.splitlines()

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        for pattern, message in SECRET_PATTERNS:
            if pattern.search(line):
                issues.append(ReviewIssue(rel_path, idx, "critical", "secret-detection", message, "将敏感信息移动到环境变量或密钥管理服务中。"))

        for keyword, message in DANGEROUS_CALLS:
            if keyword in line:
                issues.append(ReviewIssue(rel_path, idx, "high", "dangerous-call", message, "增加输入校验，避免拼接用户输入，优先使用安全 API。"))

        if "TODO" in line or "FIXME" in line:
            issues.append(ReviewIssue(rel_path, idx, "info", "todo-marker", "存在 TODO/FIXME 标记", "确认是否需要在合并前处理。"))

        if len(line) > 120:
            issues.append(ReviewIssue(rel_path, idx, "low", "line-too-long", "单行代码超过 120 个字符", "建议拆分为多行，提高可读性。"))

        if stripped.startswith("print(") and path.suffix == ".py":
            issues.append(ReviewIssue(rel_path, idx, "low", "debug-print", "发现 print 调试输出", "生产代码建议使用 logging。"))

    text_lower = text.lower()
    if path.suffix in {".py", ".js", ".ts", ".java", ".cs"}:
        if "password" in text_lower and "hash" not in text_lower:
            issues.append(ReviewIssue(rel_path, 1, "medium", "password-handling", "文件中出现 password 相关逻辑，但未发现 hash 关键字", "确认密码是否经过哈希处理，不应明文存储。"))

    if path.suffix == ".py" and "except:" in text:
        line_no = next((i for i, l in enumerate(lines, start=1) if "except:" in l), 1)
        issues.append(ReviewIssue(rel_path, line_no, "medium", "bare-except", "发现裸 except", "建议捕获具体异常类型，避免吞掉重要错误。"))

    return issues
