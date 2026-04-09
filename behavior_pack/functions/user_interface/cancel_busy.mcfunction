customform remove "user_interface/cancel_busy"
customform add "user_interface/cancel_busy" modal
editmodalform "user_interface/cancel_busy" title "return '当表单关闭の瞬间'"



editmodalform "user_interface/cancel_busy" append header
editlabel "user_interface/cancel_busy" 0 header "return '指令设置'"
editmodalform "user_interface/cancel_busy" append label
editlabel "user_interface/cancel_busy" 1 label "return '下面将设置因§e玩家正忙§r而关闭表单时要执行的指令。'"
editmodalform "user_interface/cancel_busy" append label
editlabel "user_interface/cancel_busy" 2 label "return '§e玩家正忙§r指的是玩家当前已打开了一个页面，\\n例如该玩家已经打开了一个聊天栏或表单。'"
editmodalform "user_interface/cancel_busy" append label
editlabel "user_interface/cancel_busy" 3 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/cancel_busy" append divider



customform save "user_interface/cancel_busy"