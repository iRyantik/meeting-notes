# Meeting Notes — 安装指南

你是 Claude Code agent。把 meeting-notes skill 装好。

用户只需说：

```
按照 https://github.com/iRyantik/meeting-notes/blob/main/install.md 安装 meeting-notes
```

---

## Step 1: 确保 Python 可用

```bash
python --version
```

报错 `command not found` → 自动装：

**Windows**：`winget install Python.Python.3.12 --silent --accept-package-agreements`。装完把 `%LOCALAPPDATA%\Programs\Python\Python312` 加入 PATH。

**macOS**：`brew install python`

---

## Step 2: 下载并安装 skill

```bash
python -c "
import urllib.request, zipfile, io, shutil
from pathlib import Path

# Try direct, fallback to mirror
urls = [
    'https://api.github.com/repos/iRyantik/meeting-notes/zipball/main',
    'https://ghproxy.com/https://api.github.com/repos/iRyantik/meeting-notes/zipball/main',
]
data = None
for url in urls:
    try:
        with urllib.request.urlopen(url, timeout=30) as r: data = r.read()
        print(f'Downloaded from {url[:40]}...')
        break
    except Exception as e:
        print(f'Failed: {url[:50]}... ({e})')
if not data:
    print('All URLs failed. Download manually from https://github.com/iRyantik/meeting-notes and extract to ~/.claude/skills/meeting-notes/')
    exit(1)

tmp = Path.home() / '.claude' / 'skills' / '_tmp_meeting_notes'
shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
with zipfile.ZipFile(io.BytesIO(data)) as z: z.extractall(tmp)
dst = Path.home() / '.claude' / 'skills' / 'meeting-notes'
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(next(tmp.iterdir()), dst)
shutil.rmtree(tmp, ignore_errors=True)
print('Skill installed')
"
```

---

## Step 3: 安装依赖

```bash
python ~/.claude/skills/meeting-notes/scripts/install.py
```

（幂等——已装的跳过。ffmpeg 约 70MB，仅在需要音频转写时下载）

---

## 安装完成

按 `/` → 查找 `meeting-notes`。能用 → 成功。

音频转写需配置 `WHISPER_API_KEY` 环境变量。
