customform remove "user_interface/modal/insert"
customform add "user_interface/modal/insert" long
editlongform "user_interface/modal/insert" title "return '插入元素'"
editlongform "user_interface/modal/insert" content "return '请从现有的元素中选择一个元素。\\n我们将在它的前面插入一个元素。'"

editlongform "user_interface/modal/insert" append button
editbutton "user_interface/modal/insert" 0 text "return '返回上一级'"

customform save "user_interface/modal/insert"