"""
后宫游戏 - 全局静态配置
存放窗口设置、初始数据表、路径映射等常量。
"""

# --- 窗口与显示配置 ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# 颜色定义 (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GOLD = (212, 175, 55)  # 用于高级位分显示
RED = (200, 0, 0)  # 用于死亡状态显示

# --- 时间系统配置 ---
HOURS_PER_DAY = 24
DAYS_PER_MONTH = 4
MONTHS_PER_YEAR = 12

# --- 初始数据预设 ---

# 1. 初始宫殿配置 
# MVP 阶段 capacity 设为 3，储秀宫和重华宫设为极大值
INITIAL_PALACES = [
    {"name": "储秀宫", "capacity": 100},  # 初始待命处
    {"name": "重华宫", "capacity": 100},  # 子女居住处
    {"name": "景仁宫", "capacity": 3},
    {"name": "延禧宫", "capacity": 3},
    {"name": "承乾宫", "capacity": 3},
    {"name": "翊坤宫", "capacity": 3},
    {"name": "永和宫", "capacity": 3},
    {"name": "钟粹宫", "capacity": 3},
]

# 2. 初始位分表 (Rank List)
# 格式: (名称, 人数限制, 晋升所需宠爱值)
INITIAL_RANKS = [
    {"name": "皇后", "limit": 1, "favor_req": 2000},
    {"name": "皇贵妃", "limit": 1, "favor_req": 1500},
    {"name": "贵妃", "limit": 2, "favor_req": 1000},
    {"name": "妃", "limit": 4, "favor_req": 800},
    {"name": "嫔", "limit": 6, "favor_req": 500},
    {"name": "贵人", "limit": -1, "favor_req": 200},
    {"name": "常在", "limit": -1, "favor_req": 100},
    {"name": "答应", "limit": -1, "favor_req": 0},
]

# 3. 游玩地点 (AVAILABLE_TRAVEL_PLACES)
AVAILABLE_TRAVEL_PLACES = [
    "御花园", "畅春园", "圆明园",
    "避暑山庄", "太液池", "昆明湖"
]

# 4. 初始物品清单
INITIAL_ITEMS = [
    {"name": "玉佩", "quantity": 10, "favor_bonus": 20},
    {"name": "点心", "quantity": 20, "favor_bonus": 10},
]

# --- 资源路径配置 ---

# 图片 ID 与 路径映射 (目前全部使用 tmp1 和 tmp2)
# key: 立绘ID/背景ID, value: 相对路径
PICTURE_LIBRARY = {
    # 背景类 (使用 tmp1.png)
    "bg_main": "assets/tmp1.png",
    "bg_harem": "assets/tmp1.png",
    "bg_palace": "assets/tmp1.png",
    "bg_warehouse": "assets/tmp1.png",
    "bg_draft": "assets/tmp1.png",
    "bg_travel": "assets/tmp1.png",

    # 角色类 (使用 tmp2.png)
    "default_f": "assets/tmp2.png",  # 默认妃嫔立绘
    "default_c": "assets/tmp2.png",  # 默认子女立绘
}

# --- 交互平衡参数 ---
INTERACT_COST_HOUR = 4  # 侍寝和游玩消耗的小时数
YEARLY_ITEM_BONUS = 50  # 每年结算增加的物品数量
INITIAL_PREGNANCY_DAYS = 36  # 初始怀孕倒计时天数
ADULT_AGE_DAYS = 864  # 成年天数 (4 * 12 * 18)