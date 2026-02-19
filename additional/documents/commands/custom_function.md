# 目录
- [目录](#目录)
- [前情提要](#前情提要)
- [指令概览](#指令概览)
- [添加自定义函数](#添加自定义函数)
  - [语法](#语法)
  - [备注](#备注)
  - [示例](#示例)
- [调用（执行）自定义函数](#调用执行自定义函数)
  - [语法](#语法-1)
  - [解释](#解释)
  - [示例](#示例-1)
  - [补充一](#补充一)
  - [补充二](#补充二)
- [列出自定义函数](#列出自定义函数)
  - [语法](#语法-2)
  - [示例一](#示例一)
  - [效果一（示例一）](#效果一示例一)
  - [示例二](#示例二)
  - [效果二（示例二）](#效果二示例二)
- [移除自定义函数](#移除自定义函数)
  - [语法](#语法-3)
  - [示例](#示例-2)





# 前情提要
要想高效的掌握和理解自定义函数的用法，您需要了解如何在本模组中编写代码。<br/>
这意味着如果您还没有掌握这部分的先验知识，则您最好先进行一个初步的了解。<br/>
您可以通过参看 [自述 § 编程语法](../../../README.md#编程语法) 章节来了解关于编写代码的详细细节。





# 指令概览
```mcfunction
customfunction add <name: string> <code: string>
customfunction call <executor: target> <position: x y z> <name: string>
customfunction list [name: string]
customfunction remove <name: string>
```





# 添加自定义函数
## 语法
添加名为 `<name: string>` 的自定义函数，并指定该函数的代码为 `<code: string>`。
```mcfunction
customfunction add <name: string> <code: string>
```



## 备注
`<code: string>` 所指示的代码必须在执行完毕前返回值。<br/>
这是因为我们允许自定义函数之间可以内部地互相调用对方，<br/>
因此您必须显式地在代码中返回值。

关于如何在自定义函数内部调用其他自定义函数，<br/>
请参看 [调用自定义函数 § 补充一](#补充一) 章节中的内容。

如果您不知道编写的代码的方法，可以参看 [自述 § 编程语法](../../../README.md#编程语法) 。



## 示例
```mcfunction
# 添加自定义函数 func1，该函数返回 True
customfunction add func1 "return True"

# 添加自定义函数 func2，该函数执行命令 say Hello! 并返回命令是否成功
customfunction add func2 "return {command, 'say Hello!"} > 0"

# 添加自定义函数 shallow，该函数返回 0+1+2+...+99 的结果
customfunction add shallow "total = 0
for i, 100:
  total = total + i
rof
return total"
```





# 调用（执行）自定义函数
## 语法
以 `<executor: target>` 作为命令执行者，`<position: x y z>` 作为命令执行点，<br/>
在不改变原有命令执行维度的情况下，调用（执行）名为 `<name: string>` 的自定义函数。

```mcfunction
customfunction call <executor: target> <position: x y z> <name: string>
```



## 解释
由于自定义函数的本质是一段代码，而这段代码内部允许执行命令，或使用与命令执行有关的功能，<br/>
因此，你需要通过 `<executor: target>` 和 `<position: x y z>` 来显式定义命令执行者和命令执行点。

这意味着自定义函数中任何需要执行指令（或与执行指令相关的功能）的代码都将使用提供的命令执行上下文来完成。<br/>
应注意的是，命令执行维度将会自动继承，这意味着命令执行维度将是该 `customfunction` 执行时所使用的维度。<br/>
这也基本意味着自定义函数的命令执行维度与 `<executor: target>` 所在的维度没有任何显式的关系。

另外还有一些事项值得您关注。
- 上文未列举的，其他的所有命令执行上下文都将丢失，例如命令执行朝向等
- 命令执行者至多设置一个，设置多个命令执行者将导致命令执行失败
- `<executor: target>` 和 `<position: x y z>` 之间没有显式联系



## 示例
```mcfunction
# 以 @e[tag=abc,c=1] 作为命令执行者，以 ~ ~ ~ 指示的位置作为命令执行点，执行 main 函数。
# 需要特别注意的是，main 函数的命令执行维度是该执行该 customfunction 时所使用的维度。
customfunction call @e[tag=abc,c=1] ~ ~ ~ main

# 以 @e[tag=abc,c=1] 的各项参数作为命令执行上下文，执行 main 函数。
# 由于此处使用了 execute 命令，因此 main 函数的命令执行维度就是 @e[tag=abc,c=1] 所处的维度。
execute as @e[tag=abc,c=1] at @s run customfunction call @s ~ ~ ~ main
```



## 补充一
尽管通过指令无法显式定义要传入函数的参数，并且实际上也无法通过指令来传递参数，<br/>
然而，我们允许自定义函数之间在内部传递参数，即您可以通过下面的方式来传递参数。

```mcfunction
# 添加自定义函数 math_compute
customfunction add math_compute "arg1 = {func, tuple.get(args, 0)}
arg2 = {func, tuple.get(args, 1)}
arg4 = {func, tuple.get(args, 3)}
len = {func, tuple.length(args)}
return {command, 'say arg1=' + str(arg1) + ', arg2=' + str(arg2) + ', arg4=' + str(arg4) + ', len=' + str(len)}"

# 添加自定义函数 main
customfunction add main "result = {func, function.call('math_compute', 'a_a_a', 23, 'B-B-B', 'PLACEHOLDER')}
return {command, 'say result=' + str(result)}"

# 执行自定义函数 main
customfunction call @p ~ ~ ~ main
```

在上面的例子中，自定义函数 `main` 通过内建函数 `function.call` 调用了自定义函数 `math_compute`。<br/>
同时，在这个过程中，`main` 向 `math_compute` 传入了参数 `'a_a_a'`、`'BBB'`、`23` 和 `'PLACEHOLDER'`。

如果准确无误，在依次运行上面的命令后，您将在聊天栏发现类似于下面的输出。
```
[Eternal] arg1=a_a_a, arg2=23, arg4=PLACEHOLDER, len=4
[Eternal] result=1
```



## 补充二
在[补充一](#补充一)的基础上，您需要额外注意的一种情况是未传入任何参数的情况。<br/>
在这种情况下，变量 `args` 将不会存在，这意味着诸如下面的代码将会报错。

```mcfunction
# 添加自定义函数 tester1
customfunction add tester1 "n = {func, tuple.get(args, 0)}
return {command, 'say n=' + str(n)}"
"

# 添加自定义函数 tester2
customfunction add tester2 "result = {func, function.call('tester1')}
return {command, 'say result=' + str(result)}"

# 执行自定义函数 tester2
customfunction call @p ~ ~ ~ tester2
```

这意味着 `customfunction call @p ~ ~ ~ tester2` 将执行失败，<br/>
这也意味着您在执行该命令后将会得到下面的命令失败提示。

```
Runtime Error.

- Error -
  Variable "args" used before assignment

- Code -
  n = {func, tuple.get(args, 0)}

- Context -
  In function "tester1"
```

这种例外是特别设计的。这意味着您应该提前通过某种方式约定函数的调用方法。<br/>
具体来说，在您设计自定义函数时，应确保传入该函数的参数数量不会变化，并且传入该函数的各个参数的数据类型也不会发生变化。





# 列出自定义函数
## 语法
列出已添加（已注册）的所有自定义函数，或只查询 `[name: string]` 所指示的自定义函数是否存在。
```mcfunction
customfunction list [name: string]
```


## 示例一
列出已注册的所有自定义函数。
```mcfunction
customfunction list
```



## 效果一（示例一）
```
当前已注册了 3 个自定义函数:
  - func1
  - tester1
  - tester2
```



## 示例二
查询自定义函数 tester1 是否存在。
```mcfunction
customfunction list tester1
```



## 效果二（示例二）
```
已找到名为 "tester1" 的自定义函数
```





# 移除自定义函数
## 语法
移除名为 `<name: string>` 的自定义函数。
```mcfunction
customfunction remove <name: string>
```



## 示例
```mcfunction
# 移除名为 abc 的自定义函数
customfunction remove abc

# 移除名为 233233666 的自定义函数
customfunction remove "233233666"
```