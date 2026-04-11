customform remove "user_interface/long/edit_divider"
customform add "user_interface/long/edit_divider" popup

editpopupform "user_interface/long/edit_divider" title "return '提示'"
editpopupform "user_interface/long/edit_divider" content "return '分割线无需进一步编辑。'"
editpopupform "user_interface/long/edit_divider" button1 "return '我知道了'"
editpopupform "user_interface/long/edit_divider" button2 "return '继续'"

customform save "user_interface/long/edit_divider"