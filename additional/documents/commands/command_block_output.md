# 目录
- [目录](#目录)
- [概述](#概述)
- [语法](#语法)
- [示例及效果](#示例及效果)
- [备注](#备注)



# 概述
在部分情况下，命令方块中的报错信息可能较长，导致其超出显示范围。<br/>
一个例子是在命令方块执行下面的指令将会得到下方较长的报错信息。

```mcfunction
customfunction add my_func "a = 1
b = 2
c = 3
d = {func, object.ref(True)

if a==1 and b==2 and c==3 and d != 0:
  _ = {command, 'say OK'}
fi

return True"
```

<img width="739" height="425" alt="Image" src="../../images/command_block_output_1.png" />

因此我们需要一种方式可以完整的查看相应的报错信息。<br/>
这种方式便是使用命令 `commandblockoutput` 来进行查看。



# 语法
查看 `<commandBlockPosition: x y z>` 处的命令方块的输出。
```mcfunction
commandblockoutput <commandBlockPosition: x y z>
```



# 示例及效果
以[概述](#概述)中的情形为例，我们可以站在命令方块上执行以下指令。<br/>
然后，您便可以通过打开的表单观察到该命令方块的完整输出。

```mcfunction
commandblockoutput ~ ~-1 ~
```

<img width="450" height="400" alt="Image" src="../../images/command_block_output_2.png" />

这意味着这一行的代码存在错误。
```python
d = {func, object.ref(True)
```

只需要补上右大括号即可。
```python
d = {func, object.ref(True)}
```



# 备注
- 该命令不能用于查看我的世界原版指令的执行日志
- 大多数模组中的命令执行日志应该可以使用该命令查看，但不确保兼容性