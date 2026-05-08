import pygame
import sys
from src import config
from src.models import GameState
from .scenes import main_scene


class UIManager:
    def __init__(self, state: GameState):
        """初始化 Pygame 和 游戏窗口"""
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("后宫模拟器")
        self.clock = pygame.time.Clock()
        self.state = state

        # 加载中文字体 (兼容不同操作系统)
        pygame.font.init()
        # 直接加载字体文件
        font_normal_path = "C:/Windows/Fonts/STXIHEI.TTF"
        font_title_path = "C:/Windows/Fonts/STXIHEI.TTF"  # 和普通字体用同一个文件，只是字号不同

        self.fonts = {
            "normal": pygame.font.Font(font_normal_path, 24),
            "title": pygame.font.Font(font_title_path, 36)
        }

        # 资源缓存字典
        self.images = {}
        self._load_resources()

    def _load_resources(self):
        """预加载图片资源"""
        try:
            # 加载占位背景，并缩放至窗口大小
            bg = pygame.image.load(config.PICTURE_LIBRARY["bg_main"]).convert()
            self.images["bg_main"] = pygame.transform.scale(bg, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except Exception as e:
            print(f"[警告] 图片资源加载失败: {e}")
            # 如果没找到图片，建一个灰色占位色块防崩溃
            surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            surface.fill(config.GRAY)
            self.images["bg_main"] = surface

    def handle_events(self):
        """全局事件分发"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 状态机路由：根据当前界面分发鼠标/键盘事件
            if self.state.current_state == "main":
                main_scene.handle_event(event, self.state, self)
            # 未来这里会增加 elif state == "harem" 等等

    def draw(self):
        """全局绘制控制"""
        self.screen.fill(config.BLACK)

        # 状态机路由：根据当前界面绘制对应内容
        if self.state.current_state == "main":
            main_scene.draw(self.screen, self.state, self)

        pygame.display.flip()

    def run(self):
        """游戏主循环"""
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(config.FPS)