import pygame
from src import config
from src.logic import advance_to_next_day, interact_abdicate
from src.ui_manager.components import Button, draw_text

# 场景内持久化按钮
buttons = {}
# 传位选择模式标识
is_selecting_heir = False


def init_buttons(ui_mgr):
    """初始化基础交互按钮"""
    if "sleep" not in buttons:
        font = ui_mgr.fonts.get("normal")
        # 左侧功能按钮
        buttons["sleep"] = Button(100, 200, 200, 50, "处理朝政(睡觉)", font, (144, 238, 144))
        buttons["start_abdicate"] = Button(100, 270, 200, 50, "退位让贤", font, (255, 200, 100))
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", font)


def handle_event(event, state, ui_mgr):
    """处理养心殿事件"""
    global is_selecting_heir
    init_buttons(ui_mgr)

    if not event: return

    # 处理基础返回按钮
    if buttons["back"].is_clicked(event):
        if is_selecting_heir:
            is_selecting_heir = False  # 如果在选人模式，先退回预览模式
        else:
            state.current_state = "main"
        return

    # 1. 处理“睡觉”
    if buttons["sleep"].is_clicked(event):
        result = advance_to_next_day(state)

        # 检查是否有生产事件
        if result.get("trigger_birth"):
            # 将需要起名的母亲们存入管家的队列
            ui_mgr.birth_queue = result["mother_ids"]
            # 取出第一个开始起名
            first_mother = ui_mgr.birth_queue.pop(0)
            from . import naming_scene  # 延迟导入避免循环引用
            naming_scene.init_scene(ui_mgr, first_mother)
            # 切换状态
            state.current_state = "naming"

    # 2. 处理“传位”模式切换
    if buttons["start_abdicate"].is_clicked(event):
        is_selecting_heir = not is_selecting_heir
        return

    # 3. 在“传位”模式下，点击具体子嗣的交互（此处简单处理为点击区域）
    if is_selecting_heir and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = event.pos
        # 遍历所有子女，检测点击
        start_y = 200
        for i, child in enumerate(state.child_list):
            if child.health > 0 and child.age_days >= config.ADULT_AGE_DAYS:
                # 假设点击范围在右侧列表区域
                item_rect = pygame.Rect(450, start_y + i * 50, 400, 40)
                if item_rect.collidepoint(mouse_pos):
                    # 执行传位逻辑
                    res = interact_abdicate(state, child.id)
                    print(res["msg"])  # 控制台打印提示，状态会自动变为 game_over
                    break


def draw(screen, state, ui_mgr):
    """绘制养心殿"""
    init_buttons(ui_mgr)

    # 1. 背景与标题
    screen.fill((40, 40, 45))  # 庄严的深灰色
    font_title = ui_mgr.fonts.get("title")
    font_normal = ui_mgr.fonts.get("normal")

    draw_text(screen, "--- 养心殿 (皇帝寝宫) ---", font_title, config.GOLD, config.SCREEN_WIDTH // 2, 60, center=True)

    # 2. 左侧：绘制常用功能按钮
    buttons["sleep"].draw(screen)
    buttons["start_abdicate"].draw(screen)
    buttons["back"].draw(screen)

    # 3. 右侧：动态显示信息
    if not is_selecting_heir:
        # 普通模式：显示皇帝当前状态
        pygame.draw.rect(screen, (60, 60, 65), (450, 180, 500, 300))  # 信息面板
        pygame.draw.rect(screen, config.GOLD, (450, 180, 500, 300), 2)

        draw_text(screen, f"【万岁爷】", font_normal, config.GOLD, 480, 210)
        draw_text(screen, f"当前年份：第 {state.year} 年", font_normal, config.WHITE, 480, 260)
        draw_text(screen, f"当前月份：{state.month} 月", font_normal, config.WHITE, 480, 310)
        draw_text(screen, f"当前日期：第 {state.day} 日", font_normal, config.WHITE, 710, 260)
        draw_text(screen, f"当前时间：{state.hour}:00", font_normal, config.WHITE, 710, 310)
        draw_text(screen, f"子嗣总数：{len(state.child_list)} 人", font_normal, config.WHITE, 480, 360)
        draw_text(screen, "提示：点击左侧退位，选择已成年子嗣继承大统。", font_normal, config.GRAY, 480, 430)
    else:
        # 传位模式：显示可继承人列表
        draw_text(screen, "请选择继承人（需年满18岁/864天）：", font_normal, config.WHITE, 450, 160)

        start_y = 200
        eligible_count = 0
        for i, child in enumerate(state.child_list):
            y = start_y + i * 50
            rect = pygame.Rect(450, y, 400, 40)

            # 判断是否成年
            can_inherit = child.health > 0 and child.age_days >= config.ADULT_AGE_DAYS
            color = (100, 255, 100) if can_inherit else config.GRAY

            pygame.draw.rect(screen, (30, 30, 35), rect)
            pygame.draw.rect(screen, color, rect, 1)

            age_str = f"{child.age_days // 48}岁"
            draw_text(screen, f"{child.name} ({child.gender}) - {age_str}", font_normal, color, rect.x + 10, rect.y + 8)

            if can_inherit:
                draw_text(screen, "[ 点击传位 ]", font_normal, config.GOLD, rect.x + 280, rect.y + 8)
                eligible_count += 1

        if not state.child_list:
            draw_text(screen, "膝下暂无子嗣...", font_normal, config.GRAY, 450, 250)
        elif eligible_count == 0:
            draw_text(screen, "( 暂无成年的子嗣 )", font_normal, (200, 100, 100), 450,
                      start_y + len(state.child_list) * 50 + 20)