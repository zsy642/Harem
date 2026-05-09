import pygame
from src import config
from src.logic import trigger_birth
from src.ui_manager.components import draw_text, InputBox, Button

input_box = None
submit_btn = None
current_mother_id = None


def init_scene(ui_mgr, mother_id):
    global input_box, submit_btn, current_mother_id
    current_mother_id = mother_id
    if not input_box:
        input_box = InputBox(config.SCREEN_WIDTH // 2 - 100, 400, 200, 50, ui_mgr.fonts["normal"])
        submit_btn = Button(config.SCREEN_WIDTH // 2 - 100, 480, 200, 50, "确认赐名", ui_mgr.fonts["normal"],
                            (144, 238, 144))


def handle_event(event, state, ui_mgr):
    global input_box
    res = input_box.handle_event(event)

    # 点击确认或按回车提交
    if res == "SUBMIT" or submit_btn.is_clicked(event):
        name = input_box.text.strip()
        if not name: name = "无名"

        # 1. 调用底层逻辑生成子嗣（此时才会真正加入列表和宫殿！）
        trigger_birth(state, current_mother_id, name)

        # 2. 检查队列里是否还有其他待产妃子
        if ui_mgr.birth_queue:
            next_mother = ui_mgr.birth_queue.pop(0)
            input_box.text = ""
            init_scene(ui_mgr, next_mother)
        else:
            # 全部起名完成，回到皇帝寝宫
            state.current_state = "emperor_palace"
            input_box.text = ""


def draw(screen, state, ui_mgr):
    screen.fill((20, 20, 20))  # 纯黑背景增加仪式感

    mother = next((c for c in state.concubine_list if c.id == current_mother_id), None)
    m_name = mother.name if mother else "某妃嫔"

    draw_text(screen, "✦ 皇家喜讯 ✦", ui_mgr.fonts["title"], config.GOLD, config.SCREEN_WIDTH // 2, 150, center=True)
    draw_text(screen, f"启奏皇上：【{m_name}】娘娘顺产，诞下一名皇嗣！", ui_mgr.fonts["normal"], config.WHITE,
              config.SCREEN_WIDTH // 2, 250, center=True)
    draw_text(screen, "请为皇子/公主赐名（仅限名，将随皇姓）：", ui_mgr.fonts["normal"], config.GRAY,
              config.SCREEN_WIDTH // 2, 320, center=True)

    input_box.draw(screen)
    submit_btn.draw(screen)