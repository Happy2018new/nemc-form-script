customform remove "user_interface/modal/edit_step_slider"
customform add "user_interface/modal/edit_step_slider" modal
editmodalform "user_interface/modal/edit_step_slider" title "return '显式步进滑块 ({})'"



editmodalform "user_interface/modal/edit_step_slider" append header
editlabel "user_interface/modal/edit_step_slider" 0 header "return '标题文本'"
editmodalform "user_interface/modal/edit_step_slider" append divider
editmodalform "user_interface/modal/edit_step_slider" append input
editinput "user_interface/modal/edit_step_slider" 2 text "return '请输入要设置的标题文本'"
editinput "user_interface/modal/edit_step_slider" 2 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_step_slider" 2 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_step_slider" append header
editlabel "user_interface/modal/edit_step_slider" 3 header "return '默认选项'"
editmodalform "user_interface/modal/edit_step_slider" append divider
editmodalform "user_interface/modal/edit_step_slider" append input
editinput "user_interface/modal/edit_step_slider" 5 text "return '设置滑块默认选中选项的索引'"
editinput "user_interface/modal/edit_step_slider" 5 placeholder "return '#-#@s#选项记分板#'"
editinput "user_interface/modal/edit_step_slider" 5 tooltip "return '§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b选项索引§r\\n  第 §b1§r 个选项的索引为 §e0§r。\\n  第 §b2§r 个选项的索引为 §e1§r。\\n  第 §b3§r 个选项的索引为 §e2§r。\\n  第 §bn§r 个选项的索引为 §en-1§r。\\n§b其他说明§r\\n  置空将视作使用第 §b1§r 个选项。'"

editmodalform "user_interface/modal/edit_step_slider" append header
editlabel "user_interface/modal/edit_step_slider" 6 header "return '灯泡提示文本'"
editmodalform "user_interface/modal/edit_step_slider" append divider
editmodalform "user_interface/modal/edit_step_slider" append input
editinput "user_interface/modal/edit_step_slider" 8 text "return '当该指令成功时显示灯泡提示文本'"
editinput "user_interface/modal/edit_step_slider" 8 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_step_slider" 8 tooltip "return '置空将视作命令执行成功。'"
editmodalform "user_interface/modal/edit_step_slider" append input
editinput "user_interface/modal/edit_step_slider" 9 text "return '灯泡提示文本'"
editinput "user_interface/modal/edit_step_slider" 9 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_step_slider" 9 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_step_slider" append header
editlabel "user_interface/modal/edit_step_slider" 10 header "return '选项设置'"
editmodalform "user_interface/modal/edit_step_slider" append label
editlabel "user_interface/modal/edit_step_slider" 11 label "return '下面将设置滑块中可以出现的选项。'"
editmodalform "user_interface/modal/edit_step_slider" append label
editlabel "user_interface/modal/edit_step_slider" 12 label "return '当填写满所有输入框后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多选项。'"
editmodalform "user_interface/modal/edit_step_slider" append divider

editmodalform "user_interface/modal/edit_step_slider" append header
editlabel "user_interface/modal/edit_step_slider" 14 header "return '指令设置'"
editmodalform "user_interface/modal/edit_step_slider" append label
editlabel "user_interface/modal/edit_step_slider" 15 label "return '下面将设置当表单提交时要执行的指令。'"
editmodalform "user_interface/modal/edit_step_slider" append label
editlabel "user_interface/modal/edit_step_slider" 16 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/modal/edit_step_slider" append divider



customform save "user_interface/modal/edit_step_slider"