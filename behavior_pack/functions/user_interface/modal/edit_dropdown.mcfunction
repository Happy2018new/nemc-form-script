customform remove "user_interface/modal/edit_dropdown"
customform add "user_interface/modal/edit_dropdown" modal
editmodalform "user_interface/modal/edit_dropdown" title "return '编辑下拉框'"



editmodalform "user_interface/modal/edit_dropdown" append header
editlabel "user_interface/modal/edit_dropdown" 0 header "return '标题文本'"
editmodalform "user_interface/modal/edit_dropdown" append divider
editmodalform "user_interface/modal/edit_dropdown" append input
editinput "user_interface/modal/edit_dropdown" 2 text "return '请输入要设置的标题文本'"
editinput "user_interface/modal/edit_dropdown" 2 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_dropdown" 2 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_dropdown" append header
editlabel "user_interface/modal/edit_dropdown" 3 header "return '默认选项'"
editmodalform "user_interface/modal/edit_dropdown" append divider
editmodalform "user_interface/modal/edit_dropdown" append input
editinput "user_interface/modal/edit_dropdown" 5 text "return '设置下拉框默认选中选项的索引'"
editinput "user_interface/modal/edit_dropdown" 5 placeholder "return '#-#@s#选项记分板#'"
editinput "user_interface/modal/edit_dropdown" 5 tooltip "return '§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b选项索引§r\\n  第 §b1§r 个选项的索引为 §e0§r。\\n  第 §b2§r 个选项的索引为 §e1§r。\\n  第 §b3§r 个选项的索引为 §e2§r。\\n  第 §bn§r 个选项的索引为 §en-1§r。\\n§b其他说明§r\\n  置空将视作使用第 §b1§r 个选项。'"

editmodalform "user_interface/modal/edit_dropdown" append header
editlabel "user_interface/modal/edit_dropdown" 6 header "return '灯泡提示文本'"
editmodalform "user_interface/modal/edit_dropdown" append divider
editmodalform "user_interface/modal/edit_dropdown" append input
editinput "user_interface/modal/edit_dropdown" 8 text "return '当该指令成功时显示灯泡提示文本'"
editinput "user_interface/modal/edit_dropdown" 8 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_dropdown" 8 tooltip "return '置空将视作命令执行成功。'"
editmodalform "user_interface/modal/edit_dropdown" append input
editinput "user_interface/modal/edit_dropdown" 9 text "return '灯泡提示文本'"
editinput "user_interface/modal/edit_dropdown" 9 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_dropdown" 9 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_dropdown" append header
editlabel "user_interface/modal/edit_dropdown" 10 header "return '选项设置'"
editmodalform "user_interface/modal/edit_dropdown" append label
editlabel "user_interface/modal/edit_dropdown" 11 label "return '下面将设置下拉框中可以出现的选项。'"
editmodalform "user_interface/modal/edit_dropdown" append label
editlabel "user_interface/modal/edit_dropdown" 12 label "return '当填写满所有输入框后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多选项。'"
editmodalform "user_interface/modal/edit_dropdown" append divider

editmodalform "user_interface/modal/edit_dropdown" append header
editlabel "user_interface/modal/edit_dropdown" 14 header "return '指令设置'"
editmodalform "user_interface/modal/edit_dropdown" append label
editlabel "user_interface/modal/edit_dropdown" 15 label "return '下面将设置当表单提交时要执行的指令。'"
editmodalform "user_interface/modal/edit_dropdown" append label
editlabel "user_interface/modal/edit_dropdown" 16 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/modal/edit_dropdown" append divider



customform save "user_interface/modal/edit_dropdown"