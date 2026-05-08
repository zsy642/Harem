import pygame
from src import config
from src.ui_manager.components import Button, draw_text

buttons = {}


def handle_event(event, state, ui_mgr):
    if "back" not in buttons:
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", ui_mgr.fonts.get("normal"))

    if buttons["back"].is_clicked(event):
        state.current_state = "main"


def draw(screen, state, ui_mgr):
    if "back" not in buttons:
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", ui_mgr.fonts.get("normal"))

    screen.fill((50, 40, 70))  # 后宫背景色偏紫
    draw_text(screen, "--- 后宫寝殿 ---", ui_mgr.fonts.get("title"), config.WHITE, config.SCREEN_WIDTH // 2, 100, True)
    draw_text(screen, "（此处后续将渲染妃嫔列表）", ui_mgr.fonts.get("normal"), config.GRAY, config.SCREEN_WIDTH // 2,
              200, True)

    buttons["back"].draw(screen)
