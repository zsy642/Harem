import pygame
import sys
from src import config
from src.models import GameState
# 导入所有具体的场景文件
from .scenes import (
    main_scene, palace_scene, emperor_palace_scene,
    draft_scene, child_scene, travel_scene, storehouse_scene
)


class UIManager:
    def __init__(self, state: GameState):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("后宫模拟器 - 完整导航架构")
        self.clock = pygame.time.Clock()
        self.state = state

        # 加载中文字体 (保留你的修复)
        pygame.font.init()
        font_path = "C:/Windows/Fonts/STXIHEI.TTF"
        self.fonts = {
            "normal": pygame.font.Font(font_path, 24),
            "title": pygame.font.Font(font_path, 36)
        }

        self.images = {}
        self._load_resources()

    def _load_resources(self):
        """预加载图片资源"""
        try:
            bg = pygame.image.load(config.PICTURE_LIBRARY["bg_main"]).convert()
            self.images["bg_main"] = pygame.transform.scale(bg, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except Exception as e:
            print(f"[警告] 图片资源加载失败: {e}")
            surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            surface.fill(config.GRAY)
            self.images["bg_main"] = surface

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- 全局路由分发 ---
            s = self.state.current_state
            if s == "main":
                main_scene.handle_event(event, self.state, self)
            elif s == "palace":
                palace_scene.handle_event(event, self.state, self)
            elif s == "emperor_palace":
                emperor_palace_scene.handle_event(event, self.state, self)
            elif s == "draft":
                draft_scene.handle_event(event, self.state, self)
            elif s == "child":
                child_scene.handle_event(event, self.state, self)
            elif s == "travel":
                travel_scene.handle_event(event, self.state, self)
            elif s == "storehouse":
                storehouse_scene.handle_event(event, self.state, self)

    def draw(self):
        self.screen.fill(config.BLACK)

        # --- 全局绘制分发 ---
        s = self.state.current_state
        if s == "main":
            main_scene.draw(self.screen, self.state, self)
        elif s == "palace":
            palace_scene.draw(self.screen, self.state, self)
        elif s == "emperor_palace":
            emperor_palace_scene.draw(self.screen, self.state, self)
        elif s == "draft":
            draft_scene.draw(self.screen, self.state, self)
        elif s == "child":
            child_scene.draw(self.screen, self.state, self)
        elif s == "travel":
            travel_scene.draw(self.screen, self.state, self)
        elif s == "storehouse":
            storehouse_scene.draw(self.screen, self.state, self)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(config.FPS)