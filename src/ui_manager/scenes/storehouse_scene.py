import pygame
from src import config
from src.ui_manager.components import Button, draw_text

buttons = {}


def init_buttons(ui_mgr):
    """初始化场景交互按钮"""
    if "back" not in buttons:
        buttons["back"] = Button(20, config.SCREEN_HEIGHT - 70, 100, 50, "返回", ui_mgr.fonts.get("normal"))


def handle_event(event, state, ui_mgr):
    """处理内务府的交互事件"""
    init_buttons(ui_mgr)

    if event and buttons["back"].is_clicked(event):
        state.current_state = "main"


def draw(screen, state, ui_mgr):
    """绘制内务府界面"""
    init_buttons(ui_mgr)

    # 1. 绘制背景色
    screen.fill((60, 30, 30))  # 宫墙红底色

    font_title = ui_mgr.fonts.get("title")
    font_normal = ui_mgr.fonts.get("normal")

    # 2. 绘制标题
    draw_text(screen, "--- 内务府 (皇家私库) ---", font_title, config.WHITE, config.SCREEN_WIDTH // 2, 80, center=True)

    # 3. 渲染物品列表 (核心逻辑)
    start_y = 160  # 列表起始Y坐标
    row_height = 60  # 每行的高度
    spacing = 15  # 每行的间距
    panel_width = 700  # 列表面板宽度
    panel_x = (config.SCREEN_WIDTH - panel_width) // 2  # 居中X坐标

    if not state.item_list:
        draw_text(screen, "内务府空空如也...", font_normal, config.GRAY, config.SCREEN_WIDTH // 2, 250, center=True)
    else:
        for i, item in enumerate(state.item_list):
            y = start_y + i * (row_height + spacing)

            # 画一个半透明/深色的底框，让列表看起来更像UI
            rect = pygame.Rect(panel_x, y, panel_width, row_height)
            pygame.draw.rect(screen, (80, 50, 50), rect)  # 稍微亮一点的深红底框
            pygame.draw.rect(screen, config.BLACK, rect, 2)  # 黑色描边

            # 画物品名称 (居左，使用金色)
            draw_text(screen, f"【{item.name}】", font_normal, config.GOLD, rect.x + 30, rect.y + 15)

            # 画库存数量 (居中)
            draw_text(screen, f"库存数量: {item.quantity} 件", font_normal, config.WHITE, rect.x + 250, rect.y + 15)

            # 画物品效果 (居右)
            draw_text(screen, f"赏赐效果: 宠爱 +{item.favor_bonus}", font_normal, (200, 200, 200), rect.x + 480,
                      rect.y + 15)

    # 4. 绘制返回按钮
    buttons["back"].draw(screen)