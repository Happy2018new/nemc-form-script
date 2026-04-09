customform remove "user_interface/pivot"
customform add "user_interface/pivot" long
editlongform "user_interface/pivot" title "return '选择表单类型'"
editlongform "user_interface/pivot" content "return '请选择您要操作的表单的类型。'"



editlongform "user_interface/pivot" append button
editbutton "user_interface/pivot" 0 text "return '长表单'"
editlongform "user_interface/pivot" append button
editbutton "user_interface/pivot" 1 text "return '信息表单'"
editlongform "user_interface/pivot" append button
editbutton "user_interface/pivot" 2 text "return '模态表单'"
editlongform "user_interface/pivot" append button
editbutton "user_interface/pivot" 3 text "return '返回上一级'"



customform save "user_interface/pivot"