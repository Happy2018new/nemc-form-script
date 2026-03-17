# 目录
- [目录](#目录)
- [指令概览](#指令概览)
  - [编辑长表单](#编辑长表单)
  - [编辑长表单中的按钮](#编辑长表单中的按钮)
- [编辑长表单](#编辑长表单-1)
  - [添加元素](#添加元素)
    - [语法](#语法)
    - [备注](#备注)
    - [示例一](#示例一)
    - [示例二](#示例二)
    - [效果（示例二）](#效果示例二)
  - [设置内容文本](#设置内容文本)
    - [语法](#语法-1)
    - [备注](#备注-1)
    - [示例](#示例)
  - [插入元素](#插入元素)
    - [语法](#语法-2)
  - [备注一](#备注一)
    - [备注二](#备注二)
    - [补充](#补充)
    - [示例](#示例-1)
  - [列出元素](#列出元素)
    - [语法](#语法-3)
    - [示例](#示例-2)
    - [效果（示例）](#效果示例)
  - [弹出元素](#弹出元素)
    - [语法](#语法-4)
    - [备注](#备注-2)
    - [示例](#示例-3)
  - [截断元素](#截断元素)
    - [语法](#语法-5)
    - [备注](#备注-3)
    - [补充](#补充-1)
    - [示例](#示例-4)
  - [设置标题文本](#设置标题文本)
    - [语法](#语法-6)
    - [示例](#示例-5)
- [编辑长表单中的按钮](#编辑长表单中的按钮-1)
  - [设置图标](#设置图标)
    - [语法](#语法-7)
    - [备注一](#备注一-1)
    - [备注二](#备注二-1)
    - [补充](#补充-2)
    - [示例](#示例-6)
    - [效果（示例）](#效果示例-1)
  - [设置文字](#设置文字)
    - [语法](#语法-8)
    - [补充](#补充-3)
    - [示例](#示例-7)
    - [效果（示例）](#效果示例-2)







# 指令概览
## 编辑长表单
```mcfunction
editlongform <formName: string> append [button|label|header|divider]
editlongform <formName: string> content <contentCode: string>
editlongform <formName: string> insert <index: int> [button|label|header|divider]
editlongform <formName: string> list
editlongform <formName: string> pop left|right
editlongform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
editlongform <formName: string> title <titleCode: string>
```





## 编辑长表单中的按钮
```mcfunction
editbutton <formName: string> <index: int> icon [textureCode: string]
editbutton <formName: string> <index: int> text <textCode: string>
```







# 编辑长表单
## 添加元素
### 语法
向长表单 `<formName: string>` 添加（追加）一个元素。
```mcfunction
editlongform <formName: string> append [button|label|header|divider]
```

| 元素 ID | 元素名称 | 图例                                                                                   |
| ------- | -------- | -------------------------------------------------------------------------------------- |
| button  | 按钮     | <img width="416" height="81" alt="Image" src="../../images/sample_button.png" />       |
| label   | 普通文本 | <img width="416" height="42" alt="Image" src="../../images/sample_long_label.png" />   |
| header  | 大字文本 | <img width="416" height="65" alt="Image" src="../../images/sample_long_header.png" />  |
| divider | 分割线   | <img width="416" height="18" alt="Image" src="../../images/sample_long_divider.png" /> |



### 备注
通过该方式添加的元素后，您需要通过其他指令来进一步编辑它们。<br/>
这意味着通过该方式添加的元素在一开始都保持下面列出的默认状态。

- 按钮
  - 按钮上无文本
  - 按钮上无图标
- 普通文本
  - 空文本
- 大字文本
  - 空文本

由于分割线在添加后无需进一步修改，因此它将始终保持在相同的状态。



### 示例一
```mcfunction
# 向长表单 Happy 添加一个按钮
editlongform Happy append button

# 向长表单 abc 添加一个普通文本
editlongform abc append label

# 向长表单 hello 添加一个大字文本
editlongform hello append header

# 向长表单 123 添加一个分割线
editlongform "123" append divider
```



### 示例二
```mcfunction
# 添加名为 longtest 的长表单
customform add longtest long

# 将该长表单的标题文本设为固定的 ABC
editlongform longtest title "return 'ABC'"

# 将该长表单的内容文本设为固定的 DEF
editlongform longtest content "return 'DEF'"

# 向该长表单添加一个按钮
editlongform longtest append button
# 将该按钮的显示文本设置为 按钮一
editbutton longtest 0 text "return '按钮一'"

# 向该长表单添加一个普通文本
editlongform longtest append label
# 将该普通文本所显示的内容设置为固定的 牛牛牛
editlabel longtest 1 label "return '牛牛牛'"

# 向该长表单添加一个分割线
editlongform longtest append divider

# 向该长表单添加一个大字文本
editlongform longtest append header
# 将该普通文本所显示的内容设置为固定的 献给机械の花束
editlabel longtest 3 header "return '献给机械の花束'"

# 向该长表单添加一个按钮
editlongform longtest append button

# 向最近的玩家展示（打开）该长表单（在命令方块中执行）
customform show @p ~ ~ ~ @p longtest
```



### 效果（示例二）
<img width="449" height="398" alt="Image" src="../../images/edit_long_form_append.png" />





## 设置内容文本
### 语法
设置长表单要显示的内容文本。
```mcfunction
editlongform <formName: string> content <contentCode: string>
```

| 参数                  | 数据类型 | 备注 | 解释                   |
| --------------------- | -------- | ---- | ---------------------- |
| <formName: string>    | 字符串   | 必填 | 被编辑的长表单的名字   |
| <contentCode: string> | 字符串   | 必填 | 用于生成内容文本的代码 |

<img width="449" height="400" alt="Image" src="../../images/edit_long_form_content.png" />



### 备注
如果您不知道编写的代码的方法，可以参看 [自述 § 编程语法](../../../README.md#编程语法) 。



### 示例
设置长表单 `i_am_a_boy` 的内容文本，并且内容文本总是固定的 `你好`。
```mcfunction
editlongform i_am_a_boy content "return '你好'"
```





## 插入元素
### 语法
在长表单 `<formName: string>` 的索引 `<index: int>` 处插入一个元素。
```mcfunction
editlongform <formName: string> insert <index: int> [button|label|header|divider]
```



## 备注一
插入元素的行为与上方的添加元素的行为保持一致，<br/>
它们的唯一区别在于插入元素可以指定插入的位置。



### 备注二
要在第一个元素前插入一个元素，索引值应使用 0。<br/>
要在第一个元素后插入一个元素，索引值应使用 1。

要在第 `i` 个元素前插入一个元素，索引值应使用 `i-1`。<br/>
要在第 `i` 个元素后插入一个元素，索引值应使用 `i`。

如果一个元素的索引是 `i`，则要在它之前插入一个元素，应使用 `i`。<br/>
如果一个元素的索引是 `i`，则要在它之后插入一个元素，应使用 `i+1`。



### 补充
第 1 个元素的索引值是 0。<br/>
第 2 个元素的索引值是 1。<br/>
第 3 个元素的索引值是 2。<br/>
...<br/>
第 n 个元素的索引值是 n-1。



### 示例
```mcfunction
# 在 bbc 长表单的第三个元素前插入一个 普通文本 元素
editlongform bbc insert 2 label

# 在 bbc 长表单的第三个元素后插入一个 按钮 元素
editlongform bbc insert 3 button

# 在 bbc 长表单的第一个元素前插入一个 大字文本 元素
editlongform bbc insert 0 header

# 在 bbc 长表单的第一个元素后插入一个 分割线 元素
editlongform bbc insert 1 divider
```





## 列出元素
### 语法
列出长表单 `<formName: string>` 中的所有元素。
```mcfunction
editlongform <formName: string> list
```



### 示例
```mcfunction
# 列出长表单 a 中所有元素的情况
editlongform a list
```



### 效果（示例）
```
长表单 "a" 目前已存在 5 个元素:
  - 按钮 (无图标)
  - 普通文本
  - 分割线
  - 大字文本
  - 按钮 (使用材质贴图)
```





## 弹出元素
### 语法
弹出（移除）长表单 `<formName: string>` 中的第一个元素或最后一个元素。
```mcfunction
editlongform <formName: string> pop left|right
```



### 备注
枚举值 `left|right` 的含义如下。
- left: 弹出（移除）第一个元素
- right: 弹出（移除）最后一个元素



### 示例
```mcfunction
# 移除长表单 rta 中的最后一个元素
editlongform rta pop right

# 移除长表单 rta 中的第一个元素
editlongform rta pop left
```





## 截断元素
### 语法
只保留或只丢弃模态表单中的一部分元素。
```mcfunction
editlongform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
```


| 参数               | 数据类型 | 备注 | 解释                 |
| ------------------ | -------- | ---- | -------------------- |
| <formName: string> | 字符串   | 必填 | 被编辑的长表单的名字 |
| keep\|discard      | 枚举值   | 必填 | 操作类型             |
| <startIndex: int>  | 整数     | 必填 | 涉及的元素的起始索引 |
| <endIndex: int>    | 整数     | 必填 | 涉及的元素的结束索引 |



### 备注
枚举值 `keep|discard` 的含义如下。
- keep: 只保留长表单中的一部分元素
- discard: 只丢弃长表单中的一部分元素


要只保留（丢弃）第 1、2、3 个元素：
- `<startIndex: int>` 填 `0`
- `<endIndex: int>` 填 `3`


要只保留（只丢弃）第 `a、a+1、a+2、...、a+n` 个元素：
- `<startIndex: int>` 填 `a-1`
- `<endIndex: int>` 填 `a+n`

要只保留（只丢弃）索引为 `b、b+1、b+2、...、b+n` 的元素：
- `<startIndex: int>` 填 `b`
- `<endIndex: int>` 填 `b+n+1`

要只保留（只丢弃）索引为 `c` 以及它后面的元素，并且总共只选择 `n` 个：
- `<startIndex: int>` 填 `c`
- `<endIndex: int>` 填 `c+n`



### 补充
第 1 个元素的索引值是 0。<br/>
第 2 个元素的索引值是 1。<br/>
第 3 个元素的索引值是 2。<br/>
...<br/>
第 n 个元素的索引值是 n-1。



### 示例
```mcfunction
# 只保留长表单 rtx 中的第三、四、五、六个元素，剩余的丢弃
editlongform rtx sub keep 2 6

# 只移除长表单 rtx 中的第三、四、五、六个元素，保留剩余的
editlongform rtx sub discard 2 6
```





## 设置标题文本
### 语法
设置长表单要显示的标题文本。
```mcfunction
editlongform <formName: string> title <titleCode: string>
```

| 参数                | 数据类型 | 备注 | 解释                   |
| ------------------- | -------- | ---- | ---------------------- |
| <formName: string>  | 字符串   | 必填 | 被编辑的长表单的名字   |
| <titleCode: string> | 字符串   | 必填 | 用于生成标题文本的代码 |

<img width="449" height="400" alt="Image" src="../../images/edit_long_form_title.png" />



### 示例
设置长表单 `bds` 的标题文本，<br/>
并且内容文本是显示表单时设置的命令执行者的名字。

```mcfunction
editlongform bds title "return {selector, '@s'}"
```







# 编辑长表单中的按钮
## 设置图标
### 语法
设置指定长表单中指定按钮的图标。
```mcfunction
editbutton <formName: string> <index: int> icon [textureCode: string]
```

| 参数                  | 数据类型 | 备注 | 解释                             |
| --------------------- | -------- | ---- | -------------------------------- |
| <formName: string>    | 字符串   | 必填 | 被编辑的长表单的名字             |
| <index: int>          | 整数     | 必填 | 被编辑的按钮元素在长表单中的索引 |
| [textureCode: string] | 字符串   | 选填 | 用于生成图标的代码               |



### 备注一
`[textureCode: string]` 所使用的代码应返回一个字符串。<br/>
这个字符串指向了相应按钮所使用的图标在 MC 中的材质贴图路径。<br/>
当然，您可以不填写这个字符串，从而将该按钮设置为没有图标。



### 备注二
如果您不知道编写的代码的方法，可以参看 [自述 § 编程语法](../../../README.md#编程语法) 。



### 补充
第 1 个元素的索引值是 0。<br/>
第 2 个元素的索引值是 1。<br/>
第 3 个元素的索引值是 2。<br/>
...<br/>
第 n 个元素的索引值是 n-1。



### 示例
```mcfunction
# 将长表单 abc 中第二个元素（按钮）的贴图设置为一幅画作
editbutton abc 1 icon "return 'textures/painting/baroque'"
```



### 效果（示例）
<img width="449" height="399" alt="Image" src="../../images/edit_button_icon.png" />





## 设置文字
### 语法
设置指定长表单中指定按钮的文字。
```mcfunction
editbutton <formName: string> <index: int> text <textCode: string>
```

| 参数               | 数据类型 | 备注 | 解释                             |
| ------------------ | -------- | ---- | -------------------------------- |
| <formName: string> | 字符串   | 必填 | 被编辑的长表单的名字             |
| <index: int>       | 整数     | 必填 | 被编辑的按钮元素在长表单中的索引 |



### 补充
第 1 个元素的索引值是 0。<br/>
第 2 个元素的索引值是 1。<br/>
第 3 个元素的索引值是 2。<br/>
...<br/>
第 n 个元素的索引值是 n-1。



### 示例 
```mcfunction
# 将长表单 abc 中索引为 2 的元素（按钮）的文字设置为固定的 aabbcc
editbutton abc 2 text "return 'aabbcc'"
```



### 效果（示例）
<img width="449" height="399" alt="Image" src="../../images/edit_button_text.png" />