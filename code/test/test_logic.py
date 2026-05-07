import pytest
from code.models import GameState, Concubine, Child, Item, Palace, Rank
# 注意：在 logic.py 编写完成前，以下导入会报错，这是 TDD 的正常过程
from code.logic import (
    init_new_game,
    advance_to_next_day,
    interact_bedding,
    delete_character,
    interact_abdicate
)


@pytest.fixture
def basic_state():
    """创建一个基础的游戏状态用于测试"""
    state = init_new_game(family_name="慕容")
    # 手动添加一个妃子用于交互测试
    c = Concubine(id="c1", name="甄嬛", title="菀", rank="常在", palace="碎玉轩")
    state.concubine_list.append(c)
    # 为宫殿添加记录
    p = next((p for p in state.palace_list if p.name == "碎玉轩"), None)
    if p:
        p.moved_list.append("c1")
    return state


def test_init_game():
    """测试游戏初始化是否完整"""
    state = init_new_game(family_name="乌拉那拉")
    assert state.family_name == "乌拉那拉"
    assert state.year == 1
    assert state.month == 1
    assert state.day == 1
    assert state.hour == 0
    assert len(state.palace_list) > 0
    assert len(state.rank_list) > 0
    # 检查仓库是否初始化
    assert any(item.name == "玉佩" for item in state.item_list)


def test_time_progression(basic_state):
    """测试时间引擎的进位逻辑"""
    state = basic_state

    # 1. 跨天测试
    state.hour = 20
    advance_to_next_day(state)  # 消耗剩余时间并过夜
    assert state.day == 2
    assert state.hour == 0

    # 2. 跨月测试 (假设每月4天)
    state.day = 4
    advance_to_next_day(state)
    assert state.month == 2
    assert state.day == 1

    # 3. 跨年测试 (假设每年12月)
    state.month = 12
    state.day = 4
    # 跨年前记录一下物品数量
    yuhua_count = next(item.quantity for item in state.item_list if item.name == "玉佩")

    advance_to_next_day(state)
    assert state.year == 2
    assert state.month == 1

    # 4. 年结资产测试
    new_yuhua_count = next(item.quantity for item in state.item_list if item.name == "玉佩")
    assert new_yuhua_count == yuhua_count + 50


def test_bedding_logic(basic_state):
    """测试侍寝交互及其副作用"""
    state = basic_state
    concubine = state.concubine_list[0]

    # 正常侍寝
    state.hour = 0
    res = interact_bedding(state, concubine.id)
    assert res["success"] is True
    assert state.hour == 4
    assert concubine.experience == 1
    assert concubine.favor > 0

    # 时间不足拦截
    state.hour = 22
    res = interact_bedding(state, concubine.id)
    assert res["success"] is False
    assert "时间不足" in res["msg"]


def test_pregnancy_and_birth(basic_state):
    """测试怀孕流程"""
    state = basic_state
    concubine = state.concubine_list[0]

    # 强制设为怀孕
    concubine.pregnancy_days_remaining = 1

    # 推进一天触发生产
    res = advance_to_next_day(state)
    assert res["trigger_birth"] is True
    assert res["mother_id"] == concubine.id
    # 注意：此时 UI 应该弹出命名框，之后会调用 trigger_birth 逻辑


def test_death_logic(basic_state):
    """测试死亡清理逻辑"""
    state = basic_state
    concubine = state.concubine_list[0]
    palace_name = concubine.palace

    # 执行删除/赐死
    delete_character(state, concubine.id)

    assert concubine.health == 0
    # 检查是否从宫殿名单移除
    palace = next(p for p in state.palace_list if p.name == palace_name)
    assert concubine.id not in palace.moved_list

    # 检查死亡后不可侍寝
    res = interact_bedding(state, concubine.id)
    assert res["success"] is False


def test_abdication_requirements(basic_state):
    """测试传位条件"""
    state = basic_state
    # 创建一个未成年孩子
    child = Child(id="ch1", name="慕容承", gender="男", mother_id="c1", age_days=100)
    state.child_list.append(child)

    # 尝试传位 (未成年)
    res = interact_abdicate(state, "ch1")
    assert res["success"] is False

    # 设为成年 (864天)
    child.age_days = 864
    res = interact_abdicate(state, "ch1")
    assert res["success"] is True
    assert state.current_state == "game_over"