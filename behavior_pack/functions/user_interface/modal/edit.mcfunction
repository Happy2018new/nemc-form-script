customform remove "user_interface/modal/edit"
customform add "user_interface/modal/edit" long
editlongform "user_interface/modal/edit" title "return '编辑已有元素'"
editlongform "user_interface/modal/edit" content "return '请选择您要编辑的元素。'"

editlongform "user_interface/modal/edit" append button
editbutton "user_interface/modal/edit" 0 text "return '返回上一级'"

customform save "user_interface/modal/edit"