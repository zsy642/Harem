import pygame
from src import config
from src.logic import generate_draft_candidates, accept_draft_candidate
from src.ui_manager.components import Button, draw_text

# 常规按钮
buttons = {}
# 动态生成的秀女留用按钮
candidate_buttons = {}


def init_buttons(ui_mgr):
    """初始化基础交互按钮"""
    if "back" not in buttons:
        font = ui_mgr.fonts.get("normal")
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", font)
        buttons["start_draft"] = Button(config.SCREEN_WIDTH // 2 - 100, 300, 200, 50, "开启三年一秀", font,
                                        (255, 182, 193))
        buttons["clear_draft"] = Button(config.SCREEN_WIDTH // 2 - 100, 600, 200, 50, "结束本届选秀", font,
                                        (200, 200, 200))


def handle_event(event, state, ui_mgr):
    """处理选秀界面的交互事件"""
    init_buttons(ui_mgr)

    if not event: return

    # 1. 离开界面时，清理数据
    if buttons["back"].is_clicked(event):
        state.draft_pool.clear()
        candidate_buttons.clear()
        state.current_state = "main"
        return

    # 2. 如果秀女池为空，处理“开启选秀”
    if not state.draft_pool:
        if buttons["start_draft"].is_clicked(event):
            generate_draft_candidates(state)
            candidate_buttons.clear()  # 刷新按钮池
    else:
        # 3. 如果秀女池有数据，处理“结束选秀”
        if buttons["clear_draft"].is_clicked(event):
            state.draft_pool.clear()
            candidate_buttons.clear()
            return

        # 4. 遍历所有动态生成的“留用”按钮
        for cid, btn in list(candidate_buttons.items()):
            if btn.is_clicked(event):
                # 自动为秀女寻找一个有空床位的宫殿 (排除储秀宫和重华宫)
                target_palace = "储秀宫"  # 默认保底
                for p in state.palace_list:
                    if p.name not in ["储秀宫", "重华宫"] and (p.capacity == -1 or len(p.moved_list) < p.capacity):
                        target_palace = p.name
                        break

                # 调用底层逻辑将秀女纳入后宫
                res = accept_draft_candidate(state, cid, target_palace, "答应")
                print(res["msg"])  # 在控制台打印册封结果

                # 【修复Bug】: 留用后，因为剩余卡片会左移，必须清空整个按钮缓存强制重新生成坐标！
                candidate_buttons.clear()
                break  # 必须 break，防止字典被清空后继续迭代报错


def draw(screen, state, ui_mgr):
    """绘制选秀大典"""
    init_buttons(ui_mgr)

    # 绘制背景
    screen.fill((70, 60, 40))  # 皇家金褐色
    font_title = ui_mgr.fonts.get("title")
    font_normal = ui_mgr.fonts.get("normal")

    draw_text(screen, "--- 大选秀女 ---", font_title, config.WHITE, config.SCREEN_WIDTH // 2, 80, center=True)

    if not state.draft_pool:
        # 空池子状态
        draw_text(screen, "储秀宫目前空无一人，是否开启新一届选秀？", font_normal, config.WHITE, config.SCREEN_WIDTH // 2,
                  200, center=True)
        buttons["start_draft"].draw(screen)
    else:
        # 已有秀女状态：绘制卡片
        draw_text(screen, "本届秀女已在大殿候着了：", font_normal, config.WHITE, config.SCREEN_WIDTH // 2, 150,
                  center=True)

        start_x = config.SCREEN_WIDTH // 2 - 450
        card_width = 280
        card_height = 400
        spacing = 30

        for i, cand in enumerate(state.draft_pool):
            x = start_x + i * (card_width + spacing)
            y = 200
            rect = pygame.Rect(x, y, card_width, card_height)

            # 绘制卡片底色和描边
            pygame.draw.rect(screen, (90, 80, 60), rect)
            pygame.draw.rect(screen, config.GOLD, rect, 2)

            # 绘制秀女信息
            draw_text(screen, f"姓名: {cand.name}", font_normal, config.WHITE, x + 20, y + 20)
            draw_text(screen, f"出身: {cand.name[:2]}氏", font_normal, config.GRAY, x + 20, y + 60)
            draw_text(screen, f"孕率: {int(cand.pregnancy_rate * 100)}%", font_normal, (255, 180, 180), x + 20, y + 100)

            # 绘制立绘占位框
            pic_rect = pygame.Rect(x + 65, y + 150, 150, 150)
            pygame.draw.rect(screen, (50, 50, 50), pic_rect)
            draw_text(screen, "立绘加载处", font_normal, config.GRAY, pic_rect.centerx, pic_rect.centery, center=True)

            # 绘制留用按钮
            btn_id = cand.id
            if btn_id not in candidate_buttons:
                candidate_buttons[btn_id] = Button(x + 40, y + 330, 200, 40, "留用(赐答应)", font_normal,
                                                   (255, 100, 100)) #TODO这里答应不要硬编码
            candidate_buttons[btn_id].draw(screen)

        # 结束选秀按钮
        buttons["clear_draft"].draw(screen)

    buttons["back"].draw(screen)