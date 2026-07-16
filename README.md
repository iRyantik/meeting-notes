# Meeting Notes

> v1.0.0 | Claude Code Skill | 零依赖

把音频或转录稿转化为结构化会议纪要——briefing + Q&A，双语，源验证。独立使用，不需要 buy-side-research-skills 插件。

---

## 安装

**前提（仅需一次）**：`~/.claude/settings.json` 中加 `"skipWebFetchPreflight": true`，重启 CC。

```
按照 https://github.com/iRyantik/meeting-notes/blob/main/install.md 安装 meeting-notes
```

一句话。Agent 自动装 Python、依赖、ffmpeg。

---

## 使用

```
整理这个会议纪要
这段录音转文字
```

输出：

- `YYYY-MM-DD-<call>_briefing_zh.md` — 结构化 briefing
- `YYYY-MM-DD-<call>_briefing_en.md` — 英文版（可选）
- `YYYY-MM-DD-<call>_qa_zh.md` — Q&A（可选）

---

## 要求

- Claude Code（VS Code 扩展或 CLI）
- WHISPER_API_KEY 环境变量（仅音频转写需要，文本输入不需要）

其他所有依赖首次使用时自动安装。
