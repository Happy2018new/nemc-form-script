# 目录
- [目录](#目录)
- [前情提要](#前情提要)
- [指令概览](#指令概览)
- [侦听游戏事件](#侦听游戏事件)
  - [语法](#语法)
  - [备注一](#备注一)
  - [备注二](#备注二)
  - [备注三](#备注三)
  - [备注四](#备注四)
  - [备注五](#备注五)
  - [示例](#示例)
  - [效果（示例）](#效果示例)
  - [补充](#补充)
- [销毁事件函数](#销毁事件函数)
  - [语法](#语法-1)
  - [示例](#示例-1)
- [列出事件函数](#列出事件函数)
  - [语法](#语法-2)
  - [示例一](#示例一)
  - [效果一（示例一）](#效果一示例一)
  - [示例二](#示例二)
  - [效果二（示例二）](#效果二示例二)
- [查询事件函数](#查询事件函数)
  - [语法](#语法-3)
  - [示例](#示例-2)
  - [效果（示例）](#效果示例-1)





# 前情提要
要想高效的掌握和理解游戏事件的侦听和处理，您需要了解如何在本模组中编写代码。<br/>
这意味着如果您还没有掌握这部分的先验知识，则您最好先进行一个初步的了解。<br/>
您可以通过参看 [自述 § 编程语法](../../../README.md#编程语法) 章节来了解关于编写代码的详细细节。





# 指令概览
```mcfunction
systemevent destroy <funcName: string>
systemevent list [eventName: string]
systemevent listen <eventName: string> <funcName: string> <code: string> [onCodeError: string]
systemevent query <funcName: string>
```





# 侦听游戏事件
## 语法
侦听游戏事件。
```mcfunction
systemevent listen <eventName: string> <funcName: string> <code: string> [onCodeError: string]
```

| 参数                  | 数据类型 | 备注 | 解释                                                 |
| --------------------- | -------- | ---- | ---------------------------------------------------- |
| <eventName: string>   | 字符串   | 必填 | 要侦听的游戏事件的名称                               |
| <funcName: string>    | 字符串   | 必填 | 在侦听到目标事件时，所执行的事件函数（的名字）       |
| <code: string>        | 字符串   | 必填 | 在侦听到目标事件时，所执行的事件函数（的代码）       |
| [onCodeError: string] | 字符串   | 选填 | 当给出的代码执行出错时，要执行的代码（用于错误处理） |



## 备注一
不同于**自定义函数**可以通过命令来显式定义命令执行上下文，由于游戏事件侦听没有这一机制，<br/>
因此您必须在 `<code: string>` 和 `[onCodeError: string]` 中手动设置命令执行上下文。

我们提供了一些内建函数，这使得您可以手动设置命令执行上下文。
```python
command.set_executor(executor: str) -> bool
command.set_position(posx: float, posy: float, posz: float) -> bool
command.set_dimension(dim_id: int) -> bool
command.fast_set(selector_or_entity_id: str, is_selector: bool = True) -> bool
```

例如，将命令执行环境切换为 `@a[r=3,c=1]` 所指示的玩家（您必须确保提供的目标选择器所指示的实体只有 1 个）。
```python
_ = {func, command.fast_set('@a[r=3,c=1]')}
```

或者，将命令执行环境切换为实体唯一 ID 为 -2018 的实体。
```python
_ = {func, command.fast_set('-2018', False)}
```

或者，指定命令执行者为实体 ID 为 -666 的实体，且命令执行点是 (2333, 0, 201.8)，同时命令执行维度为 dm4 维度。
```python
_ = {func, command.set_executor('-666')}
_ = {func, command.set_position(2333, 0, 201.8)}
_ = {func, command.set_dimension(4)}
```

您目前只能设置命令执行上下文中的命令执行者、命令执行点和命令执行维度。<br/>
对于其他可能的所有上下文，例如命令执行朝向，无法传递且也无法设置。



## 备注二
您应该注意到了内建函数 `command.set_dimension` 需要提供数字的维度 ID。<br/>
下方则是原版所有已存在维度与这些维度所对应 ID 的关系表。

| 维度名称 | 维度英文 ID | 维度数字 ID |
| -------- | ----------- | ----------- |
| 主世界   | overworld   | 0           |
| 下界     | nether      | 1           |
| 末地     | the_end     | 2           |
| dm3      | dm3         | 3           |
| dm4      | dm4         | 4           |
| dm5      | dm5         | 5           |
| dm6      | dm6         | 6           |
| dm7      | dm7         | 7           |
| dm8      | dm8         | 8           |
| dm9      | dm9         | 9           |
| dm10     | dm10        | 10          |
| dm11     | dm11        | 11          |
| dm12     | dm12        | 12          |
| dm13     | dm13        | 13          |
| dm14     | dm14        | 14          |
| dm15     | dm15        | 15          |
| dm16     | dm16        | 16          |
| dm17     | dm17        | 17          |
| dm18     | dm18        | 18          |
| dm19     | dm19        | 19          |
| dm20     | dm20        | 20          |



## 备注三
下面列出的内建函数允许您动态的获取当前的命令执行上下文。
```python
command.get_executor() -> str
command.get_position() -> ptr@tuple[float, float, float]
command.get_dimension() -> int
command.dimension_name() -> str
```

例如，下面的代码可以获取到当前的命令执行上下文，并将它通过 `say` 命令输出到聊天栏。
```python
entity_id = {func, command.get_executor()}
pos_ptr = {func, command.get_position()}
dim_id = {func, command.get_dimension()}
dim_name = {func, command.dimension_name()}

posx = {func, tuple.get(pos_ptr, 0)}
posy = {func, tuple.get(pos_ptr, 1)}
posz = {func, tuple.get(pos_ptr, 2)}

result = '命令执行者: ' + str(entity_id) + {func, strings.chr(10)}
result = result + '命令执行点: (' + str(posx) + ', ' + str(posy) + ', ' + str(posz) + ')' + {func, strings.chr(10)}
result = result + '命令执行维度的数字 ID: ' + str(dim_id) + {func, strings.chr(10)}
result = result + '命令执行维度的英文 ID: ' + dim_name
return {command, 'say ' + result}
```



## 备注四
为了允许您最大限度的处理游戏事件，您被允许直接侦听最底层的游戏事件（仅服务端事件）。<br/>
您可以通过 [ModAPI § 事件 § 事件索引表](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%BA%8B%E4%BB%B6%E7%B4%A2%E5%BC%95%E8%A1%A8.html) 查看最底层已支持的所有服务端处的游戏事件。



## 备注五
您可以让多个事件函数侦听在同一个事件下。但在一般情况下，您最好不要修改 `args` 参数所指示的映射。

由于所有侦听在同一事件下的事件函数都会共享相同的 `args` 参数，<br/>
因此当某一个事件函数修改 `args` 后，侦听在同一事件下的，<br/>
那些剩余的未被执行的事件函数，将会在未来在被执行时观察到这一更改。

然而，我们不保证侦听在同一个事件下的事件函数总是按顺序执行，<br/>
这意味着您在设计系统时应假定所有事件函数的执行顺序是随机的。

特别地，通过使用下方的代码可以阻止同一事件下，剩余未被执行的事件函数被执行。<br/>
当然，如果 [ModAPI § 事件 § 事件索引表](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%BA%8B%E4%BB%B6%E7%B4%A2%E5%BC%95%E8%A1%A8.html) 对此有特别说明，则该代码还能撤销该事件的发生。

```python
_ = {func, maps.set(args, 'cancel', True)}
```



## 示例
我们将根据 [ModAPI § 事件 § 世界 § ServerChatEvent](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html#serverchatevent) 来制作一个简单的 `VIP, MVP, MVP+` 修饰器。

当玩家具有标签 `vip` 时，其发送的聊天信息的昵称前面将会出现 `§f[§aVIP§f]`；<br/>
当玩家具有标签 `vip_plus` 时，其发送的聊天信息的昵称前面将会出现 `§f[§bVIP§e+§f]`；<br/>
当玩家具有标签 `mvp` 时，其发送的聊天信息的昵称前面将会出现 `§f[§cMVP§f]`；<br/>
当玩家具有标签 `mvp_plus` 时，其发送的聊天信息的昵称前面将会出现 `§f[§dMVP§e+§f]`。

```mcfunction
systemevent listen ServerChatEvent add_vip_chat_prefix

"
user_name = {func, maps.get(args, 'username')}
player_id = {func, maps.get(args, 'playerId')}

if {func, object.deref({func, entity.EntityHasTag(player_id, 'mvp_plus')})}:
  user_name = '§f[§dMVP§e+§f] ' + user_name
elif {func, object.deref({func, entity.EntityHasTag(player_id, 'mvp')})}:
  user_name = '§f[§cMVP§f] ' + user_name
elif {func, object.deref({func, entity.EntityHasTag(player_id, 'vip_plus')})}:
  user_name = '§f[§bVIP§e+§f] ' + user_name
elif {func, object.deref({func, entity.EntityHasTag(player_id, 'vip')})}:
  user_name = '§f[§aVIP§f] ' + user_name
fi

return {func, maps.set(args, 'username', user_name)}
"
```



## 效果（示例）
<img width="582" height="394" alt="Image" src="../../images/system_event_listen.png" />



## 补充
下面的指令和[示例](#示例)中的具有相同的效果。
```mcfunction
systemevent listen ServerChatEvent add_vip_chat_prefix

"
user_name = {func, maps.get(args, 'username')}
player_id = {func, maps.get(args, 'playerId')}

mapping = {func, maps.new(True, 'mvp_plus', '§f[§dMVP§e+§f] ', 'mvp', '§f[§cMVP§f] ', 'vip_plus', '§f[§bVIP§e+§f] ', 'vip', '§f[§aVIP§f] ')}
keys = {func, maps.keys(mapping)}

for i, {func, slices.length(keys)}:
  key = {func, slices.get(keys, i)}
  ptr = {func, entity.EntityHasTag(player_id, key)}
  if {func, object.deref(ptr)}:
    prefix = {func, maps.get(mapping, key)}
    user_name = prefix + user_name
    break
  fi
rof

return {func, maps.set(args, 'username', user_name)}
"
```





# 销毁事件函数
## 语法
销毁名为 `<funcName: string>` 的事件函数。
```mcfunction
systemevent destroy <funcName: string>
```



## 示例
```mcfunction
# 销毁名为 add_vip_chat_prefix 的事件函数
systemevent destroy add_vip_chat_prefix

# 销毁名为 AaBbCc 的事件函数
systemevent destroy AaBbCc

# 销毁名为 LOvE 的事件函数
systemevent destroy "LOvE"
```





# 列出事件函数
## 语法
列出所有已添加（已注册）的事件函数，或查询侦听在游戏事件 `[eventName: string]` 下的所有事件函数。
```mcfunction
systemevent list [eventName: string]
```


## 示例一
列出所有已添加（已注册）的事件函数。
```mcfunction
systemevent list
```



## 效果一（示例一）
```
当前侦听了 2 个事件:
  - 事件 CommandEvent (1 个)
    - funcP
  - 事件 ServerChatEvent (2 个)
    - aBBc
    - add_vip_chat_prefix
```



## 示例二
列出侦听在游戏事件 `ServerChatEvent` 下的所有事件函数。
```mcfunction
systemevent list ServerChatEvent
```



## 效果二（示例二）
```
共有 2 个事件函数侦听了目标事件
  - aBBc
  - add_vip_chat_prefix
```





# 查询事件函数
## 语法
查询事件函数 `<funcName: string>` 侦听在哪个游戏事件下。
```mcfunction
systemevent query <funcName: string>
```



## 示例
查询事件函数 `add_vip_chat_prefix` 侦听在哪个游戏事件下。
```mcfunction
systemevent query add_vip_chat_prefix
```



## 效果（示例）
```
名为 "add_vip_chat_prefix" 的事件函数侦听在事件 "ServerChatEvent" 上
```