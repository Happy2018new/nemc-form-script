customform remove "user_interface/confirm_remove"
customform add "user_interface/confirm_remove" popup

editpopupform "user_interface/confirm_remove" title "return '二重确认'"
editpopupform "user_interface/confirm_remove" content "return '您真的要§c删除§r目标表单吗？'"
editpopupform "user_interface/confirm_remove" button1 "return '确定'"
editpopupform "user_interface/confirm_remove" button2 "return '取消'"

customform save "user_interface/confirm_remove"