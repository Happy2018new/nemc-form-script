# 目录
- [目录](#目录)
- [指令概览](#指令概览)
- [编辑确定按钮](#编辑确定按钮)
  - [语法](#语法)
  - [备注](#备注)
  - [示例](#示例)
- [编辑取消按钮](#编辑取消按钮)
  - [语法](#语法-1)
  - [备注](#备注-1)
  - [示例](#示例-1)
- [编辑内容文本](#编辑内容文本)
  - [语法](#语法-2)
  - [备注](#备注-2)
  - [示例](#示例-2)
  - [效果（示例）](#效果示例)
- [编辑标题文本](#编辑标题文本)
  - [语法](#语法-3)
  - [备注](#备注-3)
  - [示例](#示例-3)
  - [效果（示例）](#效果示例-1)





# 指令概览
```mcfunction
editpopupform <formName: string> button1 <firstButtonCode: string>
editpopupform <formName: string> button2 <secondButtonCode: string>
editpopupform <formName: string> content <contentCode: string>
editpopupform <formName: string> title <titleCode: string>
```





# 编辑确定按钮
## 语法
编辑信息表单中代表“确定”按钮所显示的文本。
```mcfunction
editpopupform <formName: string> button1 <firstButtonCode: string>
```

| 参数                      | 数据类型 | 备注 | 解释                   |
| ------------------------- | -------- | ---- | ---------------------- |
| <formName: string>        | 字符串   | 必填 | 被编辑的信息表单的名字 |
| <firstButtonCode: string> | 字符串   | 必填 | 用于生成文本的代码     |

<img width="428" height="350" alt="Image" src="../../images/edit_popup_form_button1.png" />



## 备注
如果您不知道编写的代码的方法，可以参看 [自述 § 编程语法](../../../README.md#编程语法) 。



## 示例
```mcfunction
# 将信息表单 flowers 的确定按钮设置为固定的“|确定|”
editpopupform flowers button1 "return '|确定|'"
```





# 编辑取消按钮
## 语法
编辑信息表单中代表“取消”按钮所显示的文本。
```mcfunction
editpopupform <formName: string> button2 <secondButtonCode: string>
```

| 参数                       | 数据类型 | 备注 | 解释                   |
| -------------------------- | -------- | ---- | ---------------------- |
| <formName: string>         | 字符串   | 必填 | 被编辑的信息表单的名字 |
| <secondButtonCode: string> | 字符串   | 必填 | 用于生成文本的代码     |

<img width="428" height="350" alt="Image" src="../../images/edit_popup_form_button2.png" />



## 备注
如果您不知道编写的代码的方法，可以参看 [自述 § 编程语法](../../../README.md#编程语法) 。



## 示例
```mcfunction
# 将信息表单 flowers 的取消按钮设置为固定的“<取消>”
editpopupform flowers button1 "return '<取消>'"
```





# 编辑内容文本
## 语法
编辑信息表单的内容文本。
```mcfunction
editpopupform <formName: string> content <contentCode: string>
```

| 参数                  | 数据类型 | 备注 | 解释                   |
| --------------------- | -------- | ---- | ---------------------- |
| <formName: string>    | 字符串   | 必填 | 被编辑的信息表单的名字 |
| <contentCode: string> | 字符串   | 必填 | 用于生成内容文本的代码 |



## 备注
如果您不知道编写的代码的方法，可以参看 [自述 § 编程语法](../../../README.md#编程语法) 。



## 示例
```
0
1
2
3
4
5
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
```

将信息表单 flowers 的内容文本设置为上面这个文本。

```mcfunction
editpopupform flowers content "
ret = ''
for i, 25:
    ret = ret + str(i) + '\\n'
rof
return {func, strings.strip(ret)}
"
```



## 效果（示例）
<img width="427" height="350" alt="Image" src="../../images/edit_popup_form_content.png" />





# 编辑标题文本
## 语法
编辑信息表单的标题文本。
```mcfunction
editpopupform <formName: string> title <titleCode: string>
```

| 参数                | 数据类型 | 备注 | 解释                   |
| ------------------- | -------- | ---- | ---------------------- |
| <formName: string>  | 字符串   | 必填 | 被编辑的信息表单的名字 |
| <titleCode: string> | 字符串   | 必填 | 用于生成标题文本的代码 |



## 备注
如果您不知道编写的代码的方法，可以参看 [自述 § 编程语法](../../../README.md#编程语法) 。



## 示例
```mcfunction
# 将信息表单 flowers 的标题文本设置为 5 个 CB
editpopupform flowers title "return 'CB'*5"
```



## 效果（示例）
<img width="428" height="350" alt="Image" src="../../images/edit_popup_form_title.png" />