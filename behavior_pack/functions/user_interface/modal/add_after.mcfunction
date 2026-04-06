customform remove "user_interface/modal/add_after"
customform add "user_interface/modal/add_after" popup

editpopupform "user_interface/modal/add_after" title "return '提示'"
editpopupform "user_interface/modal/add_after" content "return '您已成功添加元素，现在要编辑它吗？'"
editpopupform "user_interface/modal/add_after" button1 "return '是这样的，让我编辑'"
editpopupform "user_interface/modal/add_after" button2 "return '不了吧'"

customform save "user_interface/modal/add_after"