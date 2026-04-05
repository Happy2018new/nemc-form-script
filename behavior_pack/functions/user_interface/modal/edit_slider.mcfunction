customform remove "user_interface/modal/edit_slider"
customform add "user_interface/modal/edit_slider" modal
editmodalform "user_interface/modal/edit_slider" title "return '编辑隐式步进滑块'"



editmodalform "user_interface/modal/edit_slider" append header
editlabel "user_interface/modal/edit_slider" 0 header "return '标题文本'"
editmodalform "user_interface/modal/edit_slider" append divider
editmodalform "user_interface/modal/edit_slider" append input
editinput "user_interface/modal/edit_slider" 2 text "return '请输入要设置的标题文本'"
editinput "user_interface/modal/edit_slider" 2 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_slider" 2 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_slider" append header
editlabel "user_interface/modal/edit_slider" 3 header "return '取值范围'"
editmodalform "user_interface/modal/edit_slider" append label
editlabel "user_interface/modal/edit_slider" 4 label "return '下面您将通过 3 个属性来控制取值范围。\\n隐式步进滑块的最小值、最大值和步进长度。'"
editmodalform "user_interface/modal/edit_slider" append divider
editmodalform "user_interface/modal/edit_slider" append input
editinput "user_interface/modal/edit_slider" 6 text "return '最小值'"
editinput "user_interface/modal/edit_slider" 6 placeholder "return '0'"
editinput "user_interface/modal/edit_slider" 6 tooltip "return '最小值是滑块可滑到的§e最小的数§r。\\n须填写§e整数§r，并且应当是个§e常数§r。'"
editmodalform "user_interface/modal/edit_slider" append input
editinput "user_interface/modal/edit_slider" 7 text "return '最大值'"
editinput "user_interface/modal/edit_slider" 7 placeholder "return '1'"
editinput "user_interface/modal/edit_slider" 7 tooltip "return '最大值是滑块可滑到的§e最大的数§r。\\n须填写§e整数§r，并且应当是个§e常数§r。'"
editmodalform "user_interface/modal/edit_slider" append input
editinput "user_interface/modal/edit_slider" 8 text "return '步进长度'"
editinput "user_interface/modal/edit_slider" 8 placeholder "return '1'"
editinput "user_interface/modal/edit_slider" 8 tooltip "return '步进长度是滑块可滑动的§e最小刻度§r。\\n须填写§b正整数§r，并且应当是个§e常数§r。'"

editmodalform "user_interface/modal/edit_slider" append header
editlabel "user_interface/modal/edit_slider" 9 header "return '默认值'"
editmodalform "user_interface/modal/edit_slider" append label
editlabel "user_interface/modal/edit_slider" 10 label "return '不同于最小值、最大值和步进长度，\\n这里允许使用记分板上的分数作为默认值。'"
editmodalform "user_interface/modal/edit_slider" append divider
editmodalform "user_interface/modal/edit_slider" append input
editinput "user_interface/modal/edit_slider" 12 text "return '请输入滑块的默认值'"
editinput "user_interface/modal/edit_slider" 12 placeholder "return '#-#@s#默认值记分板#'"
editinput "user_interface/modal/edit_slider" 12 tooltip "return '§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b其他说明§r\\n  应确保默认值不会超出滑块的§e取值范围§r。\\n  置空将视作使用§e最小值§r作为默认值。'"

editmodalform "user_interface/modal/edit_slider" append header
editlabel "user_interface/modal/edit_slider" 13 header "return '灯泡提示文本'"
editmodalform "user_interface/modal/edit_slider" append divider
editmodalform "user_interface/modal/edit_slider" append input
editinput "user_interface/modal/edit_slider" 15 text "return '当该指令成功时显示灯泡提示文本'"
editinput "user_interface/modal/edit_slider" 15 placeholder "return 'testfor @s[tag=Hello]'"
editinput "user_interface/modal/edit_slider" 15 tooltip "return '置空将视作命令执行成功。'"
editmodalform "user_interface/modal/edit_slider" append input
editinput "user_interface/modal/edit_slider" 16 text "return '灯泡提示文本'"
editinput "user_interface/modal/edit_slider" 16 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_slider" 16 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/modal/edit_slider" append header
editlabel "user_interface/modal/edit_slider" 17 header "return '指令设置'"
editmodalform "user_interface/modal/edit_slider" append label
editlabel "user_interface/modal/edit_slider" 18 label "return '下面将设置当表单提交时要执行的指令。'"
editmodalform "user_interface/modal/edit_slider" append label
editlabel "user_interface/modal/edit_slider" 19 label "return '当填写满所有的指令后，在您下次进入本界面时，\\n您将看到新的输入框，从而您可以设置更多指令。'"
editmodalform "user_interface/modal/edit_slider" append divider



customform save "user_interface/modal/edit_slider"