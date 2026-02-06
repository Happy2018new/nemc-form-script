# Running this file in NEMC.
# Make sure to operate in an already backed-up game save.
#
# Then, the console will output error that prefixed with
# `Check failed for entity`.
#
# What you need to do is that you have to correct all
# these error in step1_out_file_path.
#
# After you finished, copy the JSON and paste it to
# script/server/utils.py: ENTITY_ENGINE_TYPE_STR_TO_RAW_NAME


import json
from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId

step1_entity_out_file_path = "out_file_path.json"
fixed_entity_names_mapping = {
    "minecraft:thrown_trident",
    "minecraft:wither_skull_dangerous",
    "minecraft:dragon_fireball",
    "minecraft:falling_block",
    "minecraft:unknown",
    "minecraft:painting",
    "minecraft:ender_pearl",
    "minecraft:fireball",
    "minecraft:npc",
    "minecraft:tripod_camera",
    "minecraft:eye_of_ender_signal",
    "minecraft:lingering_potion",
    "minecraft:item",
    "minecraft:villager_v2",
    "minecraft:llama_spit",
    "minecraft:breeze_wind_charge_projectile",
    "minecraft:wither_skull",
    "minecraft:zombie_villager_v2",
    "minecraft:fishing_hook",
    "minecraft:area_effect_cloud",
    "minecraft:shulker_bullet",
    "minecraft:small_fireball",
    "minecraft:moving_block",
}
with open(step1_entity_out_file_path, "r+") as file:
    mapping = json.loads(file.read())  # type: dict[str, str]


command_comp_server = GetEngineCompFactory().CreateCommand(GetLevelId())
if not command_comp_server.SetCommand("difficulty normal"):
    raise Exception("Should never happened (mark 0)")
for engine_type_str, entity_raw_name in mapping.items():
    if command_comp_server.SetCommand("summon {} ~ -32767 ~".format(engine_type_str)):
        continue
    if engine_type_str in fixed_entity_names_mapping:
        continue
    print(
        "Check failed for entity {} which named {}".format(
            engine_type_str, entity_raw_name
        )
    )
if not command_comp_server.SetCommand("difficulty peaceful"):
    raise Exception("Should never happened (mark 1)")
_ = command_comp_server.SetCommand("kill @e[type=!player]")
