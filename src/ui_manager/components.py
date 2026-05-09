import pygame
from src import config


class Button:
    """通用的 UI 按钮组件"""

    def __init__(self, x, y, width, height, text, font,
                 bg_color=(200, 200, 200), hover_color=(230, 230, 230), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        # 内部状态：鼠标是否悬停
        self.is_hovered = False

    def draw(self, screen: pygame.Surface):
        """绘制按钮"""
        # 检测鼠标是否悬停在按钮上
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # 根据悬停状态选择颜色
        current_color = self.hover_color if self.is_hovered else self.bg_color

        # 画按钮底色和黑色边框
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, config.BLACK, self.rect, 2)

        # 画文字 (自动居中)
        if self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """检测该按钮是否在当前事件中被点击"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False


def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, color: tuple, x: int, y: int,
              center: bool = False):
    """通用的文字渲染工具"""
    if not font:
        return
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
    else:
        screen.blit(text_surface, (x, y))

class InputBox:
    """简单的文本输入框"""
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = config.GOLD
        self.font = font
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return "SUBMIT"
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 4: # 限制名字长度
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        # 画底色和边框
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+10))