import pygame
from src import config
from src.logic import init_new_game
from src.ui_manager.components import Button, draw_text

buttons = {}


def init_buttons(ui_mgr):
    """初始化大结局界面的按钮"""
    if "restart" not in buttons:
        font = ui_mgr.fonts.get("normal")
        # 居中放置重新开始按钮
        btn_w, btn_h = 200, 60
        btn_x = (config.SCREEN_WIDTH - btn_w) // 2
        btn_y = config.SCREEN_HEIGHT - 150
        buttons["restart"] = Button(btn_x, btn_y, btn_w, btn_h, "开启新朝代", font, (144, 238, 144))


def handle_event(event, state, ui_mgr):
    """处理大结局事件"""
    init_buttons(ui_mgr)

    if not event: return

    # 点击重新开始按钮
    if buttons["restart"].is_clicked(event):
        # 1. 彻底清空大管家的状态缓存
        from . import main_scene, harem_scene, warehouse_scene, draft_scene, emperor_palace_scene, palace_scene, \
            child_scene, travel_scene

        # 这里的强硬清理是为了防止上一个档的按钮缓存带到下一个档
        for module in [main_scene, harem_scene, warehouse_scene, draft_scene, emperor_palace_scene, palace_scene,
                       child_scene, travel_scene]:
            if hasattr(module, 'buttons'): module.buttons.clear()
            if hasattr(module, 'action_buttons'): module.action_buttons.clear()
            if hasattr(module, 'candidate_buttons'): module.candidate_buttons.clear()

        # 2. 调用核心逻辑，生成全新的 GameState，覆盖原有的 state
        # 假设下一代还是姓慕容，或者你之后可以在这里加个起姓氏的输入框
        new_state = init_new_game(family_name=state.family_name) #TODO:实现玩家输入名字和持久化存储
        ui_mgr.state = new_state

        # 3. 回到主界面
        ui_mgr.state.current_state = "main"


def draw(screen, state, ui_mgr):
    """绘制大结局界面"""
    init_buttons(ui_mgr)

    # 用深邃的暗红色作为大结局背景
    screen.fill((30, 10, 10))
    font_title = ui_mgr.fonts.get("title")
    font_normal = ui_mgr.fonts.get("normal")

    # 1. 绘制大标题
    draw_text(screen, "✦ 新皇登基 ✦", font_title, config.GOLD, config.SCREEN_WIDTH // 2, 100, center=True)
    draw_text(screen, "先帝已退位让贤，一代传奇就此落幕。", font_normal, config.WHITE, config.SCREEN_WIDTH // 2, 180,
              center=True)

    # 2. 绘制王朝统计数据面板
    panel_w, panel_h = 600, 300
    panel_x = (config.SCREEN_WIDTH - panel_w) // 2
    panel_y = 250
    pygame.draw.rect(screen, (50, 20, 20), (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(screen, config.GOLD, (panel_x, panel_y, panel_w, panel_h), 2)

    stats_x = config.SCREEN_WIDTH // 2
    draw_text(screen, f"【{state.family_name}氏王朝·先帝实录】", font_normal, config.GOLD, stats_x, panel_y + 40,
              center=True)

    # 统计后宫人数
    alive_concubines = len([c for c in state.concubine_list if c.health > 0])
    draw_text(screen, f"在位时间： {state.year} 年 {state.month} 个月", font_normal, config.WHITE, stats_x,
              panel_y + 100, center=True)
    draw_text(screen, f"后宫佳丽： {len(state.concubine_list)} 人 (在世 {alive_concubines} 人)", font_normal,
              config.WHITE, stats_x, panel_y + 150, center=True)

    # 统计子嗣人数
    alive_children = len([c for c in state.child_list if c.health > 0])
    draw_text(screen, f"膝下子嗣： {len(state.child_list)} 人 (在世 {alive_children} 人)", font_normal, config.WHITE,
              stats_x, panel_y + 200, center=True)

    # 评价
    evaluation = "平平无奇"
    if state.year > 20 and alive_children >= 10:
        evaluation = "千古一帝，多子多福！"
    elif state.year > 10:
        evaluation = "勤政爱民，中规中矩。"
    elif alive_children == 0:
        evaluation = "后继无人，令人唏嘘..."

    draw_text(screen, f"史官评价： {evaluation}", font_normal, config.GOLD, stats_x, panel_y + 260, center=True)

    # 3. 绘制重开按钮
    buttons["restart"].draw(screen)
