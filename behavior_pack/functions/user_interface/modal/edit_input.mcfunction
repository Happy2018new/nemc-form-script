customform remove "user_interface/modal/edit_input"
customform add "user_interface/modal/edit_input" modal
editmodalform "user_interface/modal/edit_input" title "return '编辑输入框'"



editmodalform "user_interface/modal/edit_input" append header
editlabel "user_interface/modal/edit_input" 0 header "return '标题文本'"
editmodalform "user_interface/modal/edit_input" append divider
editmodalform "user_interface/modal/edit_input" append input
editinput "user_interface/modal/edit_input" 2 text "return '请输入要设置的标题文本'"
editinput "user_interface/modal/edit_input" 2 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_input" 2 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#分数#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_input" append header
editlabel "user_interface/modal/edit_input" 3 header "return '提示文本'"
editmodalform "user_interface/modal/edit_input" append divider
editmodalform "user_interface/modal/edit_input" append input
editinput "user_interface/modal/edit_input" 5 text "return '当该指令成功时显示提示文本'"
editinput "user_interface/modal/edit_input" 5 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_input" 5 tooltip "return '置空将视作命令执行成功。'"
editmodalform "user_interface/modal/edit_input" append input
editinput "user_interface/modal/edit_input" 6 text "return '要显示的提示文本'"
editinput "user_interface/modal/edit_input" 6 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_input" 6 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#分数#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_input" append header
editlabel "user_interface/modal/edit_input" 7 header "return '默认文本'"
editmodalform "user_interface/modal/edit_input" append divider
editmodalform "user_interface/modal/edit_input" append input
editinput "user_interface/modal/edit_input" 9 text "return '当该指令成功时显示默认文本'"
editinput "user_interface/modal/edit_input" 9 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_input" 9 tooltip "return '置空将视作命令执行成功。'"
editmodalform "user_interface/modal/edit_input" append input
editinput "user_interface/modal/edit_input" 10 text "return '要显示的默认文本'"
editinput "user_interface/modal/edit_input" 10 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_input" 10 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#分数#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_input" append header
editlabel "user_interface/modal/edit_input" 11 header "return '灯泡提示文本'"
editmodalform "user_interface/modal/edit_input" append divider
editmodalform "user_interface/modal/edit_input" append input
editinput "user_interface/modal/edit_input" 13 text "return '当该指令成功时显示灯泡提示文本'"
editinput "user_interface/modal/edit_input" 13 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_input" 13 tooltip "return '置空将视作命令执行成功。'"
editmodalform "user_interface/modal/edit_input" append input
editinput "user_interface/modal/edit_input" 14 text "return '灯泡提示文本'"
editinput "user_interface/modal/edit_input" 14 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_input" 14 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#分数#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_input" append header
editlabel "user_interface/modal/edit_input" 15 header "return '指令设置'"
editmodalform "user_interface/modal/edit_input" append label
editlabel "user_interface/modal/edit_input" 16 label "return '下面将设置当表单提交时要执行的指令。'"
editmodalform "user_interface/modal/edit_input" append label
editlabel "user_interface/modal/edit_input" 17 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/modal/edit_input" append divider



customform save "user_interface/modal/edit_input"