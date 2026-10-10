#!/usr/bin/env python3
from pathlib import Path
import re

project_root = Path(__file__).resolve().parent.parent
root = project_root / "week2"
output = project_root / "dist" / "0xgame2026-writeup-week2.md"

categories = [
    ("ai", "AI"),
    ("crypto", "Crypto"),
    ("misc", "Misc"),
    ("multi-class", "多分类"),
    ("osint", "Osint"),
    ("pwn", "Pwn"),
    ("reverse", "Reverse"),
    ("web", "Web"),
]

out = []

# 总标题
out.append("# 0xGame 2026 Week 2 Writeup")
out.append("")

for category, title in categories:
    category_dir = root / category

    if not category_dir.is_dir():
        continue

    # 方向标题
    out.append(f"## {title}")
    out.append("")

    # 找到所有包含 index.md 的题目目录
    challenges = [
        p for p in category_dir.iterdir()
        if p.is_dir()
        and not p.name.startswith("_")
        and (p / "index.md").is_file()
    ]

    # 数字题号按照数字排序，非数字目录放最后
    def challenge_key(p):
        if p.name.isdigit():
            return (0, int(p.name))
        return (2, p.name)

    challenges.sort(key=challenge_key)

    for challenge_dir in challenges:
        md = challenge_dir / "index.md"

        text = md.read_text(encoding="utf-8")
        lines = text.splitlines()

        # 去掉开头空行
        while lines and not lines[0].strip():
            lines.pop(0)

        # 第一行一级标题 -> 三级标题
        if lines and re.match(r"^#(?!#)\s+", lines[0]):
            lines[0] = re.sub(
                r"^#\s+",
                "### ",
                lines[0],
                count=2
            )
        else:
            # 如果没有一级标题，则使用目录名作为题目标题
            lines.insert(0, f"### {challenge_dir.name}")

        # 当前题目的目录
        base = f"../week2/{category}/{challenge_dir.name}"

        fixed_lines = []

        for line in lines:
            # 修正 Markdown 图片和链接的相对路径
            def replace_path(match):
                prefix = match.group(1)
                target = match.group(2)
                suffix = match.group(3)

                # 不处理 URL、绝对路径、锚点、data URI
                if target.startswith((
                    "http://",
                    "https://",
                    "/",
                    "#",
                    "data:"
                )):
                    return match.group(0)

                return f"{prefix}{base}/{target}{suffix}"

            line = re.sub(
                r"(!?\[[^\]]*\]\()([^)]+)(\))",
                replace_path,
                line
            )

            fixed_lines.append(line)

        out.extend(fixed_lines)
        out.append("")

# 写入文件
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    "\n".join(out),
    encoding="utf-8"
)

print(f"Generated: {output}")