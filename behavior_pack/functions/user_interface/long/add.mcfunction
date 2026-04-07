customform remove "user_interface/long/add"
customform add "user_interface/long/add" long
editlongform "user_interface/long/add" title "return '添加元素'"
editlongform "user_interface/long/add" content "return '您正在向长表单添加新元素。\\n请选择您要添加的新元素。'"



editlongform "user_interface/long/add" append header
editlabel "user_interface/long/add" 0 header "return '可点击控件'"
editlongform "user_interface/long/add" append button
editbutton "user_interface/long/add" 1 text "return '按钮'"

editlongform "user_interface/long/add" append header
editlabel "user_interface/long/add" 2 header "return '文本控件'"
editlongform "user_interface/long/add" append button
editbutton "user_interface/long/add" 3 text "return '普通文本'"
editlongform "user_interface/long/add" append button
editbutton "user_interface/long/add" 4 text "return '大字文本'"
editlongform "user_interface/long/add" append button
editbutton "user_interface/long/add" 5 text "return '分割线'"

editlongform "user_interface/long/add" append header
editlabel "user_interface/long/add" 6 header "return '其他操作'"
editlongform "user_interface/long/add" append button
editbutton "user_interface/long/add" 7 text "return '返回上一级'"



customform save "user_interface/long/add"