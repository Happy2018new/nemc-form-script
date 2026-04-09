customform remove "user_interface/help"
customform add "user_interface/help" modal
editmodalform "user_interface/help" title "return '帮助'"



editmodalform "user_interface/help" append header
editlabel "user_interface/help" 0 header "return '警告'"
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 1 label "return '编辑器产生的菜单§e只能§r通过编辑器编辑。\\n您§c绝不应§r用指令修改编辑器产生的菜单。'"
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 2 label "return '请确保不会有多个管理员§e编辑同一个菜单§r。\\n如果它发生了，则菜单信息可能会§c严重错乱§r。'"
editmodalform "user_interface/help" append divider

editmodalform "user_interface/help" append header
editlabel "user_interface/help" 4 header "return '打开菜单'"
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 5 label "return '通过指令“execute as §b玩家§r at @s run customform show @s ~ ~ ~ @s §e菜单名字§r”来向名为“§b玩家§r”的玩家打开(显示)名为“§e菜单名字§r”的菜单。'"
editmodalform "user_interface/help" append divider

editmodalform "user_interface/help" append header
editlabel "user_interface/help" 7 header "return '常见问题'"
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 8 label "return 'Q: 我在聊天栏执行打开菜单的指令后，提示指令成功，但实际上菜单没有并没有向我自己打开？\\nA: 这是因为指令执行后，您的聊天栏还没有彻底关闭，于是菜单会因您正忙而视作关闭。'"
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 9 label "return 'Q: 我应该如何避免遇到上面这个问题？\\nA: 总是通过命令方块打开菜单可以避免这个问题。'" 
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 10 label "return 'Q: 什么情况下玩家正忙？\\nA: 当玩家已经打开聊天栏、命令方块等界面，或已经被打开一个表单后，玩家进入正忙状态。'" 
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 11 label "return 'Q: 玩家正忙的意义是什么？\\nA: 例如，如果玩家正在聊天栏打字，这个过程也不会被打断，这便是意义之一！'" 
editmodalform "user_interface/help" append divider

editmodalform "user_interface/help" append header
editlabel "user_interface/help" 13 header "return '关于'"
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 14 label "return 'Author: Eternal Crystal\\nVersion: Stable Release'"
editmodalform "user_interface/help" append label
editlabel "user_interface/help" 15 label "return 'YoRHa, Chapter 24\\nflowers for m[A]chines'"



customform save "user_interface/help"