customform remove "user_interface/modal/edit_text"
customform add "user_interface/modal/edit_text" modal
editmodalform "user_interface/modal/edit_text" title "return '编辑文本元素'"



editmodalform "user_interface/modal/edit_text" append label
editlabel "user_interface/modal/edit_text" 0 label "return '您正在编辑模态表单中的文本元素。'"

editmodalform "user_interface/modal/edit_text" append input
editinput "user_interface/modal/edit_text" 1 text "return '请输入要设置的文本内容'"
editinput "user_interface/modal/edit_text" 1 placeholder "return '我叫 $@s$ 且我有 #@s#金币# 个金币'"
editinput "user_interface/modal/edit_text" 1 tooltip "return '§b$选择器$§r 表示实体名 (如“§e$@s$§r”)。\\n§b#目标#分数#§r 表示分数 (如“§e#@s#金币#§r”)。\\n§b$$§r 表示 §e$§r。\\n§b##§r 表示 §e#§r。\\n§b\\\\n§r 表示换行。'"



customform save "user_interface/modal/edit_text"