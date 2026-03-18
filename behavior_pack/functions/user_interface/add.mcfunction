customform remove "user_interface/add"
customform add "user_interface/add" modal
editmodalform "user_interface/add" title "return '添加表单'"



editmodalform "user_interface/add" append label
editlabel "user_interface/add" 0 label "return '您将添加一个新的表单。'"

editmodalform "user_interface/add" append input
editinput "user_interface/add" 1 text "return '表单名称'"
editinput "user_interface/add" 1 placeholder "return '在此处输入表单名称'"
editinput "user_interface/add" 1 tooltip "return '新创建的表单名称不能与已有表单重复。'"



customform save "user_interface/add"