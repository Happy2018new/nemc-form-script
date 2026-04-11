customform remove "user_interface/cancel_normal"
customform add "user_interface/cancel_normal" modal
editmodalform "user_interface/cancel_normal" title "return '当表单关闭の瞬间'"



editmodalform "user_interface/cancel_normal" append header
editlabel "user_interface/cancel_normal" 0 header "return '指令设置'"
editmodalform "user_interface/cancel_normal" append label
editlabel "user_interface/cancel_normal" 1 label "return '下面将设置当表单被玩家§e手动叉掉§r时要执行的指令。\\n§e手动叉掉§r意味着玩家通过点击叉号手动关闭了菜单。'"
editmodalform "user_interface/cancel_normal" append label
editlabel "user_interface/cancel_normal" 2 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/cancel_normal" append divider



customform save "user_interface/cancel_normal"