import sys
import os

# 将项目根目录添加到系统路径，确保能正确找到 src 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic import init_new_game
from src.ui_manager.core import UIManager


def main():
    print("正在初始化游戏数据...")
    # 1. 初始化全新的游戏数据（开局）
    state = init_new_game(family_name="慕容")

    print("正在启动 UI 管理器...")
    # 2. 启动 UI 管理器并绑定状态
    ui_mgr = UIManager(state)

    print("进入游戏主循环...")
    # 3. 进入主循环
    ui_mgr.run()


if __name__ == "__main__":
    main()