# Meeting Notes

> v1.0.0 | Claude Code Skill | Zero Dependencies

Turn audio recordings or transcripts into structured meeting notes — briefing + Q&A, bilingual, with source verification. Works standalone, no plugin required.

---

## Install

```
按照 https://github.com/iRyantik/meeting-notes/blob/main/install.md 安装 meeting-notes
```

One prompt. Agent auto-installs Python, dependencies, ffmpeg. Nothing manual.

---

## Use

```
整理这个会议纪要
这段录音转文字
```

Outputs:

- `YYYY-MM-DD-<call>_briefing_zh.md` — structured briefing
- `YYYY-MM-DD-<call>_briefing_en.md` — English (optional)
- `YYYY-MM-DD-<call>_qa_zh.md` — Q&A (optional)

---

## Requirements

- Claude Code (VS Code extension or CLI)
- WHISPER_API_KEY env var (for audio transcription only)

Everything else auto-installed on first use.
