customform remove "user_interface/long/text"
customform add "user_interface/long/text" modal
editmodalform "user_interface/long/text" title "return '编辑长表单的标题和内容'"



editmodalform "user_interface/long/text" append header
editlabel "user_interface/long/text" 0 header "return '标题文本'"
editmodalform "user_interface/long/text" append divider
editmodalform "user_interface/long/text" append input
editinput "user_interface/long/text" 2 text "return '请输入要设置的标题文本'"
editinput "user_interface/long/text" 2 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/long/text" 2 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"

editmodalform "user_interface/long/text" append header
editlabel "user_interface/long/text" 3 header "return '内容文本'"
editmodalform "user_interface/long/text" append divider
editmodalform "user_interface/long/text" append input
editinput "user_interface/long/text" 5 text "return '请输入要设置的内容文本'"
editinput "user_interface/long/text" 5 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/long/text" 5 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"



customform save "user_interface/long/text"