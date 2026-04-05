customform remove "user_interface/modal/edit_toggle"
customform add "user_interface/modal/edit_toggle" modal
editmodalform "user_interface/modal/edit_toggle" title "return '编辑开关'"



editmodalform "user_interface/modal/edit_toggle" append header
editlabel "user_interface/modal/edit_toggle" 0 header "return '标题文本'"
editmodalform "user_interface/modal/edit_toggle" append divider
editmodalform "user_interface/modal/edit_toggle" append input
editinput "user_interface/modal/edit_toggle" 2 text "return '请输入要设置的标题文本'"
editinput "user_interface/modal/edit_toggle" 2 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_toggle" 2 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_toggle" append header
editlabel "user_interface/modal/edit_toggle" 3 header "return '默认状态'"
editmodalform "user_interface/modal/edit_toggle" append divider
editmodalform "user_interface/modal/edit_toggle" append input
editinput "user_interface/modal/edit_toggle" 5 text "return '当该指令成功时将开关设置为开'"
editinput "user_interface/modal/edit_toggle" 5 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_toggle" 5 tooltip "return '如果指令执行失败，或指令为空，则开关将设置为关。'"

editmodalform "user_interface/modal/edit_toggle" append header
editlabel "user_interface/modal/edit_toggle" 6 header "return '灯泡提示文本'"
editmodalform "user_interface/modal/edit_toggle" append divider
editmodalform "user_interface/modal/edit_toggle" append input
editinput "user_interface/modal/edit_toggle" 8 text "return '当该指令成功时显示灯泡提示文本'"
editinput "user_interface/modal/edit_toggle" 8 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_toggle" 8 tooltip "return '置空将视作命令执行成功。'"
editmodalform "user_interface/modal/edit_toggle" append input
editinput "user_interface/modal/edit_toggle" 9 text "return '灯泡提示文本'"
editinput "user_interface/modal/edit_toggle" 9 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_toggle" 9 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_toggle" append header
editlabel "user_interface/modal/edit_toggle" 10 header "return '指令设置'"
editmodalform "user_interface/modal/edit_toggle" append label
editlabel "user_interface/modal/edit_toggle" 11 label "return '下面将设置当表单提交时要执行的指令。'"
editmodalform "user_interface/modal/edit_toggle" append label
editlabel "user_interface/modal/edit_toggle" 12 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/modal/edit_toggle" append divider



customform save "user_interface/modal/edit_toggle"