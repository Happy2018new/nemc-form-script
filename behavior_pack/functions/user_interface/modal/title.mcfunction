customform remove "user_interface/modal/title"
customform add "user_interface/modal/title" modal
editmodalform "user_interface/modal/title" title "return '编辑模态表单的标题'"



editmodalform "user_interface/modal/title" append label
editlabel "user_interface/modal/title" 0 label "return '您正在设置模态表单的标题文本。'"
editmodalform "user_interface/modal/title" append input
editinput "user_interface/modal/title" 1 text "return '请输入要设置的标题文本'"
editinput "user_interface/modal/title" 1 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/title" 1 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"



customform save "user_interface/modal/title"