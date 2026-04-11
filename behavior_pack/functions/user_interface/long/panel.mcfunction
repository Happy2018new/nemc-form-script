customform remove "user_interface/long/panel"
customform add "user_interface/long/panel" long
editlongform "user_interface/long/panel" title "return '操作长表单'"
editlongform "user_interface/long/panel" content "return '您目前正在操作长表单“{}”。\\n请选择您要进行的操作。'"


editlongform "user_interface/long/panel" append header
editlabel "user_interface/long/panel" 0 header "return '表单预览'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 1 text "return '预览表单'"

editlongform "user_interface/long/panel" append header
editlabel "user_interface/long/panel" 2 header "return '表单元素'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 3 text "return '添加元素'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 4 text "return '插入元素'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 5 text "return '编辑已有元素'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 6 text "return '移除已有元素'"

editlongform "user_interface/long/panel" append header
editlabel "user_interface/long/panel" 7 header "return '表单设置'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 8 text "return '设置标题和内容'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 9 text "return '当表单关闭时'"

editlongform "user_interface/long/panel" append header
editlabel "user_interface/long/panel" 10 header "return '其他操作'"
editlongform "user_interface/long/panel" append button
editbutton "user_interface/long/panel" 11 text "return '返回上一级'"



customform save "user_interface/long/panel"