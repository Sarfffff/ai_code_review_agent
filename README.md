# AI 自动代码审查 Agent

这是一个可直接上传到 GitHub 的本地代码审查 Agent。它可以扫描项目源码，发现常见安全风险、可维护性问题、调试残留、TODO 标记、过长代码行等，并生成 Markdown 或 JSON 审查报告。

项目默认只使用 Python 标准库，无需第三方依赖。你也可以通过 OpenAI 兼容接口接入真实大模型审查。

## 功能

- 扫描 Python、JavaScript、TypeScript、Java、C/C++、C#、Go、PHP、Ruby 等源码文件
- 内置规则审查：硬编码密钥、危险函数、裸 except、调试输出、TODO/FIXME、超长代码行等
- 可选大模型审查：通过环境变量配置 API Key
- 输出 Markdown / JSON 报告
- 支持 GitHub Actions 自动审查
- 结构清晰，适合作为课程设计、毕业设计或 GitHub 开源项目基础版

## 项目结构

```text
ai_code_review_agent/
├── ai_reviewer/
│   ├── cli.py          # 命令行入口
│   ├── config.py       # 审查配置
│   ├── llm.py          # 可选大模型审查接口
│   ├── models.py       # 数据模型
│   ├── report.py       # 报告生成
│   ├── reviewer.py     # 审查流程
│   └── rules.py        # 内置规则
├── examples/
│   └── sample_project/ # 示例待审查项目
├── .github/workflows/  # GitHub Actions
├── main.py
├── requirements.txt
└── README.md
```

## 快速开始

```bash
cd ai_code_review_agent
python main.py examples/sample_project --output review_report.md
```

输出 JSON：

```bash
python main.py examples/sample_project --format json --output review_report.json
```

启用 AI 审查：

```bash
set AI_REVIEW_API_KEY=你的密钥
python main.py examples/sample_project --ai --output review_report.md
```

macOS / Linux：

```bash
export AI_REVIEW_API_KEY=你的密钥
python main.py examples/sample_project --ai --output review_report.md
```

## GitHub Actions 使用

项目已包含 `.github/workflows/code-review.yml`。上传到 GitHub 后，每次 push 或 pull request 都会自动运行审查，并把报告作为 artifact 保存。

如需在 GitHub Actions 中启用 AI 审查，可以在仓库 Settings → Secrets and variables → Actions 中添加：

- `AI_REVIEW_API_KEY`

然后修改 workflow 命令，加上 `--ai`。

## 可扩展方向

你可以继续增加：

- AST 级别代码分析
- Pull Request 评论机器人
- Web 可视化界面
- 更多语言规则
- 与 SonarQube、ESLint、Pylint 等工具集成
- 自动修复建议和补丁生成

## 适合写进简历的项目描述

基于 Python 实现 AI 自动代码审查 Agent，支持多语言源码扫描、规则引擎检测、安全风险识别、Markdown/JSON 报告生成，并预留大模型审查接口；项目集成 GitHub Actions，可在 Pull Request 阶段自动执行代码质量检查，提高团队代码审查效率。
