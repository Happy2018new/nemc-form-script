# -*- coding: utf-8 -*-

try:
    from hashlib import md5
except Exception:
    import _md5  # type: ignore

    md5 = _md5.new  # type: ignore

import json
from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId

ENTITY_ENGINE_TYPE_STR_TO_RAW_NAME = {
    "minecraft:npc": "NPC",
    "minecraft:area_effect_cloud": "区域效果云",
    "minecraft:armadillo": "犰狳",
    "minecraft:armor_stand": "盔甲架",
    "minecraft:arrow": "箭",
    "minecraft:bat": "蝙蝠",
    "minecraft:bee": "蜜蜂",
    "minecraft:blaze": "烈焰人",
    "minecraft:boat": "船",
    "minecraft:bogged": "沼骸",
    "minecraft:breeze": "旋风人",
    "minecraft:breeze_wind_charge_projectile": "风弹",
    "minecraft:cat": "猫",
    "minecraft:cave_spider": "洞穴蜘蛛",
    "minecraft:chicken": "鸡",
    "minecraft:cow": "牛",
    "minecraft:creaking": "嘎枝",
    "minecraft:creeper": "苦力怕",
    "minecraft:dolphin": "海豚",
    "minecraft:goat": "山羊",
    "minecraft:panda": "熊猫",
    "minecraft:donkey": "驴",
    "minecraft:dragon_fireball": "末影龙火球",
    "minecraft:drowned": "溺尸",
    "minecraft:egg": "掷出的鸡蛋",
    "minecraft:elder_guardian": "远古守卫者",
    "minecraft:ender_crystal": "末地水晶",
    "minecraft:ender_dragon": "末影龙",
    "minecraft:enderman": "末影人",
    "minecraft:endermite": "末影螨",
    "minecraft:ender_pearl": "掷出的末影珍珠",
    "minecraft:evocation_illager": "唤魔者",
    "minecraft:evocation_fang": "唤魔者尖牙",
    "minecraft:eye_of_ender_signal": "末影之眼",
    "minecraft:falling_block": "下落的方块",
    "minecraft:fireball": "火球",
    "minecraft:fireworks_rocket": "烟花火箭",
    "minecraft:fishing_hook": "浮漂",
    "minecraft:fox": "狐狸",
    "minecraft:cod": "鳕鱼",
    "minecraft:pufferfish": "河豚",
    "minecraft:salmon": "鲑鱼",
    "minecraft:tropicalfish": "热带鱼",
    "minecraft:axolotl": "美西螈",
    "minecraft:ghast": "恶魂",
    "minecraft:glow_squid": "发光鱿鱼",
    "minecraft:piglin_brute": "猪灵蛮兵",
    "minecraft:guardian": "守卫者",
    "minecraft:hoglin": "疣猪兽",
    "minecraft:horse": "马",
    "minecraft:husk": "尸壳",
    "minecraft:ravager": "劫掠兽",
    "minecraft:iron_golem": "铁傀儡",
    "minecraft:item": "物品",
    "minecraft:leash_knot": "拴绳结",
    "minecraft:lightning_bolt": "闪电束",
    "minecraft:lingering_potion": "滞留药水",
    "minecraft:llama": "羊驼",
    "minecraft:trader_llama": "行商羊驼",
    "minecraft:llama_spit": "羊驼唾沫",
    "minecraft:magma_cube": "岩浆怪",
    "minecraft:minecart": "矿车",
    "minecraft:chest_minecart": "运输矿车",
    "minecraft:command_block_minecart": "命令方块矿车",
    "minecraft:hopper_minecart": "漏斗矿车",
    "minecraft:tnt_minecart": "TNT 矿车",
    "minecraft:mule": "骡",
    "minecraft:mooshroom": "哞菇",
    "minecraft:moving_block": "移动的方块",
    "minecraft:ocelot": "豹猫",
    "minecraft:painting": "画",
    "minecraft:parrot": "鹦鹉",
    "minecraft:phantom": "幻翼",
    "minecraft:pig": "猪",
    "minecraft:piglin": "猪灵",
    "minecraft:pillager": "掠夺者",
    "minecraft:polar_bear": "北极熊",
    "minecraft:rabbit": "兔子",
    "minecraft:sheep": "绵羊",
    "minecraft:shulker": "潜影贝",
    "minecraft:shulker_bullet": "潜影弹",
    "minecraft:silverfish": "蠹虫",
    "minecraft:skeleton": "骷髅",
    "minecraft:skeleton_horse": "骷髅马",
    "minecraft:stray": "流浪者",
    "minecraft:slime": "史莱姆",
    "minecraft:small_fireball": "小火球",
    "minecraft:sniffer": "嗅探兽",
    "minecraft:snowball": "雪球",
    "minecraft:snow_golem": "雪傀儡",
    "minecraft:spider": "蜘蛛",
    "minecraft:splash_potion": "药水",
    "minecraft:squid": "鱿鱼",
    "minecraft:strider": "炽足兽",
    "minecraft:tnt": "被激活的 TNT",
    "minecraft:thrown_trident": "三叉戟",
    "minecraft:tripod_camera": "摄像机",
    "minecraft:turtle": "海龟",
    "minecraft:unknown": "未知",
    "minecraft:vex": "恼鬼",
    "minecraft:villager": "村民",
    "minecraft:villager_v2": "村民",
    "minecraft:vindicator": "卫道士",
    "minecraft:wandering_trader": "流浪商人",
    "minecraft:wind_charge_projectile": "风弹",
    "minecraft:witch": "女巫",
    "minecraft:wither": "凋灵",
    "minecraft:wither_skeleton": "凋灵骷髅",
    "minecraft:wither_skull": "凋灵之首",
    "minecraft:wither_skull_dangerous": "凋灵之首",
    "minecraft:wolf": "狼",
    "minecraft:xp_orb": "经验球",
    "minecraft:xp_bottle": "掷出的附魔之瓶",
    "minecraft:zoglin": "僵尸疣猪兽",
    "minecraft:zombie": "僵尸",
    "minecraft:zombie_horse": "僵尸马",
    "minecraft:zombie_pigman": "僵尸猪灵",
    "minecraft:zombie_villager": "僵尸村民",
    "minecraft:zombie_villager_v2": "僵尸村民",
    "minecraft:frog": "青蛙",
    "minecraft:tadpole": "蝌蚪",
    "minecraft:warden": "监守者",
    "minecraft:allay": "悦灵",
    "minecraft:chest_boat": "运输船",
    "minecraft:camel": "骆驼",
}


def compute_md5(data):  # type: (bytes) -> bytes
    """compute_md5 计算给定数据的 MD5 摘要值

    Args:
        data (bytes): 给定的数据

    Returns:
        bytes: 给定数据的 MD5 摘要值
    """
    result = md5(data).digest()
    return result


def disconnect_player(player_id, reason):  # type: (str, str) -> None
    """
    disconnect_player 断开玩家与服务器的连接

    Args:
        player_id (str): 目标玩家的 ID
        reason (str): 断开连接的原因
    """
    engine_comp = GetEngineCompFactory()

    player_name = engine_comp.CreateName(player_id).GetName()
    if player_name is None:
        return

    _ = engine_comp.CreateCommand(GetLevelId()).SetCommand(
        "kick {} {}".format(
            json.dumps(player_name, ensure_ascii=False),
            reason,
        ),
        player_id,
        False,
    )


def filter_user_word(sentence):  # type: (str) -> str
    """
    filter_user_word 过滤 sentence 中的敏感词。
    当 sentence 中存在敏感词时，将直接返回 `***`

    Args:
        sentence (str): 欲过滤的句子

    Returns:
        str: sentence 的安全化表示
    """
    if GetEngineCompFactory().CreateGame(GetLevelId()).CheckWordsValid(sentence):
        return sentence
    return "***"


def get_entity_name(entity_id):  # type: (str) -> str
    """get_entity_name 返回给定实体的显示名称

    Args:
        entity_id (str): 欲获取名称的实体 ID

    Returns:
        str: 目标实体的显示名称
    """
    comp = GetEngineCompFactory()

    custom_name = comp.CreateName(entity_id).GetName()
    if custom_name is not None:
        return custom_name

    engine_type = comp.CreateEngineType(entity_id).GetEngineTypeStr()
    if engine_type != "minecraft:item":
        if engine_type in ENTITY_ENGINE_TYPE_STR_TO_RAW_NAME:
            return ENTITY_ENGINE_TYPE_STR_TO_RAW_NAME[engine_type]
        return engine_type

    item_comp = comp.CreateItem(entity_id)
    item_data = item_comp.GetDroppedItem(entity_id, True)
    custom_name = item_comp.GetCustomName(item_data)

    if len(custom_name) > 0:
        return custom_name
    else:
        item_info = (
            GetEngineCompFactory()
            .CreateItem(GetLevelId())
            .GetItemBasicInfo(item_data["newItemName"], item_data["newAuxValue"], False)
        )
        return item_info["itemName"]
