import pygame
from src import config
from src.logic import delete_character, interact_gift
from src.ui_manager.components import Button, draw_text

buttons = {}
action_buttons = {}
page_info = {"current": 0, "per_page": 8}
selected_cid = None
scene_msg = ""


def init_buttons(ui_mgr):
    if "back" not in buttons:
        font = ui_mgr.fonts.get("normal")
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", font)
        buttons["prev"] = Button(50, 620, 100, 40, "上一页", font)
        buttons["next"] = Button(250, 620, 100, 40, "下一页", font)


def handle_event(event, state, ui_mgr):
    global scene_msg, selected_cid
    init_buttons(ui_mgr)
    if not event: return

    if buttons["back"].is_clicked(event):
        state.current_state = "main"
        scene_msg = ""
        selected_cid = None
        return

    # 分页逻辑
    total_pages = max(1, (len(state.child_list) + page_info["per_page"] - 1) // page_info["per_page"])
    if buttons["prev"].is_clicked(event) and page_info["current"] > 0:
        page_info["current"] -= 1
        scene_msg = ""
    if buttons["next"].is_clicked(event) and page_info["current"] < total_pages - 1:
        page_info["current"] += 1
        scene_msg = ""

    # 列表点击检测
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        start_idx = page_info["current"] * page_info["per_page"]
        end_idx = start_idx + page_info["per_page"]
        for i, child in enumerate(state.child_list[start_idx:end_idx]):
            item_rect = pygame.Rect(50, 120 + i * 60, 300, 50)
            if item_rect.collidepoint(event.pos):
                selected_cid = child.id
                scene_msg = ""
                action_buttons.clear()

    # 操作按钮检测
    for key, btn in list(action_buttons.items()):
        if btn.is_clicked(event):
            action, cid = key.split("_", 1)
            if action == "gift":
                res = interact_gift(state, cid, "点心", is_child=True)  # 赏赐点心
                scene_msg = res["msg"]
            elif action == "kill":
                res = delete_character(state, cid)
                scene_msg = res["msg"]
                action_buttons.clear()


def draw(screen, state, ui_mgr):
    global selected_cid
    init_buttons(ui_mgr)

    screen.fill((40, 60, 60))  # 沉稳的青蓝色
    font_title = ui_mgr.fonts.get("title")
    font_normal = ui_mgr.fonts.get("normal")

    draw_text(screen, "--- 重华宫 (皇子公主) ---", font_title, config.WHITE, config.SCREEN_WIDTH // 2, 40, center=True)

    if scene_msg:
        draw_text(screen, scene_msg, font_normal, config.GOLD, config.SCREEN_WIDTH // 2, 80, center=True)

    if not state.child_list:
        draw_text(screen, "膝下暂无子嗣...", font_normal, config.GRAY, config.SCREEN_WIDTH // 2, 300, center=True)
        buttons["back"].draw(screen)
        return

    # 左侧名单区
    list_rect = pygame.Rect(40, 100, 320, 580)
    pygame.draw.rect(screen, (30, 45, 45), list_rect)
    pygame.draw.rect(screen, config.GOLD, list_rect, 2)

    total_pages = max(1, (len(state.child_list) + page_info["per_page"] - 1) // page_info["per_page"])
    if page_info["current"] >= total_pages: page_info["current"] = max(0, total_pages - 1)

    start_idx = page_info["current"] * page_info["per_page"]
    end_idx = start_idx + page_info["per_page"]
    display_list = state.child_list[start_idx:end_idx]

    if not selected_cid and display_list:
        selected_cid = display_list[0].id

    for i, child in enumerate(display_list):
        item_rect = pygame.Rect(50, 120 + i * 60, 300, 50)
        is_selected = (child.id == selected_cid)
        is_dead = (child.health <= 0)

        bg_color = (60, 90, 90) if is_selected else (40, 60, 60)
        if is_dead: bg_color = (30, 30, 30)

        pygame.draw.rect(screen, bg_color, item_rect)
        pygame.draw.rect(screen, config.GOLD if is_selected else (100, 100, 100), item_rect, 2)

        name_str = f"{child.name} ({child.gender})"
        text_color = config.WHITE if not is_dead else config.GRAY
        draw_text(screen, name_str, font_normal, text_color, item_rect.x + 20, item_rect.y + 12)

    draw_text(screen, f"{page_info['current'] + 1} / {total_pages}", font_normal, config.WHITE, 200, 640, center=True)
    if page_info["current"] > 0: buttons["prev"].draw(screen)
    if page_info["current"] < total_pages - 1: buttons["next"].draw(screen)

    # 右侧详情区
    detail_rect = pygame.Rect(400, 100, 840, 580)
    pygame.draw.rect(screen, (30, 45, 45), detail_rect)
    pygame.draw.rect(screen, config.GOLD, detail_rect, 2)

    selected_child = next((c for c in state.child_list if c.id == selected_cid), None)

    if selected_child:
        is_dead = selected_child.health <= 0

        pic_rect = pygame.Rect(450, 150, 250, 350)
        pygame.draw.rect(screen, (80, 80, 80) if not is_dead else (30, 30, 30), pic_rect)
        draw_text(screen, "子嗣立绘", font_normal, config.WHITE if not is_dead else config.GRAY, pic_rect.centerx,
                  pic_rect.centery, center=True)

        info_x, info_y = 750, 150
        age_years = selected_child.age_days // 48

        # 查找生母名字
        mother = next((c for c in state.concubine_list if c.id == selected_child.mother_id), None)
        mother_name = mother.name if mother else "未知"

        draw_text(screen, f"姓名：{selected_child.name}", font_title, config.GOLD if not is_dead else config.GRAY,
                  info_x, info_y)
        draw_text(screen, f"性别：{selected_child.gender}", font_normal, config.WHITE if not is_dead else config.GRAY,
                  info_x, info_y + 60)
        draw_text(screen, f"年龄：{age_years} 岁 ({selected_child.age_days}天)", font_normal,
                  config.WHITE if not is_dead else config.GRAY, info_x, info_y + 110)
        draw_text(screen, f"生母：{mother_name}", font_normal, config.WHITE if not is_dead else config.GRAY, info_x,
                  info_y + 160)
        draw_text(screen, f"聪慧：{selected_child.intelligence}", font_normal,
                  config.WHITE if not is_dead else config.GRAY, info_x, info_y + 210)
        draw_text(screen, f"宠爱：{selected_child.favor}", font_normal, config.WHITE if not is_dead else config.GRAY,
                  info_x, info_y + 260)

        if is_dead:
            draw_text(screen, "【状态：不幸夭折】", font_title, (200, 50, 50), info_x, info_y + 310)
        else:
            status = "已成年 (可传位)" if age_years >= 18 else "未成年"
            draw_text(screen, f"【状态：健康 ({status})】", font_normal, (100, 255, 100), info_x, info_y + 310)

            gift_key, kill_key = f"gift_{selected_cid}", f"kill_{selected_cid}"
            if gift_key not in action_buttons:
                action_buttons[gift_key] = Button(info_x, info_y + 380, 150, 50, "赏赐点心", font_normal,
                                                  (180, 200, 255))
                action_buttons[kill_key] = Button(info_x + 180, info_y + 380, 150, 50, "赐死", font_normal,
                                                  (100, 100, 100), text_color=config.WHITE)

            action_buttons[gift_key].draw(screen)
            action_buttons[kill_key].draw(screen)

    buttons["back"].draw(screen)