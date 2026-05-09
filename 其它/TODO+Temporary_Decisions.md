1. ### 问题

2. ### 临时约定

- 东西六宫： 景仁宫, 延禧宫, 承乾宫, 翊坤宫, 永和宫, 钟粹宫

> (MVP 阶段可以直接给这些宫殿设定 capacity = 3 或类似数值，初始自动把它们实例化进 GameState.palace_list)

供 config.AVAILABLE_TRAVEL_PLACES 使用的皇家园林和风景名胜：

> 地点： 御花园, 畅春园, 圆明园, 避暑山庄, 太液池, 昆明湖

3. Todo:
  - [ ] 把立绘改成随机立绘
  - [ ] 视觉与听觉觉醒
  - [ ] 丰富随机事件
  - [ ] #-把秀女名字的改成随机的
  - [ ] 更完善的测试数据生成工具（比如随机生成一批妃子和子嗣数据，自动存成 json 文件，方便测试）
  - [ ] 更完善覆盖更多边界情况的单元测试
  - [ ] config里面那个100改成无限
  - [ ] 实现时间在每个界面都有
  - [ ] 重构部分结构把saves改成output/saves,assert下新增picture和font,并修改对应的逻辑和文件
  - [ ] #Todo:实现玩家输入名字和持久化存储
  - [ ] 假如宫殿页面和宫殿内部的ui和logic以及更改位分的UI
  - [ ] #Todo:这里答应不要硬编码
  - [ ] 绘制更好的ui
  - [ ] #解决妃嫔最后一页上一页失效的问题
  - [ ] 打包成可执行文件
  - [ ] #绘制妃嫔剩余的属性和交互
  - [ ] 把字体改成自适应,目前更改成自动扫描会显示
```
Traceback (most recent call last):
  File "D:\develop\source\Py作品集\ai氛围_后宫游戏\src\main.py", line 26, in <module>
    main()
    ~~~~^^
  File "D:\develop\source\Py作品集\ai氛围_后宫游戏\src\main.py", line 18, in main
    ui_mgr = UIManager(state)
  File "D:\develop\source\Py作品集\ai氛围_后宫游戏\src\ui_manager\core.py", line 38, in __init__
    "normal": load_font(24, font_names_to_try),
              ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\develop\source\Py作品集\ai氛围_后宫游戏\src\ui_manager\core.py", line 27, in load_font
    font_path = pygame.font.match_font(font_name)
  File "D:\develop\source\Py作品集\ai氛围_后宫游戏\.venv\Lib\site-packages\pygame\sysfont.py", line 488, in match_font
    initsysfonts()
    ~~~~~~~~~~~~^^
  File "D:\develop\source\Py作品集\ai氛围_后宫游戏\.venv\Lib\site-packages\pygame\sysfont.py", line 355, in initsysfonts
    fonts = initsysfonts_win32()
  File "D:\develop\source\Py作品集\ai氛围_后宫游戏\.venv\Lib\site-packages\pygame\sysfont.py", line 82, in initsysfonts_win32
    if splitext(font)[1].lower() not in OpenType_extensions:
       ~~~~~~~~^^^^^^
  File "<frozen ntpath>", line 244, in splitext
TypeError: expected str, bytes or os.PathLike object, not int

进程已结束，退出代码为 1
```
