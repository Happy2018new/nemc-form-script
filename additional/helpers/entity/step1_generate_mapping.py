# Running this file under Python 3


import json

lang_file_path = "zh_CN.lang"
out_file_path = "out_file_path.json"
entity_mapping: dict[str, str] = {
    "minecraft:npc": "NPC",
}

with open(lang_file_path, "r+", encoding="utf-8") as file:
    lang_file_contents = file.read().splitlines()

for i in lang_file_contents:
    if not i.startswith("entity."):
        continue
    if not i.split("=")[0].endswith(".name"):
        continue

    engine_type_str = i.split("=")[0]
    engine_type_str = engine_type_str[7:-5]
    engine_type_str = engine_type_str.strip()
    engine_type_str = "minecraft:" + engine_type_str

    entity_raw_name = i.split("=")[1]
    entity_raw_name = entity_raw_name.replace("#", "")
    entity_raw_name = entity_raw_name.strip()

    entity_mapping[engine_type_str] = entity_raw_name

with open(out_file_path, "w+", encoding="utf-8") as file:
    result = json.dumps(entity_mapping, ensure_ascii=False, indent=4)
    file.write(result)
