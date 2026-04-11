customform remove "user_interface/cancel"
customform add "user_interface/cancel" long
editlongform "user_interface/cancel" title "return '设置表单关闭时要执行的指令'"
editlongform "user_interface/cancel" content "return '请选择一个选项以开始设置。'"



editlongform "user_interface/cancel" append button
editbutton "user_interface/cancel" 0 text "return '当表单被玩家叉掉时'"
editlongform "user_interface/cancel" append button
editbutton "user_interface/cancel" 1 text "return '当玩家正忙时'"
editlongform "user_interface/cancel" append button
editbutton "user_interface/cancel" 2 text "return '当玩家退出游戏时'"
editlongform "user_interface/cancel" append button
editbutton "user_interface/cancel" 3 text "return '返回上一级'"



customform save "user_interface/cancel"