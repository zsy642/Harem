from typing import Union, List
import random
from src.models import GameState, Concubine, Child, Item, Palace, Rank
import src.config as config


# ==========================================
# 第一阶段：世界的诞生与运转（基础核心）
# ==========================================

def init_new_game(family_name: str) -> GameState:
    """
    初始化并返回一个全新的游戏状态
    """
    state = GameState(family_name=family_name)

    # 从 config 加载静态预设
    state.palace_list = [Palace(**p) for p in config.INITIAL_PALACES]
    state.rank_list = [Rank(**r) for r in config.INITIAL_RANKS]
    state.item_list = [Item(**i) for i in config.INITIAL_ITEMS]
    state.available_travel_places = config.AVAILABLE_TRAVEL_PLACES.copy()
    state.picture_library = config.PICTURE_LIBRARY.copy()

    return state


def advance_to_next_day(state: GameState) -> dict:
    """
    时间驱动引擎：推进到次日，并执行每日/每月/每年结算
    """
    state.hour = 0
    state.day += 1

    result = {
        "success": True,
        "trigger_birth": False,
        "mother_ids": []  # 修复2：改为列表以支持多人同日生产
    }

    # --- 每日结算 ---
    for concubine in state.concubine_list:
        if concubine.health > 0 and concubine.pregnancy_days_remaining > 0:
            concubine.pregnancy_days_remaining -= 1
            if concubine.pregnancy_days_remaining == 0:
                result["trigger_birth"] = True
                result["mother_ids"].append(concubine.id)

    for child in state.child_list:
        if child.health > 0:
            child.age_days += 1

    # --- 每月结算 ---
    if state.day > config.DAYS_PER_MONTH:
        state.day = 1
        state.month += 1

    # --- 每年结算 ---
    if state.month > config.MONTHS_PER_YEAR:
        state.month = 1
        state.year += 1
        for item in state.item_list:
            item.quantity += config.YEARLY_ITEM_BONUS

    return result


# ==========================================
# 第二阶段：核心交互与数值变化（日常玩法）
# ==========================================

def interact_bedding(state: GameState, concubine_id: Union[str, int]) -> dict:
    """
    侍寝：消耗时间，增加宠爱经验，判定怀孕
    """
    # 1. 拦截校验：时间与生死
    if config.HOURS_PER_DAY - state.hour < config.INTERACT_COST_HOUR:
        return {"success": False, "msg": "时间不足，操作失败"}

    target = next((c for c in state.concubine_list if c.id == str(concubine_id)), None)
    if not target or target.health <= 0:
        return {"success": False, "msg": "目标状态异常或已故"}

    # 2. 消耗时间与增加属性
    state.hour += config.INTERACT_COST_HOUR
    target.favor += 20  # MVP固定增加宠爱20点
    target.experience += 1

    # 3. 怀孕判定
    is_pregnant = False
    if target.pregnancy_days_remaining == -1:
        # 掷骰子：0.0~1.0 之间的随机数小于怀孕概率则中奖
        if random.random() < target.pregnancy_rate:
            target.pregnancy_days_remaining = config.INITIAL_PREGNANCY_DAYS
            is_pregnant = True
            target.log.append({"time": f"{state.year}年{state.month}月", "event": "查出喜脉"})

    # 4. 记录日志与返回
    target.log.append({"time": f"{state.year}年{state.month}月", "event": "侍寝"})

    msg = "春宵一刻值千金。" + ("（太医禀报：娘娘有喜了！）" if is_pregnant else "")
    return {"success": True, "msg": msg, "is_pregnant": is_pregnant}


def interact_travel(state: GameState, companion_ids: List[Union[str, int]], location: str) -> dict:
    """
    游玩：消耗时间，群体增加好感
    """
    if config.HOURS_PER_DAY - state.hour < config.INTERACT_COST_HOUR:
        return {"success": False, "msg": "时间不足，操作失败"}

    state.hour += config.INTERACT_COST_HOUR

    # 将传来的ID列表转换为字符串以便比对
    str_ids = [str(cid) for cid in companion_ids]

    # 遍历后宫和子女，找对应的存活角色加好感
    for char in state.concubine_list + state.child_list:
        if char.id in str_ids and char.health > 0:
            char.favor += 15
            char.log.append({"time": f"{state.year}年{state.month}月", "event": f"同游{location}"})

    return {"success": True, "msg": f"与众人同游{location}，宾主尽欢。"}


def interact_gift(state: GameState, target_id: Union[str, int], item_name: str, is_child: bool = False) -> dict:
    """
    送礼：消耗物品不消耗时间
    """
    # 1. 查找物品并校验库存
    item = next((i for i in state.item_list if i.name == item_name), None)
    if not item or item.quantity <= 0:
        return {"success": False, "msg": "物品库存不足"}

    # 2. 确定目标并校验生死
    target_pool = state.child_list if is_child else state.concubine_list
    target = next((c for c in target_pool if c.id == str(target_id)), None)

    if not target or target.health <= 0:
        return {"success": False, "msg": "目标状态异常或已故"}

    # 3. 结算
    item.quantity -= 1
    target.favor += item.favor_bonus
    target.log.append({"time": f"{state.year}年{state.month}月", "event": f"获赠{item_name}"})

    return {"success": True, "msg": f"成功赏赐{item_name}。"}


def change_character_info(state: GameState, target_id: Union[str, int],
                          new_picture_id: str = None, new_title: str = None,
                          new_name: str = None, is_child: bool = False) -> bool:
    """
    统一的数据修改接口（供后期赐名、改立绘等使用）
    """
    target_pool = state.child_list if is_child else state.concubine_list
    target = next((c for c in target_pool if c.id == str(target_id)), None)

    if not target:
        return False

    if new_picture_id is not None:
        target.picture = new_picture_id
    if new_title is not None:
        target.title = new_title
    if new_name is not None:
        target.name = new_name

    return True


# ==========================================
# 第三阶段：生老病死与传承（生命周期 + 系统管理）
# ==========================================

def trigger_birth(state: GameState, mother_id: Union[str, int], child_name: str) -> Child:
    """生成新生儿属性，加入子女列表，返回新创建的 Child 对象"""
    mother = next((c for c in state.concubine_list if c.id == str(mother_id)), None)

    # 纯随机生成新生儿属性
    gender = random.choice(["男", "女"])
    intelligence = random.randint(30, 100)
    full_name = f"{state.family_name}{child_name}"

    # 生成唯一ID
    child_id = f"child_{state.year}_{state.month}_{len(state.child_list)}"

    new_child = Child(
        id=child_id,
        name=full_name,
        gender=gender,
        mother_id=str(mother_id),
        intelligence=intelligence,
        health=100,
        age_days=0,
        palace="重华宫",
        picture="default_c"  # 修复3：显式指定新生儿默认立绘
    )

    state.child_list.append(new_child)

    # 重华宫名单增加记录
    palace = next((p for p in state.palace_list if p.name == "重华宫"), None)
    if palace:
        palace.moved_list.append(child_id)

    if mother:
        mother.pregnancy_days_remaining = -1  # 修复1：重置怀孕状态，允许再次怀孕
        mother.log.append({"time": f"{state.year}年{state.month}月", "event": f"诞下皇嗣 {full_name}"})

    return new_child


def delete_character(state: GameState, target_id: Union[str, int]) -> dict:
    """将目标角色的 health 设为 0（死亡），从所属宫殿居住名单中移除并释放名额"""
    tid = str(target_id)

    # 先在妃嫔中找
    target = next((c for c in state.concubine_list if c.id == tid), None)
    if target:
        target.health = 0
        palace = next((p for p in state.palace_list if p.name == target.palace), None)
        if palace and tid in palace.moved_list:
            palace.moved_list.remove(tid)
        target.log.append({"time": f"{state.year}年{state.month}月", "event": "香消玉殒"})
        return {"success": True, "msg": f"{target.name} 已离世，处理完毕。"}

    # 再在子女中找
    target = next((c for c in state.child_list if c.id == tid), None)
    if target:
        target.health = 0
        palace = next((p for p in state.palace_list if p.name == target.palace), None)
        if palace and tid in palace.moved_list:
            palace.moved_list.remove(tid)
        target.log.append({"time": f"{state.year}年{state.month}月", "event": "不幸夭折"})
        return {"success": True, "msg": f"{target.name} 不幸夭折，处理完毕。"}

    # 修复4：最后在待选秀女中找（如果在选秀阶段赐死/删除）
    target = next((c for c in state.draft_pool if c.id == tid), None)
    if target:
        target.health = 0
        state.draft_pool.remove(target)
        return {"success": True, "msg": f"候选秀女 {target.name} 已被移除。"}

    return {"success": False, "msg": "未找到指定角色"}


def interact_abdicate(state: GameState, child_id: Union[str, int]) -> dict:
    """传位：检查目标子女是否存活且年龄满足条件，成功则修改状态"""
    child = next((c for c in state.child_list if c.id == str(child_id)), None)

    if not child or child.health <= 0:
        return {"success": False, "msg": "该子嗣不存在或已故。"}

    if child.age_days < config.ADULT_AGE_DAYS:
        return {"success": False, "msg": "该子嗣尚未成年（不足18岁），无法继承大统！"}

    # 满足条件，结束当前游戏
    state.current_state = "game_over"
    return {"success": True, "msg": f"你已成功传位于 {child.name}，新皇登基，天下大吉！"}


def generate_draft_candidates(state: GameState) -> List[Concubine]:
    """随机生成 3 名秀女存入 draft_pool（严格执行先遣散后生成的防坑指南）"""
    state.draft_pool.clear()

    surnames = ["富察", "乌拉那拉", "钮祜禄", "瓜尔佳", "佟佳", "马佳", "索绰罗", "叶赫那拉"]
    first_names = ["如兰", "明兰", "海棠", "秋月", "冬雪", "春花", "青樱", "玉娆", "陵容", "眉庄"]

    for i in range(3):
        cid = f"draft_tmp_{i}"
        name = random.choice(surnames) + random.choice(first_names)
        preg_rate = round(random.uniform(0.05, 0.25), 2)

        c = Concubine(
            id=cid,
            name=name,
            title="",
            rank="秀女",
            pregnancy_rate=preg_rate,
            palace="储秀宫"
        )
        state.draft_pool.append(c)

    return state.draft_pool


def accept_draft_candidate(state: GameState, candidate_id: Union[str, int], palace_name: str, rank_name: str) -> dict:
    """将选中的秀女移入正式后宫，分配宫殿和位分"""
    candidate = next((c for c in state.draft_pool if c.id == str(candidate_id)), None)
    if not candidate:
        return {"success": False, "msg": "候选人不存在或已被遣散。"}

    palace = next((p for p in state.palace_list if p.name == palace_name), None)
    if not palace:
        return {"success": False, "msg": "指定的宫殿不存在。"}

    if palace.capacity != -1 and len(palace.moved_list) >= palace.capacity:
        return {"success": False, "msg": f"【{palace_name}】已住满，请更换赐居宫殿。"}

    # 从待选池移除
    state.draft_pool.remove(candidate)

    # 分配正式 ID 及入宫数据
    new_id = f"con_{state.year}_{state.month}_{len(state.concubine_list)}"
    candidate.id = new_id
    candidate.rank = rank_name
    candidate.palace = palace_name
    candidate.log.append({"time": f"{state.year}年{state.month}月", "event": f"通过大选入宫，册封为{rank_name}"})

    # 正式加入队列并更新宫殿居住名单
    state.concubine_list.append(candidate)
    palace.moved_list.append(new_id)

    return {"success": True, "msg": f"成功将 {candidate.name} 册封为 {rank_name}，赐居 {palace_name}。"}