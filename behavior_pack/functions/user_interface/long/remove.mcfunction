customform remove "user_interface/long/remove"
customform add "user_interface/long/remove" long
editlongform "user_interface/long/remove" title "return '移除已有元素'"
editlongform "user_interface/long/remove" content "return '请选择您要移除的元素。'"

editlongform "user_interface/long/remove" append button
editbutton "user_interface/long/remove" 0 text "return '返回上一级'"

customform save "user_interface/long/remove"