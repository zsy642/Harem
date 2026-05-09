import pygame
from src import config
from src.logic import interact_bedding, delete_character, interact_gift
from src.ui_manager.components import Button, draw_text

# 固定的基础按钮
buttons = {}
# 动态的操作按钮
action_buttons = {}
# 分页控制 (左侧列表每页可容纳8人)
page_info = {"current": 0, "per_page": 8}
# 当前选中的妃子ID
selected_cid = None
# 顶部提示语
scene_msg = ""

def init_buttons(ui_mgr):
    """初始化固定的导航与分页按钮"""
    if "back" not in buttons:
        font = ui_mgr.fonts.get("normal")
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", font)
        # 左侧列表分页按钮
        buttons["prev"] = Button(50, 620, 100, 40, "上一页", font)
        buttons["next"] = Button(250, 620, 100, 40, "下一页", font)

def handle_event(event, state, ui_mgr):
    global scene_msg, selected_cid
    init_buttons(ui_mgr)
    if not event: return

    # 1. 返回主界面
    if buttons["back"].is_clicked(event):
        state.current_state = "main"
        scene_msg = ""
        selected_cid = None
        return

    # 2. 分页逻辑 (安全严谨版)
    total_pages = max(1, (len(state.concubine_list) + page_info["per_page"] - 1) // page_info["per_page"])
    if buttons["prev"].is_clicked(event) and page_info["current"] > 0:
        page_info["current"] -= 1
        scene_msg = ""
        return
    if buttons["next"].is_clicked(event) and page_info["current"] < total_pages - 1:
        page_info["current"] += 1
        scene_msg = ""
        return

    # 3. 左侧名单点击检测 (直接算坐标，彻底告别缓存Bug)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        start_idx = page_info["current"] * page_info["per_page"]
        end_idx = start_idx + page_info["per_page"]
        display_list = state.concubine_list[start_idx:end_idx]

        for i, concubine in enumerate(display_list):
            item_rect = pygame.Rect(50, 120 + i * 60, 300, 50)
            if item_rect.collidepoint(event.pos):
                selected_cid = concubine.id
                scene_msg = ""
                action_buttons.clear() # 切换妃子，清空右侧按钮缓存

    # 4. 右侧操作按钮点击检测
    for key, btn in list(action_buttons.items()):
        if btn.is_clicked(event):
            action, cid = key.split("_", 1)
            if action == "bed":
                res = interact_bedding(state, cid)
                scene_msg = res["msg"]
            elif action == "gift":
                res = interact_gift(state, cid, "玉佩")
                scene_msg = res["msg"]
            elif action == "kill":
                res = delete_character(state, cid)
                scene_msg = res["msg"]
                action_buttons.clear()


def draw(screen, state, ui_mgr):
    global selected_cid
    init_buttons(ui_mgr)

    # 背景与标题
    screen.fill((50, 40, 60))
    font_title = ui_mgr.fonts.get("title")
    font_normal = ui_mgr.fonts.get("normal")

    draw_text(screen, "--- 东西六宫 (后宫寝殿) ---", font_title, config.WHITE, config.SCREEN_WIDTH//2, 40, center=True)

    if scene_msg:
        draw_text(screen, scene_msg, font_normal, config.GOLD, config.SCREEN_WIDTH//2, 80, center=True)

    if not state.concubine_list:
        draw_text(screen, "后宫空无一人，请先前往【大选秀女】充实后宫...", font_normal, config.GRAY, config.SCREEN_WIDTH//2, 300, center=True)
        buttons["back"].draw(screen)
        return

    # ================= 左侧：妃嫔名单区 =================
    list_rect = pygame.Rect(40, 100, 320, 580)
    pygame.draw.rect(screen, (40, 30, 50), list_rect)
    pygame.draw.rect(screen, config.GOLD, list_rect, 2)

    total_pages = max(1, (len(state.concubine_list) + page_info["per_page"] - 1) // page_info["per_page"])
    if page_info["current"] >= total_pages: page_info["current"] = max(0, total_pages - 1)

    start_idx = page_info["current"] * page_info["per_page"]
    end_idx = start_idx + page_info["per_page"]
    display_list = state.concubine_list[start_idx:end_idx]

    # 若未选中任何妃子，默认选中当前页的第一个
    if not selected_cid and display_list:
        selected_cid = display_list[0].id

    for i, concubine in enumerate(display_list):
        item_rect = pygame.Rect(50, 120 + i * 60, 300, 50)
        is_selected = (concubine.id == selected_cid)
        is_dead = (concubine.health <= 0)

        bg_color = (100, 80, 120) if is_selected else (60, 50, 70)
        if is_dead: bg_color = (30, 30, 30)

        pygame.draw.rect(screen, bg_color, item_rect)
        pygame.draw.rect(screen, config.GOLD if is_selected else (100, 100, 100), item_rect, 2)

        name_str = f"{concubine.name} ({concubine.rank})"
        text_color = config.WHITE if not is_dead else config.GRAY
        draw_text(screen, name_str, font_normal, text_color, item_rect.x + 20, item_rect.y + 12)

    # 分页控制
    draw_text(screen, f"{page_info['current'] + 1} / {total_pages}", font_normal, config.WHITE, 200, 640, center=True)
    if page_info["current"] > 0: buttons["prev"].draw(screen)
    if page_info["current"] < total_pages - 1: buttons["next"].draw(screen)

    # ================= 右侧：选中妃嫔详情区 =================
    detail_rect = pygame.Rect(400, 100, 840, 580)
    pygame.draw.rect(screen, (40, 30, 50), detail_rect)
    pygame.draw.rect(screen, config.GOLD, detail_rect, 2)

    selected_con = next((c for c in state.concubine_list if c.id == selected_cid), None)

    if selected_con:
        is_dead = selected_con.health <= 0

        # 1. 立绘占位
        pic_rect = pygame.Rect(450, 150, 250, 350)
        pygame.draw.rect(screen, (80,80,80) if not is_dead else (30,30,30), pic_rect)
        draw_text(screen, "妃嫔立绘", font_normal, config.WHITE if not is_dead else config.GRAY, pic_rect.centerx, pic_rect.centery, center=True)

        # 2. 文字信息
        info_x = 750
        info_y = 150
        draw_text(screen, f"姓名：{selected_con.name}", font_title, config.GOLD if not is_dead else config.GRAY, info_x, info_y)
        draw_text(screen, f"位分：{selected_con.title}{selected_con.rank}", font_normal, config.WHITE if not is_dead else config.GRAY, info_x, info_y + 60)
        draw_text(screen, f"居所：{selected_con.palace}", font_normal, config.WHITE if not is_dead else config.GRAY, info_x, info_y + 110)
        draw_text(screen, f"宠爱值：{selected_con.favor}", font_normal, config.WHITE if not is_dead else config.GRAY, info_x, info_y + 160)
        draw_text(screen, f"经验值：{selected_con.experience}", font_normal, config.WHITE if not is_dead else config.GRAY, info_x, info_y + 210)
        draw_text(screen, f"怀孕率：{int(selected_con.pregnancy_rate*100)}%", font_normal, config.WHITE if not is_dead else config.GRAY, info_x, info_y + 260)

        # 状态提示
        if selected_con.pregnancy_days_remaining > 0:
            draw_text(screen, f"【有喜：距生产剩 {selected_con.pregnancy_days_remaining} 天】", font_normal, (255, 150, 150), info_x, info_y + 310)
        elif is_dead:
            draw_text(screen, "【状态：香消玉殒】", font_title, (200, 50, 50), info_x, info_y + 310)
        else:
            draw_text(screen, "【状态：健康闲居】", font_normal, (100, 255, 100), info_x, info_y + 310)

        # 3. 操作按钮区
        if not is_dead:
            bed_key = f"bed_{selected_cid}"
            gift_key = f"gift_{selected_cid}"
            kill_key = f"kill_{selected_cid}"

            if bed_key not in action_buttons:
                action_buttons[bed_key] = Button(info_x, info_y + 380, 150, 50, "侍寝(-4h)", font_normal, (255, 180, 180))
                action_buttons[gift_key] = Button(info_x + 180, info_y + 380, 150, 50, "赏赐玉佩", font_normal, (180, 200, 255))
                action_buttons[kill_key] = Button(info_x, info_y + 450, 150, 50, "赐死", font_normal, (100, 100, 100), text_color=config.WHITE)

            action_buttons[bed_key].draw(screen)
            action_buttons[gift_key].draw(screen)
            action_buttons[kill_key].draw(screen)

    buttons["back"].draw(screen)