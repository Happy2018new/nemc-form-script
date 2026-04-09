customform remove "user_interface/modal/panel"
customform add "user_interface/modal/panel" long
editlongform "user_interface/modal/panel" title "return '操作模态表单'"
editlongform "user_interface/modal/panel" content "return '您目前正在操作模态表单“{}”。\\n请选择您要进行的操作。'"


editlongform "user_interface/modal/panel" append header
editlabel "user_interface/modal/panel" 0 header "return '表单预览'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 1 text "return '预览表单'"

editlongform "user_interface/modal/panel" append header
editlabel "user_interface/modal/panel" 2 header "return '表单元素'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 3 text "return '添加元素'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 4 text "return '插入元素'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 5 text "return '编辑已有元素'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 6 text "return '移除已有元素'"

editlongform "user_interface/modal/panel" append header
editlabel "user_interface/modal/panel" 7 header "return '表单设置'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 8 text "return '设置标题文本'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 9 text "return '当表单关闭时'"

editlongform "user_interface/modal/panel" append header
editlabel "user_interface/modal/panel" 10 header "return '其他操作'"
editlongform "user_interface/modal/panel" append button
editbutton "user_interface/modal/panel" 11 text "return '返回上一级'"



customform save "user_interface/modal/panel"