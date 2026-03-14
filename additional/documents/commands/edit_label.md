# 目录
- [目录](#目录)
- [指令概览](#指令概览)
- [编辑普通文本](#编辑普通文本)
  - [语法](#语法)
  - [示例一](#示例一)
  - [示例二](#示例二)
  - [效果（示例二）](#效果示例二)
- [编辑大字文本](#编辑大字文本)
  - [语法](#语法-1)
  - [示例一](#示例一-1)
  - [示例二](#示例二-1)
  - [效果（示例二）](#效果示例二-1)





# 指令概览
```mcfunction
editlabel <formName: string> <index: int> header <headerCode: string>
editlabel <formName: string> <index: int> label <labelCode: string>
```





# 编辑普通文本
## 语法
编辑长表单或模态表单中的普通文本元素。
```mcfunction
editlabel <formName: string> <index: int> label <labelCode: string>
```



## 示例一
```mcfunction
# 假定长表单 aaa 中第三个元素是普通文本，
# 并将该普通文本所显示的内容设置为固定的 aobo
editlabel aaa 2 label "return 'aobo'"

# 假定模态表单 242322 中第八个元素是普通文本，
# 并将该普通文本所显示的内容设置为固定的 hhhhc
editlabel "242322" 7 label "return 'hhhhc'"
```



## 示例二
```mcfunction
# 添加名为 ak6 的长表单
customform add ak6 long

# 向该长表单添加一个普通文本
editlongform ak6 append label

# 将该长表单的内容文本设为固定的 aa|bb|cc
editlongform ak6 content "return 'aa|bb|cc'"

# 将该普通文本所显示的内容设置为固定的 233
editlabel ak6 0 label "return '233'"

# 向最近的玩家展示（打开）该长表单（在命令方块中执行）
customform show @p ~ ~ ~ @p ak6
```



## 效果（示例二）
<img width="449" height="398" alt="Image" src="../../images/edit_label_label.png" />





# 编辑大字文本
## 语法
编辑长表单或模态表单中的大字文本元素。
```mcfunction
editlabel <formName: string> <index: int> header <headerCode: string>
```



## 示例一
```mcfunction
# 假定长表单 你好 中第一个元素是大字文本，
# 并将该大字文本所显示的内容设置为固定的 ababac
editlabel 你好 0 header "return 'ababac'"

# 假定模态表单 oaoboc 中第四个元素是大字文本，
# 并将该大字文本所显示的内容设置为固定的 “Bob and Alexis?”
editlabel oaoboc 3 header "return 'Bob and Alexis?'"
```



## 示例二
```mcfunction
# 添加名为 labelheader 的模态表单
customform add labelheader modal

# 向该模态表单添加一个大字文本
editmodalform labelheader append header

# 将该大字文本所显示的内容设置为展示（打开）表单时的月份
editlabel labelheader 0 header "ptr = {func, datetime_datetime.now()}
month = {func, datetime_datetime.month(ptr)}
return '现在的时间是' + str(month) + '月'"

# 向最近的玩家展示（打开）该模态表单（在命令方块中执行）
customform show @p ~ ~ ~ @p labelheader
```



## 效果（示例二）
<img width="449" height="398" alt="Image" src="../../images/edit_label_header.png" />