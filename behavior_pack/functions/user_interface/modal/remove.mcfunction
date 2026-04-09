customform remove "user_interface/modal/remove"
customform add "user_interface/modal/remove" long
editlongform "user_interface/modal/remove" title "return '移除已有元素'"
editlongform "user_interface/modal/remove" content "return '请选择您要移除的元素。'"

editlongform "user_interface/modal/remove" append button
editbutton "user_interface/modal/remove" 0 text "return '返回上一级'"

customform save "user_interface/modal/remove"