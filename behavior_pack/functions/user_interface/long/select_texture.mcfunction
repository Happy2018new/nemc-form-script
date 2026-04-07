customform remove "user_interface/long/select_texture"
customform add "user_interface/long/select_texture" modal
editmodalform "user_interface/long/select_texture" title "return '为按钮选择材质贴图'"



editmodalform "user_interface/long/select_texture" append label
editlabel "user_interface/long/select_texture" 0 label "return '搜索材质贴图'"

editmodalform "user_interface/long/select_texture" append input
editinput "user_interface/long/select_texture" 1 text "return '请输入搜索关键词'"
editinput "user_interface/long/select_texture" 1 placeholder "return '物品或方块的英文 (如 apple)'"
editinput "user_interface/long/select_texture" 1 tooltip "return '如果目标物品或方块的材质贴图没有找到，\\n那么您可以尝试只提供其英文 ID 的一部分，\\n例如可以把 §egolden_apple§r 替换为 §egolden§r。'"

editmodalform "user_interface/long/select_texture" append toggle
edittoggle "user_interface/long/select_texture" 2 text "return '直接使用贴图路径'"
edittoggle "user_interface/long/select_texture" 2 tooltip "return '§b小提示§r\\n  §e1.§r 打开此开关后将跳过搜索，于是您输入的内容将视作贴图的路径，然后我们将使用该路径对应之贴图作为按钮的贴图。\\n  §e2.§r 您可以通过将输入框置空并打开此按钮来清空该按钮上的贴图。'"



customform save "user_interface/long/select_texture"