customform remove "user_interface/long/edit_button_cmd"
customform add "user_interface/long/edit_button_cmd" modal
editmodalform "user_interface/long/edit_button_cmd" title "return '当按钮点击の瞬间'"



editmodalform "user_interface/long/edit_button_cmd" append header
editlabel "user_interface/long/edit_button_cmd" 0 header "return '指令设置'"
editmodalform "user_interface/long/edit_button_cmd" append label
editlabel "user_interface/long/edit_button_cmd" 1 label "return '下面将设置当玩家点击该按钮时要执行的指令。'"
editmodalform "user_interface/long/edit_button_cmd" append label
editlabel "user_interface/long/edit_button_cmd" 2 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/long/edit_button_cmd" append divider



customform save "user_interface/long/edit_button_cmd"