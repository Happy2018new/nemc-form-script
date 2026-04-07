customform remove "user_interface/long/edit_button_panel"
customform add "user_interface/long/edit_button_panel" long
editlongform "user_interface/long/edit_button_panel" title "return '编辑按钮'"
editlongform "user_interface/long/edit_button_panel" content "return '请选择您要进行的操作。'"



editlongform "user_interface/long/edit_button_panel" append header
editlabel "user_interface/long/edit_button_panel" 0 header "return '按钮样式'"
editlongform "user_interface/long/edit_button_panel" append button
editbutton "user_interface/long/edit_button_panel" 1 text "return '设置内容文本'"
editlongform "user_interface/long/edit_button_panel" append button
editbutton "user_interface/long/edit_button_panel" 2 text "return '设置贴图图标'"

editlongform "user_interface/long/edit_button_panel" append header
editlabel "user_interface/long/edit_button_panel" 3 header "return '指令设置'"
editlongform "user_interface/long/edit_button_panel" append button
editbutton "user_interface/long/edit_button_panel" 4 text "return '当按钮被点击时'"

editlongform "user_interface/long/edit_button_panel" append header
editlabel "user_interface/long/edit_button_panel" 5 header "return '其他操作'"
editlongform "user_interface/long/edit_button_panel" append button
editbutton "user_interface/long/edit_button_panel" 6 text "return '返回上一级'"



customform save "user_interface/long/edit_button_panel"