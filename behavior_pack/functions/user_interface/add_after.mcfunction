customform remove "user_interface/add_after_popup"
customform add "user_interface/add_after_popup" popup

editpopupform "user_interface/add_after_popup" title "return '提示'"
editpopupform "user_interface/add_after_popup" content "return '目标表单已成功添加，现在要编辑它吗？'"
editpopupform "user_interface/add_after_popup" button1 "return '是这样的，让我编辑'"
editpopupform "user_interface/add_after_popup" button2 "return '不了吧'"

customform save "user_interface/add_after_popup"



customform remove "user_interface/add_after_failed"
customform add "user_interface/add_after_failed" popup

editpopupform "user_interface/add_after_failed" title "return '错误'"
editpopupform "user_interface/add_after_failed" content "return '目标表单添加失败，请检查提供的表单名称是否与已有表单重复？'"
editpopupform "user_interface/add_after_failed" button1 "return '好的'"
editpopupform "user_interface/add_after_failed" button2 "return '继续'"

customform save "user_interface/add_after_failed"