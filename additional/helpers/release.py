"""
把项目中所有 `if TYPE_CHECKING:` 代码块里的每一行变成双引号字符串
"""

import sys
import re
from pathlib import Path
from typing import List

# 匹配  if TYPE_CHECKING:  及其下方整个缩进块
TYPE_CHECKING_RE = re.compile(
    r"""
    (?P<indent>^[ \t]*)          # 行首缩进
    if\s+TYPE_CHECKING\s*:\s*$\n #  if TYPE_CHECKING:  行
    (?P<body>(?:\1[ \t].*\n?)*)  # 和它下面所有再多缩进一层的内容
    """,
    re.MULTILINE | re.VERBOSE,
)


def process_file(py_file: Path) -> bool:
    """处理单个 .py 文件，返回是否做了修改"""
    content = py_file.read_text(encoding="utf-8")
    new_content = TYPE_CHECKING_RE.sub(_replacer, content)
    if new_content != content:
        py_file.write_text(new_content, encoding="utf-8")
        return True
    return False


def _replacer(match: re.Match) -> str:
    indent, body = match.group("indent", "body")
    out_lines = [f"{indent}if TYPE_CHECKING:"]
    for line in body.splitlines():
        # 去掉行首行尾空白，再用双引号包裹
        stripped = line.strip()
        out_lines.append(f'{indent}    "{stripped}"')
    # 最后补一个换行，让块结束后有空行
    out_lines.append("")
    return "\n".join(out_lines)


def main(root: Path) -> None:
    if not root.is_dir():
        sys.exit(f"{root} 不是有效目录")
    changed: List[Path] = []
    for py in root.rglob("*.py"):
        try:
            if process_file(py):
                changed.append(py)
        except Exception as e:
            print(f"跳过 {py}: {e}", file=sys.stderr)

    if changed:
        print("已处理文件:")
        for p in changed:
            print("  ", p)
    else:
        print("未找到需要处理的文件。")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("用法: python release_typing_fixer.py <项目根目录>")
    main(Path(sys.argv[1]).expanduser().resolve())
