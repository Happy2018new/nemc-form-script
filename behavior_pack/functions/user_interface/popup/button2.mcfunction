customform remove "user_interface/popup/button2"
customform add "user_interface/popup/button2" modal
editmodalform "user_interface/popup/button2" title "return '编辑取消按钮'"



editmodalform "user_interface/popup/button2" append header
editlabel "user_interface/popup/button2" 0 header "return '内容文本'"
editmodalform "user_interface/popup/button2" append label
editlabel "user_interface/popup/button2" 1 label "return '您正在编辑代表“取消”的按钮的内容文本。'"
editmodalform "user_interface/popup/button2" append divider
editmodalform "user_interface/popup/button2" append input
editinput "user_interface/popup/button2" 3 text "return '请输入要设置的内容文本'"
editinput "user_interface/popup/button2" 3 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/popup/button2" 3 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/popup/button2" append header
editlabel "user_interface/popup/button2" 4 header "return '指令设置'"
editmodalform "user_interface/popup/button2" append label
editlabel "user_interface/popup/button2" 5 label "return '您将设置当玩家点击该按钮时要执行的命令。\\n这通常意味着玩家点击了代表“取消”的按钮。'"
editmodalform "user_interface/popup/button2" append label
editlabel "user_interface/popup/button2" 6 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/popup/button2" append divider



customform save "user_interface/popup/button2"