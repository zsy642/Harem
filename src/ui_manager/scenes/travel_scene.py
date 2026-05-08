import pygame
from src import config
from src.ui_manager.components import Button, draw_text

buttons = {}

def init_buttons(ui_mgr):
    if "back" not in buttons:
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", ui_mgr.fonts.get("normal"))

def handle_event(event, state, ui_mgr):
    init_buttons(ui_mgr)
    if event and buttons["back"].is_clicked(event):
        state.current_state = "main"

def draw(screen, state, ui_mgr):
    init_buttons(ui_mgr)
    screen.fill((40, 70, 40))  # 绿色
    draw_text(screen, "--- 皇家园林游玩 ---", ui_mgr.fonts.get("title"), config.WHITE, config.SCREEN_WIDTH//2, 100, True)
    buttons["back"].draw(screen)