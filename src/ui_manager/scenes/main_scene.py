import pygame
from src import config
from src.models import GameState
from src.logic import advance_to_next_day


def handle_event(event: pygame.event.Event, state: GameState, ui_mgr):
    """处理主界面的交互事件"""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = event.pos

        # 临时“睡觉”按钮的碰撞检测区 (X, Y, W, H)
        sleep_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 50, config.SCREEN_HEIGHT // 2, 100, 50)

        if sleep_rect.collidepoint(mouse_pos):
            # 调用底层逻辑：推进到下一天
            advance_to_next_day(state)


def draw(screen: pygame.Surface, state: GameState, ui_mgr):
    """绘制主界面"""
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

        # 3. 绘制临时“睡觉”按钮
        sleep_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 50, config.SCREEN_HEIGHT // 2, 100, 50)
        pygame.draw.rect(screen, (100, 200, 100), sleep_rect)  # 绿色底色
        pygame.draw.rect(screen, config.BLACK, sleep_rect, 2)  # 黑色边框

        sleep_text = font.render("睡觉", True, config.BLACK)
        text_rect = sleep_text.get_rect(center=sleep_rect.center)
        screen.blit(sleep_text, text_rect)