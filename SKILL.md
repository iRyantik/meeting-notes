---
name: meeting-notes
description: Turn audio recordings or transcripts into structured meeting notes — briefing + Q&A, bilingual, with source verification.
---

# Meeting Notes

把音频或转录稿转化为结构化研究输出。两个模板：`briefing`（对外邮件）+ `qa`（对外问答实录）。

**零依赖**——不需要 buy-side-research-skills 插件。独立使用。

安装请参考 [install.md](install.md)。

## 原理

语音转文字稿有三个致命问题：
1. **名字全错**——语音识别乱写
2. **听不懂**——讲者默认听众有背景知识
3. **真假难辨**——数字、声明散落，没人验证

本 skill 做三件事：**纠正 → 补背景 → 挂 source**。

## 原则

- 内容深度完整优先，不设篇幅上限
- 事实直接陈述，不铺叙事层
- 英文原文全部翻译为中文
- 正文不挂验证标签——`[需查证]` 等仅出现在 appendix

## 触发场景

- "帮我整理这个会议纪要"
- "这段录音转文字帮我纠错"
- 粘贴语音转文字稿 + 要求结构化
- 直接给音频文件路径

## Step 0: 环境检查（仅音频输入，文本跳过）

```bash
python ~/.claude/skills/meeting-notes/scripts/install.py
```

whisper API key：从 `WHISPER_API_KEY` 环境变量读取。未配置时提示用户提供。

## Step 1: 音频转写（仅音频输入）

```
audio .mp3/.wav/.m4a
  ↓
① Language detection → 确认语言
  ↓
② Bitrate check：<32kbps → 提示提供高清版
  ↓
③ Split（>10min）：ffmpeg 切 ≤540s
  ↓
④ Transcribe：whisper-large-v3-turbo
  ↓
⑤ Merge → _verbatim.txt + _verbatim.json
```

调 `scripts/transcribe.py <audio> [lang] [model]`。

## Step 2: 预处理 → scratchpad

① 术语纠正 + 实体提取
② 背景注入（WebSearch 补核心信息）
③ 逐段读取，累积 scratchpad——不读到底绝不开写
④ 验证日志：每条 fact 挂 web search URL

## Step 3: 输出

### briefing 模板

```
# <会议主题>
> <日期> | <会议类型>

## 1. <Topic 1>
<prose>

## Company Profile
| Dimension | Detail |
|---|---|
| Company | |
| Ticker | |

## Claim Verification
| # | Claim | Source | Status |
|---|---|---|---|

## Name Corrections
| Transcript | Corrected |
|---|---|

## Follow-Up
- <item>
```

### qa 模板

```
# <会议主题> — Q&A
> <日期>

**Q1: ...**
A: ...

## Claim Verification
...
```

## 语言风格——禁止事项

| # | 禁止 |
|---|---|
| 1 | 叙事句开头（"管理层开场即给出"） |
| 2 | 英文引号原文 |
| 3 | 独立"关键点"段落 |
| 4 | 替读者下判断 |
| 5 | 修辞比喻（"皇冠明珠""护城河"） |
| 6 | 口语化措辞 |
| 7 | 对会议行为的元描述 |
| 8 | 程度副词（"远超""近乎垄断"） |

## 文件输出

```
当前目录/
├── YYYY-MM-DD-<call>_briefing_zh.md
├── YYYY-MM-DD-<call>_briefing_en.md    ← 可选
├── YYYY-MM-DD-<call>_qa_zh.md           ← 可选
└── .cache/meeting-notes/               ← 中间产物隐藏
```

## Resources

- `scripts/transcribe.py` — Whisper 转录
- `scripts/install.py` — 依赖安装
- `references/company-name-alias.yaml` — 公司名纠正词典
