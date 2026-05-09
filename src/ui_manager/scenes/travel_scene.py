import pygame
from src import config
from src.logic import interact_travel
from src.ui_manager.components import Button, draw_text

buttons = {}
location_buttons = {}
# 存储玩家选中的同行者 ID 集合
selected_companions = set()
selected_location = None
scene_msg = ""
page_info = {"current": 0, "per_page": 6}


def init_buttons(ui_mgr):
    if "back" not in buttons:
        font = ui_mgr.fonts.get("normal")
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", font)
        buttons["go_travel"] = Button(config.SCREEN_WIDTH - 220, config.SCREEN_HEIGHT - 70, 200, 50, "开始游玩(-4h)",
                                      font, (144, 238, 144))
        buttons["prev"] = Button(420, 620, 100, 40, "上一页", font)
        buttons["next"] = Button(620, 620, 100, 40, "下一页", font)

    if not location_buttons:
        font = ui_mgr.fonts.get("normal")
        for i, loc in enumerate(config.AVAILABLE_TRAVEL_PLACES):
            # 左侧生成地点按钮
            location_buttons[loc] = Button(40, 150 + i * 70, 300, 50, loc, font, (200, 200, 200))


def handle_event(event, state, ui_mgr):
    global scene_msg, selected_location
    init_buttons(ui_mgr)
    if not event: return

    if buttons["back"].is_clicked(event):
        state.current_state = "main"
        scene_msg = ""
        selected_companions.clear()
        selected_location = None
        return

    # 1. 选择地点
    for loc, btn in location_buttons.items():
        if btn.is_clicked(event):
            selected_location = loc
            scene_msg = ""

    # 2. 获取所有存活角色（妃子 + 子嗣）
    alive_chars = [c for c in state.concubine_list + state.child_list if c.health > 0]
    total_pages = max(1, (len(alive_chars) + page_info["per_page"] - 1) // page_info["per_page"])

    if buttons["prev"].is_clicked(event) and page_info["current"] > 0:
        page_info["current"] -= 1
    if buttons["next"].is_clicked(event) and page_info["current"] < total_pages - 1:
        page_info["current"] += 1

    # 3. 点击勾选/取消同伴
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        start_idx = page_info["current"] * page_info["per_page"]
        end_idx = start_idx + page_info["per_page"]

        for i, char in enumerate(alive_chars[start_idx:end_idx]):
            item_rect = pygame.Rect(420, 150 + i * 70, 400, 50)
            if item_rect.collidepoint(event.pos):
                if char.id in selected_companions:
                    selected_companions.remove(char.id)
                else:
                    selected_companions.add(char.id)
                scene_msg = ""

    # 4. 执行游玩
    if buttons["go_travel"].is_clicked(event):
        if not selected_location:
            scene_msg = "请先选择游玩地点！"
        elif not selected_companions:
            scene_msg = "请至少选择一名同行人员！"
        else:
            res = interact_travel(state, list(selected_companions), selected_location)
            scene_msg = res["msg"]
            if res["success"]:
                selected_companions.clear()  # 游玩成功后清空选择


def draw(screen, state, ui_mgr):
    init_buttons(ui_mgr)

    screen.fill((40, 70, 40))  # 园林绿
    font_title = ui_mgr.fonts.get("title")
    font_normal = ui_mgr.fonts.get("normal")

    draw_text(screen, "--- 皇家园林游玩 ---", font_title, config.WHITE, config.SCREEN_WIDTH // 2, 40, center=True)

    if scene_msg:
        draw_text(screen, scene_msg, font_normal, config.GOLD, config.SCREEN_WIDTH // 2, 80, center=True)

    # 左侧：地点选择区
    draw_text(screen, "【1】选择游玩地点", font_normal, config.GOLD, 40, 110)
    for loc, btn in location_buttons.items():
        # 如果是被选中的地点，高亮显示
        btn.bg_color = config.GOLD if loc == selected_location else (200, 200, 200)
        btn.draw(screen)

    # 右侧：人员选择区
    draw_text(screen, "【2】选择同行人员 (多选)", font_normal, config.GOLD, 420, 110)

    alive_chars = [c for c in state.concubine_list + state.child_list if c.health > 0]
    total_pages = max(1, (len(alive_chars) + page_info["per_page"] - 1) // page_info["per_page"])
    if page_info["current"] >= total_pages: page_info["current"] = max(0, total_pages - 1)

    start_idx = page_info["current"] * page_info["per_page"]
    end_idx = start_idx + page_info["per_page"]

    if not alive_chars:
        draw_text(screen, "后宫暂无人员可陪伴出游...", font_normal, config.GRAY, 420, 200)
    else:
        for i, char in enumerate(alive_chars[start_idx:end_idx]):
            item_rect = pygame.Rect(420, 150 + i * 70, 400, 50)
            is_selected = char.id in selected_companions

            # 绘制复选框底色
            pygame.draw.rect(screen, (50, 100, 50) if is_selected else (30, 50, 30), item_rect)
            pygame.draw.rect(screen, config.GOLD if is_selected else (100, 100, 100), item_rect, 2)

            # 绘制打勾状态
            checkbox_str = "[ √ ] " if is_selected else "[   ] "
            role = "子嗣" if hasattr(char, "intelligence") else "妃嫔"
            display_str = f"{checkbox_str} {char.name} ({role}) - 宠爱: {char.favor}"

            draw_text(screen, display_str, font_normal, config.WHITE, item_rect.x + 15, item_rect.y + 12)

        # 分页
        draw_text(screen, f"{page_info['current'] + 1} / {total_pages}", font_normal, config.WHITE, 570, 640,
                  center=True)
        if page_info["current"] > 0: buttons["prev"].draw(screen)
        if page_info["current"] < total_pages - 1: buttons["next"].draw(screen)

    buttons["back"].draw(screen)
    buttons["go_travel"].draw(screen)