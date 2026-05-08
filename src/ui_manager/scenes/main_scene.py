import pygame
from src import config
from src.models import GameState
from src.logic import advance_to_next_day
from src.ui_manager.components import Button

buttons = {}


def init_buttons(ui_mgr):
    """延迟初始化，确保字体已加载"""
    if buttons: return
    font = ui_mgr.fonts.get("normal")
    cx = config.SCREEN_WIDTH // 2

    # 建立四个导航按钮
    buttons["sleep"] = Button(cx - 100, 250, 200, 50, "睡觉(进入次日)", font, bg_color=(144, 238, 144))
    buttons["harem"] = Button(cx - 100, 320, 200, 50, "后宫寝殿", font)
    buttons["warehouse"] = Button(cx - 100, 390, 200, 50, "内务府(仓库)", font)
    buttons["draft"] = Button(cx - 100, 460, 200, 50, "大选秀女", font, bg_color=(255, 192, 203))


def handle_event(event: pygame.event.Event, state: GameState, ui_mgr):
    """处理主界面的交互事件"""
    init_buttons(ui_mgr)

    # 检测点击了哪个按钮
    if buttons["sleep"].is_clicked(event):
        advance_to_next_day(state)
    elif buttons["harem"].is_clicked(event):
        state.current_state = "harem"
    elif buttons["warehouse"].is_clicked(event):
        state.current_state = "warehouse"
    elif buttons["draft"].is_clicked(event):
        state.current_state = "draft"


def draw(screen: pygame.Surface, state: GameState, ui_mgr):
    """绘制主界面"""
    init_buttons(ui_mgr)

    # 1. 绘制背景图
    if "bg_main" in ui_mgr.images:
        screen.blit(ui_mgr.images["bg_main"], (0, 0))

    font = ui_mgr.fonts.get("normal")
    if font:
        # 2. 绘制顶部时间面板
        time_str = f"时间: {state.year} 年 {state.month} 月 {state.day} 日  {state.hour}:00"
        time_surface = font.render(time_str, True, config.BLACK)

        # 加个白色半透明或实色底板，让文字更清晰
        bg_rect = time_surface.get_rect(topleft=(20, 20))
        bg_rect.inflate_ip(20, 10)  # 让底板稍微大一点
        pygame.draw.rect(screen, config.WHITE, bg_rect)
        pygame.draw.rect(screen, config.BLACK, bg_rect, 2)  # 黑色边框
        screen.blit(time_surface, (30, 25))

    # 3. 绘制所有按钮
    for btn in buttons.values():
        btn.draw(screen)