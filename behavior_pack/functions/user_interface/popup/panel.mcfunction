customform remove "user_interface/popup/panel"
customform add "user_interface/popup/panel" long
editlongform "user_interface/popup/panel" title "return '操作信息表单'"
editlongform "user_interface/popup/panel" content "return '您目前正在操作信息表单“{}”。\\n请选择您要设置的部分。'"



editlongform "user_interface/popup/panel" append header
editlabel "user_interface/popup/panel" 0 header "return '表单预览'"
editlongform "user_interface/popup/panel" append button
editbutton "user_interface/popup/panel" 1 text "return '预览表单'"

editlongform "user_interface/popup/panel" append header
editlabel "user_interface/popup/panel" 2 header "return '表单按钮'"
editlongform "user_interface/popup/panel" append button
editbutton "user_interface/popup/panel" 3 text "return '设置确定按钮'"
editlongform "user_interface/popup/panel" append button
editbutton "user_interface/popup/panel" 4 text "return '设置取消按钮'"

editlongform "user_interface/popup/panel" append header
editlabel "user_interface/popup/panel" 5 header "return '表单设置'"
editlongform "user_interface/popup/panel" append button
editbutton "user_interface/popup/panel" 6 text "return '设置标题和内容'"
editlongform "user_interface/popup/panel" append button
editbutton "user_interface/popup/panel" 7 text "return '当表单关闭时'"

editlongform "user_interface/popup/panel" append header
editlabel "user_interface/popup/panel" 8 header "return '其他操作'"
editlongform "user_interface/popup/panel" append button
editbutton "user_interface/popup/panel" 9 text "return '返回上一级'"



customform save "user_interface/popup/panel"