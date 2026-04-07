customform remove "user_interface/modal/confirm_remove"
customform add "user_interface/modal/confirm_remove" popup

editpopupform "user_interface/modal/confirm_remove" title "return '二重确认'"
editpopupform "user_interface/modal/confirm_remove" content "return '您真的要§c删除§r目标元素吗？'"
editpopupform "user_interface/modal/confirm_remove" button1 "return '确定'"
editpopupform "user_interface/modal/confirm_remove" button2 "return '取消'"

customform save "user_interface/modal/confirm_remove"