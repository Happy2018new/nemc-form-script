customform remove "user_interface/modal/add"
customform add "user_interface/modal/add" long
editlongform "user_interface/modal/add" title "return '添加元素'"
editlongform "user_interface/modal/add" content "return '您正在向模态表单添加新元素。\\n请选择您要添加的新元素。'"



editlongform "user_interface/modal/add" append header
editlabel "user_interface/modal/add" 0 header "return '文本控件'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 1 text "return '普通文本'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 2 text "return '大字文本'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 3 text "return '分割线'"

editlongform "user_interface/modal/add" append header
editlabel "user_interface/modal/add" 4 header "return '可输入控件'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 5 text "return '输入框'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 6 text "return '开关'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 7 text "return '下拉框'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 8 text "return '隐式步进滑块'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 9 text "return '显式步进滑块'"

editlongform "user_interface/modal/add" append header
editlabel "user_interface/modal/add" 10 header "return '其他操作'"
editlongform "user_interface/modal/add" append button
editbutton "user_interface/modal/add" 11 text "return '返回上一级'"



customform save "user_interface/modal/add"