customform remove "user_interface/long/preview_button_icon"
customform add "user_interface/long/preview_button_icon" popup

editpopupform "user_interface/long/preview_button_icon" title "return '提示'"
editpopupform "user_interface/long/preview_button_icon" content "return '该按钮目前还没有设置任何贴图！'"
editpopupform "user_interface/long/preview_button_icon" button1 "return '现在去设置'"
editpopupform "user_interface/long/preview_button_icon" button2 "return '不必管它'"

customform save "user_interface/long/preview_button_icon"