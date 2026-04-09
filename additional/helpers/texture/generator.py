import json
from pathlib import Path

SCAN_PATH = "D:/MCStudioDownload/game/MinecraftPE_Netease/3.7.0.261178/data/resource_packs/vanilla/textures"
OUT_PATH = "additional/helpers/texture/texture_ids.json"


def collect_texture_ids(parent: Path) -> list[str]:
    result = []

    for file in parent.rglob("*"):
        if not file.is_file() or file.suffix.lower() != ".png":
            continue

        temp = len(parent.parts) - 1
        temp = file.parts[temp:]
        temp = Path(*temp).with_suffix("")

        result.append(temp.as_posix())

    return result


def main() -> None:
    with open(OUT_PATH, "w+", encoding="utf-8") as file:
        texture_ids = collect_texture_ids(Path(SCAN_PATH))
        result = json.dumps(texture_ids, ensure_ascii=False, indent=4)
        file.write(result)


main()
