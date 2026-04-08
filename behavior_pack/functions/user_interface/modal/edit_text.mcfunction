customform remove "user_interface/modal/edit_text"
customform add "user_interface/modal/edit_text" modal
editmodalform "user_interface/modal/edit_text" title "return '{} ({})'"



editmodalform "user_interface/modal/edit_text" append label
editlabel "user_interface/modal/edit_text" 0 label "return '您正在编辑模态表单中的文本元素。'"

editmodalform "user_interface/modal/edit_text" append input
editinput "user_interface/modal/edit_text" 1 text "return '请输入要设置的文本内容'"
editinput "user_interface/modal/edit_text" 1 placeholder "return '我叫 $-$@s$ 且我有 #-#@s#金币# 个金币'"
editinput "user_interface/modal/edit_text" 1 tooltip "return '§b$条件(选择器)$内容(选择器/纯文本)$§r\\n  表示实体名或纯文本(用“§e-§r”代表无需条件)。\\n§b#条件(选择器)#目标#记分板#§r\\n  表示分数(用“§e-§r”代表无需条件)。\\n§b$$§r, §b##§r 和 §b\\\\n§r\\n  分别表示 §e$§r, §e#§r 和 §e换行§r。'"



customform save "user_interface/modal/edit_text"