import sys
import json
from pathlib import Path


def collect_files(path: str) -> list[Path]:
    files: list[str] = []

    for i in Path(path).rglob("*"):
        if i.is_file() and i.suffix == ".txt":
            files.append(str(i))

    return [Path(i) for i in sorted(files)]


def remove_comments(path: str, code: str) -> str:
    ptr = 0
    ret = ""

    while True:
        if ptr >= len(code):
            break

        char = code[ptr]
        record = ptr
        ptr += 1

        if char == "'":
            while True:
                if ptr >= len(code):
                    break
                char = code[ptr]
                ptr += 1
                if char == "\\":
                    ptr += 1
                    continue
                if char == "'":
                    break
            ret = ret + code[record:ptr]
            continue

        if char != "/" or ptr >= len(code):
            ret = ret + char
            continue

        match code[ptr]:
            case "/":
                index = code.find("\n", ptr)
                ptr = index if index != -1 else len(code)
            case "*":
                index = code.find("*/", ptr)
                if index == -1:
                    raise Exception(f"Unexpected EOF on file {path}")
                ptr = index + 2
            case _:
                ret = ret + char

    return ret


def process_codes(name: str, path: str, code: str) -> str:
    code = "\n".join(code.splitlines())
    code = remove_comments(path, code)

    temp = code.splitlines()
    temp = [i.strip() for i in temp]
    temp = [i for i in temp if len(i) > 0]
    code = " | ".join(temp)

    name = json.dumps(name, ensure_ascii=False)
    return (
        f"customfunction remove {name}\n"
        + f"customfunction add {name} {json.dumps(code, ensure_ascii=False)}"
    )


def process_file(root: Path, path: Path) -> str:
    with open(path, "r+", encoding="utf-8") as file:
        code = file.read()

    prefix = len(root.parts)
    name = Path(*path.parts[prefix:])
    name = name.with_suffix("").as_posix()

    return process_codes(name, str(path), code)


def main(path: str, out: str) -> None:
    root = Path(path)
    result = [process_file(root, i) for i in collect_files(path)]

    final = Path(out)
    final = final.with_suffix(".mcfunction")
    final.parent.mkdir(parents=True, exist_ok=True)

    with open(final, "w+", encoding="utf-8") as file:
        file.write("\n".join(result))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("用法: python function.py <项目根目录> <输出文件>")
    main(sys.argv[1], sys.argv[2])
