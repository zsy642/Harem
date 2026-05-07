from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union


@dataclass
class Rank:
    """位分级表"""
    name: str  # 位分名称，如“皇后”
    limit: int  # 人数限制，-1为无限制
    favor_req: int  # 晋升所需的最低宠爱值


@dataclass
class Concubine:
    """妃嫔类"""
    id: str  # 唯一标识符
    name: str  # 名字
    title: str  # 封号
    rank: str  # 当前位分名称
    favor: int = 0  # 宠爱度
    age: int =16 #年龄,默认16
    experience: int = 0  # 经验值（侍寝增加）
    personality: str = "温柔"  # 性格
    pregnancy_rate: float = 0.1  # 怀孕概率 (0.05 - 0.25)
    pregnancy_days_remaining: int = -1  # 孕期倒计时，-1为未孕，0为生产日
    health: int = 100  # 健康值，为0死亡
    picture: str = "default_f"  # 立绘ID
    log: List[dict] = field(default_factory=list)  # 个人日志
    palace: str = "储秀宫" # 居住宫殿


@dataclass
class Child:
    """子女类"""
    id: str
    name: str  # 全名（姓+名）
    gender: str  # 性别
    mother_id: str  # 生母ID
    title: str = ""  # 封号
    favor: int = 0  # 宠爱值
    health: int = 100  # 健康值，为0死亡
    intelligence: int = 50  # 聪慧值
    age_days: int = 0  # 总天数
    palace: str = "重华宫"  # 固定居住宫殿
    picture: str = "default_c"  # 立绘ID
    log: List[dict] = field(default_factory=list)


@dataclass
class Item:
    """物品类"""
    name: str
    quantity: int = 0
    favor_bonus: int = 10  # 增加的宠爱值


@dataclass
class Palace:
    """宫殿类"""
    name: str
    capacity: int = 1  # 最大容量，-1为无限
    moved_list: List[str] = field(default_factory=list)  # 已入住妃嫔的ID或名字列表


@dataclass
class GameState:
    """全局游戏状态 (单例模式)"""
    family_name: str  # 玩家姓氏
    year: int = 1
    month: int = 1
    day: int = 1
    hour: int = 0
    current_state: str = "main"  # 界面标识：main, harem, warehouse, game_over 等

    # 实体数据容器
    rank_list: List[Rank] = field(default_factory=list)
    concubine_list: List[Concubine] = field(default_factory=list)
    child_list: List[Child] = field(default_factory=list)
    palace_list: List[Palace] = field(default_factory=list)
    item_list: List[Item] = field(default_factory=list)

    # 缓存/临时数据
    draft_pool: List[Concubine] = field(default_factory=list)  # 选秀待选池

    # 全局配置映射
    available_travel_places: List[str] = field(default_factory=list)
    picture_library: Dict[str, str] = field(default_factory=list)
