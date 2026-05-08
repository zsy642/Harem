import pygame
from src import config
from src.ui_manager.components import Button

buttons = {}


def init_buttons(ui_mgr):
    if buttons: return
    font = ui_mgr.fonts.get("normal")
    cx = config.SCREEN_WIDTH // 2

    # 建立 6 个导航按钮前往子场景
    buttons["to_emperor"] = Button(cx - 100, 200, 200, 45, "养心殿(皇帝寝宫)", font)
    buttons["to_palace"] = Button(cx - 100, 260, 200, 45, "东西六宫(后宫)", font)
    buttons["to_draft"] = Button(cx - 100, 320, 200, 45, "大选秀女", font)
    buttons["to_child"] = Button(cx - 100, 380, 200, 45, "重华宫(子嗣)", font)
    buttons["to_store"] = Button(cx - 100, 440, 200, 45, "内务府(仓库)", font)
    buttons["to_travel"] = Button(cx - 100, 500, 200, 45, "出巡游玩", font)


def handle_event(event, state, ui_mgr):
    init_buttons(ui_mgr)
    if buttons["to_emperor"].is_clicked(event):
        state.current_state = "emperor_palace"
    elif buttons["to_palace"].is_clicked(event):
        state.current_state = "palace"
    elif buttons["to_draft"].is_clicked(event):
        state.current_state = "draft"
    elif buttons["to_child"].is_clicked(event):
        state.current_state = "child"
    elif buttons["to_store"].is_clicked(event):
        state.current_state = "storehouse"
    elif buttons["to_travel"].is_clicked(event):
        state.current_state = "travel"


def draw(screen, state, ui_mgr):
    init_buttons(ui_mgr)
    if "bg_main" in ui_mgr.images:
        screen.blit(ui_mgr.images["bg_main"], (0, 0))

    # 绘制状态栏
    font = ui_mgr.fonts.get("normal")
    status = f"{state.family_name}朝 | {state.year}年{state.month}月{state.day}日 {state.hour}:00"
    surf = font.render(status, True, config.BLACK)
    pygame.draw.rect(screen, config.WHITE, (20, 20, surf.get_width() + 20, 40))
    screen.blit(surf, (30, 28))

    for btn in buttons.values():
        btn.draw(screen)