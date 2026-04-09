customform remove "user_interface/panel"
customform add "user_interface/panel" long
editlongform "user_interface/panel" title "return '菜单编辑器'"
editlongform "user_interface/panel" content "return 'Chapter 12 | flowers for m[A]chines'"



editlongform "user_interface/panel" append header
editlabel "user_interface/panel" 0 header "return '操作菜单'"
editlongform "user_interface/panel" append button
editbutton "user_interface/panel" 1 text "return '添加新的菜单'"
editlongform "user_interface/panel" append button
editbutton "user_interface/panel" 2 text "return '编辑已有菜单'"
editlongform "user_interface/panel" append button
editbutton "user_interface/panel" 3 text "return '移除已有菜单'"

editlongform "user_interface/panel" append header
editlabel "user_interface/panel" 4 header "return '帮助信息'"
editlongform "user_interface/panel" append button
editbutton "user_interface/panel" 5 text "return '查看帮助信息'"

editlongform "user_interface/panel" append header
editlabel "user_interface/panel" 6 header "return '其他操作'"
editlongform "user_interface/panel" append button
editbutton "user_interface/panel" 7 text "return '关闭本编辑器'"



customform save "user_interface/panel"