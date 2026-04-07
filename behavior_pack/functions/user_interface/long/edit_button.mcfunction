customform remove "user_interface/long/edit_button"
customform add "user_interface/long/edit_button" long
editlongform "user_interface/long/edit_button" title "return '编辑按钮'"
editlongform "user_interface/long/edit_button" content "return '请选择您要进行的操作。'"



editlongform "user_interface/long/edit_button" append header
editlabel "user_interface/long/edit_button" 0 header "return '按钮样式'"
editlongform "user_interface/long/edit_button" append button
editbutton "user_interface/long/edit_button" 1 text "return '设置内容文本'"
editlongform "user_interface/long/edit_button" append button
editbutton "user_interface/long/edit_button" 2 text "return '设置贴图图标'"

editlongform "user_interface/long/edit_button" append header
editlabel "user_interface/long/edit_button" 3 header "return '指令设置'"
editlongform "user_interface/long/edit_button" append button
editbutton "user_interface/long/edit_button" 4 text "return '当按钮被点击时'"

editlongform "user_interface/long/edit_button" append header
editlabel "user_interface/long/edit_button" 5 header "return '其他操作'"
editlongform "user_interface/long/edit_button" append button
editbutton "user_interface/long/edit_button" 6 text "return '返回上一级'"



customform save "user_interface/long/edit_button"