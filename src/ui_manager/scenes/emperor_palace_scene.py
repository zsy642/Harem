import pygame
from src import config
from src.logic import advance_to_next_day
from src.ui_manager.components import Button, draw_text

buttons = {}

def init_buttons(ui_mgr):
    """确保按钮只初始化一次"""
    if "sleep" not in buttons:
        font = ui_mgr.fonts.get("normal")
        buttons["sleep"] = Button(config.SCREEN_WIDTH // 2 - 100, 250, 200, 50, "睡觉(进入次日)", font, (144, 238, 144))
        buttons["abdicate"] = Button(config.SCREEN_WIDTH // 2 - 100, 320, 200, 50, "传位(大结局)", font, (255, 100, 100))
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", font)

def handle_event(event, state, ui_mgr):
    init_buttons(ui_mgr)
    if event:
        if buttons["back"].is_clicked(event):
            state.current_state = "main"
        elif buttons["sleep"].is_clicked(event):
            advance_to_next_day(state)
        elif buttons["abdicate"].is_clicked(event):
            print("尝试点击传位，第三阶段将实现逻辑检测")

def draw(screen, state, ui_mgr):
    init_buttons(ui_mgr)
    screen.fill((40, 40, 40))  # 养心殿用深灰色色调
    draw_text(screen, "--- 养心殿 (皇帝寝宫) ---", ui_mgr.fonts.get("title"), config.WHITE, config.SCREEN_WIDTH // 2, 100, True)
    draw_text(screen, "皇上，该翻牌子还是休息了？", ui_mgr.fonts.get("normal"), config.GRAY, config.SCREEN_WIDTH // 2, 160, True)

    for btn in buttons.values():
        btn.draw(screen)
