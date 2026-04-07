customform remove "user_interface/long/edit"
customform add "user_interface/long/edit" long
editlongform "user_interface/long/edit" title "return '编辑已有元素'"
editlongform "user_interface/long/edit" content "return '请选择您要编辑的元素。'"

editlongform "user_interface/long/edit" append button
editbutton "user_interface/long/edit" 0 text "return '返回上一级'"

customform save "user_interface/long/edit"