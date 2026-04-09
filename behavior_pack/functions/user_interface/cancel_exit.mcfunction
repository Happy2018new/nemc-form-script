customform remove "user_interface/cancel_exit"
customform add "user_interface/cancel_exit" modal
editmodalform "user_interface/cancel_exit" title "return '当表单关闭の瞬间'"



editmodalform "user_interface/cancel_exit" append header
editlabel "user_interface/cancel_exit" 0 header "return '指令设置'"
editmodalform "user_interface/cancel_exit" append label
editlabel "user_interface/cancel_exit" 1 label "return '您将设置玩家§e突然退出游戏§r时要执行的指令。\\n这意味着玩家在与表单交互时突然退出了游戏。'"
editmodalform "user_interface/cancel_exit" append label
editlabel "user_interface/cancel_exit" 2 label "return '您有责任确保此时不会向玩家打开新的表单。\\n如果您这么做，则菜单系统可能会出现§c严重错误§r。'"
editmodalform "user_interface/cancel_exit" append label
editlabel "user_interface/cancel_exit" 3 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/cancel_exit" append divider



customform save "user_interface/cancel_exit"