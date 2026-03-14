# 目录
- [目录](#目录)
- [前情提要](#前情提要)
- [指令概览](#指令概览)
  - [编辑模态表单](#编辑模态表单)
  - [编辑模态表单中的输入框](#编辑模态表单中的输入框)
  - [编辑模态表单中的开关](#编辑模态表单中的开关)
  - [编辑模态表单中的下拉框](#编辑模态表单中的下拉框)
  - [编辑模态表单中的隐式步进滑块](#编辑模态表单中的隐式步进滑块)
  - [编辑模态表单中的显式步进滑块](#编辑模态表单中的显式步进滑块)
- [编辑模态表单](#编辑模态表单-1)
  - [添加元素](#添加元素)
    - [语法](#语法)
    - [备注一](#备注一)
    - [备注二](#备注二)
    - [示例](#示例)
  - [插入元素](#插入元素)
    - [语法](#语法-1)
    - [备注](#备注)
    - [示例](#示例-1)
  - [列出元素](#列出元素)
    - [语法](#语法-2)
    - [示例](#示例-2)
    - [效果（示例）](#效果示例)
  - [弹出元素](#弹出元素)
    - [语法](#语法-3)
    - [备注](#备注-1)
    - [示例](#示例-3)
  - [截断元素](#截断元素)
    - [语法](#语法-4)
    - [备注一](#备注一-1)
    - [备注二](#备注二-1)
    - [示例](#示例-4)
  - [设置标题文本](#设置标题文本)
    - [语法](#语法-5)
    - [示例](#示例-5)
- [编辑模态表单中的输入框](#编辑模态表单中的输入框-1)
  - [语法](#语法-6)
  - [示例](#示例-6)
  - [效果（示例）](#效果示例-1)
  - [补充](#补充)
- [编辑模态表单中的开关](#编辑模态表单中的开关-1)
  - [语法](#语法-7)
  - [示例一](#示例一)
  - [示例二](#示例二)
  - [效果（示例二）](#效果示例二)
- [编辑模态表单中的下拉框](#编辑模态表单中的下拉框-1)
  - [语法](#语法-8)
  - [示例一](#示例一-1)
  - [示例二](#示例二-1)
  - [效果（示例二）](#效果示例二-1)
- [编辑模态表单中的隐式步进滑块](#编辑模态表单中的隐式步进滑块-1)
  - [语法](#语法-9)
  - [示例](#示例-7)
  - [效果（示例）](#效果示例-2)
  - [解释](#解释)
  - [备注一](#备注一-2)
  - [备注二](#备注二-2)
- [编辑模态表单中的显式步进滑块](#编辑模态表单中的显式步进滑块-1)
  - [概览](#概览)
  - [语法](#语法-10)
  - [示例](#示例-8)
  - [效果（示例）](#效果示例-3)







# 前情提要
模态表单中存在相当多的命令需要您通过编写代码来进行构建。<br/>
如果您还没有学习如何在本模组中编写代码，则您最好先进行一个初步的了解。<br/>
您可以通过参看 [自述 § 编程语法](../../../README.md#编程语法) 章节来了解关于编写代码的详细细节。







# 指令概览
## 编辑模态表单
```mcfunction
editmodalform <formName: string> append label|header|divider|input|toggle|dropdown|slider|stepslider
editmodalform <formName: string> insert <index: int> label|header|divider|input|toggle|dropdown|slider|stepslider
editmodalform <formName: string> list
editmodalform <formName: string> pop left|right
editmodalform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
editmodalform <formName: string> title <titleCode: string>
```





## 编辑模态表单中的输入框
```mcfunction
editinput <formName: string> <index: int> default <defaultCode: string>
editinput <formName: string> <index: int> placeholder <placeHolderCode: string>
editinput <formName: string> <index: int> text <textCode: string>
editinput <formName: string> <index: int> tooltip [tooltipCode: string]
```





## 编辑模态表单中的开关
```mcfunction
edittoggle <formName: string> <index: int> default <stateCode: string>
edittoggle <formName: string> <index: int> text <textCode: string>
edittoggle <formName: string> <index: int> tooltip [tooltipCode: string]
```





## 编辑模态表单中的下拉框
```mcfunction
editdropdown <formName: string> <index: int> append <optionCode: string>
editdropdown <formName: string> <index: int> default <indexCode: string>
editdropdown <formName: string> <index: int> insert <index: int> <optionCode: string>
editdropdown <formName: string> <index: int> list
editdropdown <formName: string> <index: int> pop left|right
editdropdown <formName: string> <index: int> sub keep|discard <startIndex: int> <endIndex: int>
editdropdown <formName: string> <index: int> text <textCode: string>
editdropdown <formName: string> <index: int> tooltip [tooltipCode: string]
```





## 编辑模态表单中的隐式步进滑块
```mcfunction
editslider <formName: string> <index: int> default <defaultCode: string>
editslider <formName: string> <index: int> min <minCode: string>
editslider <formName: string> <index: int> max <maxCode: string>
editslider <formName: string> <index: int> step <stepCode: string>
editslider <formName: string> <index: int> text <textCode: string>
editslider <formName: string> <index: int> tooltip [tooltipCode: string]
```





## 编辑模态表单中的显式步进滑块
```mcfunction
editstepslider <formName: string> <index: int> append <stepCode: string>
editstepslider <formName: string> <index: int> default <indexCode: string>
editstepslider <formName: string> <index: int> insert <index: int> <stepCode: string>
editstepslider <formName: string> <index: int> list
editstepslider <formName: string> <index: int> pop left|right
editstepslider <formName: string> <index: int> sub keep|discard <startIndex: int> <endIndex: int>
editstepslider <formName: string> <index: int> text <textCode: string>
editstepslider <formName: string> <index: int> tooltip [tooltipCode: string]
```







# 编辑模态表单
## 添加元素
### 语法
向模态表单 `<formName: string>` 添加（追加）一个元素。
```mcfunction
editmodalform <formName: string> append label|header|divider|input|toggle|dropdown|slider|stepslider
```

| 元素 ID    | 元素名称     | 图例                                                                                    |
| ---------- | ------------ | --------------------------------------------------------------------------------------- |
| label      | 普通文本     | <img width="400" height="35" alt="Image" src="../../images/sample_modal_label.png" />   |
| header     | 大字文本     | <img width="400" height="59" alt="Image" src="../../images/sample_modal_header.png" />  |
| divider    | 分割线       | <img width="400" height="35" alt="Image" src="../../images/sample_modal_divider.png" /> |
| input      | 输入框       | <img width="400" height="100" alt="Image" src="../../images/sample_input.png" />        |
| toggle     | 开关         | <img width="400" height="50" alt="Image" src="../../images/sample_toggle.png" />        |
| dropdown   | 下拉框       | <img width="400" height="100" alt="Image" src="../../images/sample_dropdown.png" />     |
| slider     | 隐式步进滑块 | <img width="400" height="75" alt="Image" src="../../images/sample_slider.png" />        |
| stepslider | 显式步进滑块 | <img width="400" height="75" alt="Image" src="../../images/sample_step_slider.png" />   |



### 备注一
通过该方式添加的元素后，您需要通过其他指令来进一步编辑它们。<br/>
这意味着通过该方式添加的元素在一开始都保持下面列出的默认状态。

- 普通文本
  - 空文本
- 大字文本
  - 空文本
- 输入框
  - 标题文本为空文本
  - 输入框提示语为空文本
  - 输入框的已输入内容（默认内容）为空文本
  - 空灯泡提示文本
- 开关
  - 标题文本为空文本
  - 开关默认保持关闭
  - 空灯泡提示文本
- 下拉框
  - 标题文本为空文本
  - 空灯泡提示文本
  - **默认没有任何选项**
- 隐式步进滑块
  - 标题文本为空文本
  - 最小值为 0.0
  - 最大值为 1.0
  - 单次步进长度为 1.0
  - 默认值为 0.0
  - 空灯泡提示文本
- 显式步进滑块
  - 标题文本为空文本
  - 空灯泡提示文本
  - **默认没有任何选项**

由于分割线在添加后无需进一步修改，因此它将始终保持在相同的状态。



### 备注二
在通过指令向玩家展示（打开）模态表单时，<br/>
我们对 `下拉框` 和 `显式步进滑块` 具有下面的限制。

- 模态表单中的每个 `下拉框` 必须要有**至少 1 个选项**
- 模态表单中的每个 `显式步进滑块` 必须要有**至少 2 个选项**

您需要通过其他指令来编辑添加的 `下拉框` 和 `显式步进滑块`，<br/>
以使得它们的选项数量达到最低要求（或超过最低要求）。



### 示例
```mcfunction
# 向模态表单 你好 添加一个普通文本
editmodalform 你好 append label

# 向模态表单 667788 添加一个大字文本
editmodalform "667788" append header

# 向模态表单 wow 添加一个分割线
editmodalform wow append divider

# 向模态表单 happy2018new 添加一个输入框
editmodalform happy2018new append input

# 向模态表单 bb 添加一个开关
editmodalform bb append toggle

# 向模态表单 hello 添加一个下拉框
editmodalform hello append dropdown

# 向模态表单 233 添加一个隐式步进滑块
editmodalform "233" append slider

# 向模态表单 my_form 添加一个显式步进滑块
editmodalform my_form append stepslider
```





## 插入元素
### 语法
在模态表单 `<formName: string>` 的索引 `<index: int>` 处插入一个元素。
```mcfunction
editmodalform <formName: string> insert <index: int> label|header|divider|input|toggle|dropdown|slider|stepslider
```



### 备注
插入元素的行为与上方的添加元素的行为保持一致，<br/>
它们的唯一区别在于插入元素可以指定插入的位置。

关于索引的概念，以及在何处插入元素，<br/>
请参看 [编辑长表单 § 插入元素](./long_form.md#插入元素) 章节。



### 示例
下述所有指令都是在模态表单 `a0` 上操作的。

```mcfunction
# 在第一个元素的后面插入一个开关
editmodalform a0 insert 1 toggle

# 在第三个元素的前面插入一个隐式步进滑块
editmodalform a0 insert 2 toggle
```





## 列出元素
### 语法
列出模态表单 `<formName: string>` 中的所有元素。
```mcfunction
editmodalform <formName: string> list
```



### 示例
```mcfunction
# 列出模态表单 cookie 中的所有元素
editmodalform cookie list
```



### 效果（示例）
```
模态表单 "cookie" 目前已存在 4 个元素:
  - 普通文本
  - 分割线
  - 大字文本
  - 普通文本
  - 普通文本
  - 开关
```





## 弹出元素
### 语法
弹出（移除）模态表单 `<formName: string>` 中的第一个元素或最后一个元素。
```mcfunction
editmodalform <formName: string> pop left|right
```



### 备注
枚举值 `left|right` 的含义如下。
- left: 弹出（移除）第一个元素
- right: 弹出（移除）最后一个元素



### 示例
```mcfunction
# 移除模态表单 yorha 中的第一个元素
editmodalform yorha pop left

# 移除模态表单 2018 中的最后一个元素
editmodalform "2018" pop right
```





## 截断元素
### 语法
只保留或只丢弃模态表单中的一部分元素。
```mcfunction
editmodalform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
```


| 参数               | 数据类型 | 备注 | 解释                   |
| ------------------ | -------- | ---- | ---------------------- |
| <formName: string> | 字符串   | 必填 | 被编辑的模态表单的名字 |
| keep\|discard      | 枚举值   | 必填 | 操作类型               |
| <startIndex: int>  | 整数     | 必填 | 涉及的元素的起始索引   |
| <endIndex: int>    | 整数     | 必填 | 涉及的元素的结束索引   |



### 备注一
枚举值 `keep|discard` 的含义如下。
- keep: 只保留模态表单中的一部分元素
- discard: 只丢弃模态表单中的一部分元素



### 备注二
模态表单的截断元素的行为与 [编辑长表单 § 截断元素](./long_form.md#截断元素) 的行为基本一致。<br/>
它们在本质上并没有太大的区别，因此本处不再赘述截断元素在编辑模态表单中的用法。



### 示例
```mcfunction
# 只保留模态表单 super 中的第一、二、三、四、五个元素，剩余的丢弃
editmodalform super sub keep 0 5

# 只移除模态表单 bbc 中的第二、三、四、五、六个元素，保留剩余的
editmodalform bbc sub discard 1 6
```





## 设置标题文本
### 语法
设置模态表单要显示的标题文本。
```mcfunction
editmodalform <formName: string> title <titleCode: string>
```

| 参数                | 数据类型 | 备注 | 解释                   |
| ------------------- | -------- | ---- | ---------------------- |
| <formName: string>  | 字符串   | 必填 | 被编辑的模态表单的名字 |
| <titleCode: string> | 字符串   | 必填 | 用于生成标题文本的代码 |

<img width="449" height="400" alt="Image" src="../../images/edit_modal_form_title.png" />



### 示例
```mcfunction
# 设置模态表单 “good night today!” 的标题文本为 “我|是|标|题”
editmodalform "good night today!" title "return '我|是|标|题'"

# 设置模态表单 aaaaa 的标题文本为 我我是是标标题题
editmodalform aaaaa title "return '我我是是标标题题'"
```







# 编辑模态表单中的输入框
## 语法
假定模态表单 `<formName: string>` 中索引为 `<index: int>` 的元素为输入框。

---

将该输入框的已输入内容设置为 `<defaultCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该输入框的已输入内容。

```mcfunction
editinput <formName: string> <index: int> default <defaultCode: string>
```

---

将该输入框的提示文本设置为 `<placeHolderCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该提示框的提示文本。

```mcfunction
editinput <formName: string> <index: int> placeholder <placeHolderCode: string>
```

---

将该输入框的标题文本设置为 `<labelCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该输入框的标题文本。

```mcfunction
editinput <formName: string> <index: int> text <textCode: string>
```

---

将该输入框的灯泡提示文本设置为 `[tooltipCode: string]`。<br/>
应确保它是一个代码，该代码被用于生成该输入框的灯泡提示文本。

```mcfunction
editinput <formName: string> <index: int> tooltip [tooltipCode: string]
```

可以通过不填 `[tooltipCode: string]` 来清空已设置的灯泡提示文本。





## 示例
```mcfunction
# 创建名为 ohhh 的模态表单
customform add ohhh modal

# 向该模态表单添加一个输入框
editmodalform ohhh append input

# 将输入框的标题文本设置为固定的 “您的生日是什么时候？”
editinput ohhh 0 text "return '您的生日是什么时候？'"

# 将输入框的的提示文本设置为固定的 “1990-01-01”
editinput ohhh 0 placeholder "return '1990-01-01'"

# 将输入框的灯泡提示文本设置为固定的 生日是您的出生日期
editinput ohhh 0 tooltip "return '生日是您的出生日期'"

# 向最近的玩家展示（打开）该模态表单（在命令方块中执行）
customform show @p ~ ~ ~ @p ohhh
```





## 效果（示例）
<img width="450" height="400" alt="Image" src="../../images/edit_input_1.png" /><img width="10" height="1" style="border:0;"><img width="450" height="400" alt="Image" src="../../images/edit_input_2.png" />





## 补充
在上面示例的基础上，如果在打开表单前额外执行下面的指令，则输入框将出现已经输入的内容。
```mcfunction
editinput ohhh 0 default "return '2000-12-31'"
```

<img width="450" height="400" alt="Image" src="../../images/edit_input_3.png" />

在将这些已输入内容删除后，原来的灰色提示语会重新出现。







# 编辑模态表单中的开关
## 语法
假定模态表单 `<formName: string>` 中索引为 `<index: int>` 的元素为开关。

---

将这个开关的默认开关状态设置为 `<stateCode: string>`。<br/>
应确保它是一个代码，该代码被确定这个开关的默认开关状态。

```mcfunction
edittoggle <formName: string> <index: int> default <stateCode: string>
```

---

将这个开关的标题文本设置为 `<textCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成这个开关的标题文本。

```mcfunction
edittoggle <formName: string> <index: int> text <textCode: string>
```

---

将这个开关的灯泡提示文本设置为 `[tooltipCode: string]`。<br/>
应确保它是一个代码，该代码被用于生成这个开关的灯泡提示文本。

```mcfunction
edittoggle <formName: string> <index: int> tooltip [tooltipCode: string]
```

可以通过不填 `[tooltipCode: string]` 来清空已设置的灯泡提示文本。





## 示例一
```mcfunction
# 将模态表单 modal_modal_form 中第三个元素（开关）的默认开关状态设置为关闭
edittoggle abc 2 default "return False"

# 将模态表单 modal_modal_form 中第三个元素（开关）的标题文本设置为固定的 你好
edittoggle abc 2 text "return '你好'"
```





## 示例二
```mcfunction
# 将模态表单 wu_ming 中第一个元素（开关）的默认开关状态设置为开启
edittoggle wu_ming 0 default "return True"

# 将模态表单 wu_ming 中第一个元素（开关）的标题文本设置为一到一百的求和结果
edittoggle wu_ming 0 text "total = 0
for i, 101:
  total = total + i
rof
return str(total)"

# 将模态表单 wu_ming 中第一个元素（开关）的
# 灯泡提示文本设置为固定的 一到一百的求和结果
edittoggle wu_ming 0 tooltip "return '一到一百的求和结果'"
```





## 效果（示例二）
<img width="450" height="400" alt="Image" src="../../images/edit_toggle_1.png" /><img width="10" height="1" style="border:0;"><img width="450" height="400" alt="Image" src="../../images/edit_toggle_2.png" />







# 编辑模态表单中的下拉框
## 语法
假定模态表单 `<formName: string>` 中索引为 `<index: int>` 的元素为下拉框。

---

向该下拉框添加（追加）一个选项，并且选项的文本是 `<optionCode: string>`。<br/>
应确保 `<optionCode: string>` 是一个代码，该代码被用于生成该选项的文本。

```mcfunction
editdropdown <formName: string> <index: int> append <optionCode: string>
```

---

设置该下拉框在一开始时选中的选项（也即默认选项）。<br/>
代码 `<indexCode: string>` 用于生成默认选项的索引值。

```mcfunction
editdropdown <formName: string> <index: int> default <indexCode: string>
```

---

向该下拉框插入一个选项，并且选项的文本是 `<optionCode: string>`。<br/>
应确保 `<optionCode: string>` 是一个代码，该代码被用于生成该选项的文本。<br/>
另外，第二个 `<index: int>` 用于确定插入的位置，它是一个索引值。

```mcfunction
editdropdown <formName: string> <index: int> insert <index: int> <optionCode: string>
```

该子命令的工作方式与 [编辑长表单 § 插入元素](./long_form.md#插入元素) 的没有太大区别，<br/>
因此如果您不知道该子命令的工作方式，那么请参看上面的章节。

---

列出该下拉框已经存在的选项的数量。
```mcfunction
editdropdown <formName: string> <index: int> list
```

---

弹出该下拉框中的第一个选项或最后一个选项。
```mcfunction
editdropdown <formName: string> <index: int> pop left|right
```

枚举值 `left|right` 的含义如下。
- left: 弹出（移除）第一个选项
- right: 弹出（移除）最后一个选项

---

只保留或只丢弃该下拉框中的一部分选项。
```mcfunction
editdropdown <formName: string> <index: int> sub keep|discard <startIndex: int> <endIndex: int>
```

| 参数              | 数据类型 | 备注 | 解释                 |
| ----------------- | -------- | ---- | -------------------- |
| keep\|discard     | 枚举值   | 必填 | 操作类型             |
| <startIndex: int> | 整数     | 必填 | 涉及的选项的起始索引 |
| <endIndex: int>   | 整数     | 必填 | 涉及的选项的结束索引 |

枚举值 `keep|discard` 的含义如下。
- keep: 只保留下拉框中的一部分选项
- discard: 只丢弃下拉框中的一部分选项

该子命令的工作方式与 [编辑长表单 § 截断元素](./long_form.md#截断元素) 的没有太大区别，<br/>
因此如果您不知道该子命令的工作方式，那么请参看上面的章节。

---

将该下拉框的标题文本设置为 `<textCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该下拉框的标题文本。

```mcfunction
editdropdown <formName: string> <index: int> text <textCode: string>
```

---

将该下拉框的灯泡提示文本设置为 `[tooltipCode: string]`。<br/>
应确保它是一个代码，该代码被用于生成该下拉框的灯泡提示文本。

```mcfunction
editdropdown <formName: string> <index: int> tooltip [tooltipCode: string]
```

可以通过不填 `[tooltipCode: string]` 来清空已设置的灯泡提示文本。





## 示例一
```mcfunction
# 向模态表单 cq 的第五个元素（下拉框）插入一个没有文字的空选项，
# 并且插入在该下拉框的第二个选项之后
editdropdown cq 4 insert 2 "return ''"

# 列出模态表单 alpha 的第十个元素（下拉框）的选项数量
editdropdown alpha 9 list

# 弹出模态表单 beta 的第二个元素（下拉框）中的第一个选项
editdropdown beta 1 pop left

# 弹出模态表单 beta 的第二个元素（下拉框）中的最后一个选项
editdropdown beta 1 pop right

# 操作模态表单 gamma 的第八个元素（下拉框），
# 将该下拉框中的第五个选项到第九个选项保留，
# 其余的选项全部移除
editdropdown gamma 7 sub keep 4 9

# 操作模态表单 gamma 的第八个元素（下拉框），
# 将该下拉框中的第一个选项到第三个选项移除，
# 其余的选项全部保留
editdropdown gamma 7 sub discard 0 3
```





## 示例二
```mcfunction
# 创建一个名为 abc 的模态表单
customform add abc modal

# 向该模态表单添加一个普通文本
editmodalform abc append label

# 向该模态表单添加一个下拉框
editmodalform abc append dropdown

# 向下拉框添加一个选项，文本为固定的 a
editdropdown abc 1 append "return 'a'"

# 向下拉框添加一个选项，文本为固定的 b
editdropdown abc 1 append "return 'b'"

# 将这个下拉框的标题文本设置为固定的 c
editdropdown abc 1 text "return 'c'"

# 将这个下拉框一开始选中的选项（默认选项）设置为第二个选项
editdropdown abc 1 default "return 1"

# 将这个下拉框的灯泡提示文本设置为固定的 我是一个提示文本
editdropdown abc 1 tooltip "return '我是一个提示文本'"

# 向最近的玩家展示（打开）该模态表单（在命令方块中执行）
customform show @p ~ ~ ~ @p abc
```





## 效果（示例二）
<img width="313" height="278" alt="Image" src="../../images/edit_dropdown_1.png" /><img width="10" height="1" style="border:0;"><img width="313" height="278" alt="Image" src="../../images/edit_dropdown_2.png" /><img width="10" height="1" style="border:0;"><img width="313" height="278" alt="Image" src="../../images/edit_dropdown_3.png" />







# 编辑模态表单中的隐式步进滑块
## 语法
假定模态表单 `<formName: string>` 中索引为 `<index: int>` 的元素为隐式步进滑块。

---

设置该隐式步进滑块的默认值（数字）为 `<defaultCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该隐式步进滑块的默认值（数字）。

```mcfunction
editslider <formName: string> <index: int> default <defaultCode: string>
```

---

设置该隐式步进滑块的最小值（数字）为 `<minCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该隐式步进滑块的最小值（数字）。

```mcfunction
editslider <formName: string> <index: int> min <minCode: string>
```

---

设置该隐式步进滑块的最大值（数字）为 `<maxCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该隐式步进滑块的最大值（数字）。

```mcfunction
editslider <formName: string> <index: int> max <maxCode: string>
```

---

设置该隐式步进滑块的步进长度（数字）为 `<stepCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该隐式步进滑块的步进长度（数字）。

```mcfunction
editslider <formName: string> <index: int> step <stepCode: string>
```

---

设置该隐式步进滑块的标题文本为 `<textCode: string>`。<br/>
应确保它是一个代码，该代码被用于生成该隐式步进滑块的标题文本。

```mcfunction
editslider <formName: string> <index: int> text <textCode: string>
```

---

设置该隐式步进滑块的灯泡提示文本为 `[tooltipCode: string]`。<br/>
应确保它是一个代码，该代码被用于生成该隐式步进滑块的灯泡提示文本。

```mcfunction
editslider <formName: string> <index: int> tooltip [tooltipCode: string]
```

可以通过不填 `[tooltipCode: string]` 来清空已设置的灯泡提示文本。





## 示例
```mcfunction
# 创建一个名为 app 的模态表单
customform add app modal

# 向该模态表单添加一个隐式步进滑块
editmodalform app append slider

# 将该隐式步进滑块的标题文本设置为固定的 aaa
editslider app 0 text "return 'aaa'"

# 将该隐式步进滑块的最小值设置为固定的 -5.0
editslider app 0 min "return -5.0"

# 将该隐式步进滑块的最大值设置为固定的 5
editslider app 0 max "return 5"

# 将该隐式步进滑块的步进长度设置为固定的 0.5
editslider app 0 step "return 0.5"

# 将该隐式步进滑块的默认值设置为固定的 3.5
editslider app 0 default "return 3.5"

# 将该隐式步进滑块的灯泡提示文本设置为固定的 666
editslider app 0 tooltip "return '666'"

# 向最近的玩家展示（打开）该模态表单（在命令方块中执行）
customform show @p ~ ~ ~ @p app
```





## 效果（示例）
<img width="450" height="400" alt="Image" src="../../images/edit_slider_1.png" /><img width="10" height="1" style="border:0;"><img width="450" height="400" alt="Image" src="../../images/edit_slider_2.png" />





## 解释
在上面这个示例中，我们将 `隐式步进滑块` 的最小值和最大值分别设为了 -5 和 5。<br/>
这意味着玩家移动滑块时，滑块所指向的实际值只可能在 -5 到 5 之间（当然也包括 -5 和 5）。

那么什么是步进长度呢？<br/>
实际上，步进长度代表了滑块的最小刻度。

在这个例子中，我们使用的步进长度是 0.5，<br/>
这意味着玩家在移动滑块时，滑块所指向的实际值只能取得以下的值。

```
-5.0,   -4.5,   -4.0,   -3.5,   -3.0,
-2.5,   -2.0,   -1.5,   -1.0,   -0.5,
+0.0,   +0.5,   +1.0,   +1.5,   +2.0,
+2.5,   +3.0,   +3.5,   +4.0,   +4.5,
+5.0
```

这意味着移动滑块不会取得诸如 4.7 这样的值，即便它在 -5 到 5 之间。





## 备注一
如果您提供的最小值、最大值和步进长度不足以使滑块从最小值抵达最大值，<br/>
则系统可以确保玩家仍然能取得您提供的最大值。

一个例子是最小值为 0，最大值为 5，步进长度为 0.4 的情况。
```
0.0,    0.4,    0.8,    1.2,    1.6,
2.0,    2.4,    2.8,    3.2,    3.6,
4.0,    4.4,    4.8
```

很显然，在正常情况下，最大值 5 是不可达的，但我们这里仍然确保玩家能够取得 5。<br/>
值得注意的是，如果提供的默认值是不可达的，则滑块的默认位置将被修正到距离其最近的一个值（但不超过提供的默认值）。





## 备注二
如何判定某个数 $x$ 在最小值为 $min$，最大值为 $max$，步进长度为 $step$ 的情况下是否可达？

这个问题不难，因为隐式步进滑块能得到的数字构成了等差数列。<br/>
其中，等差数列的首项为 $min$，公差为 $step$。

因此，这个等差数列可以形式化为 $T_n=min+(n-1)\times{step}$。<br/>
其中， $T_n$ 代表等差数列的第 $n$ 项。

如果 $x$ 是可达的，那么有 $x=min+(m-1)\times{step}$。<br/>
其中 $m$ 是个整数。

容易写出 $m$ 的表达式是 $m=\frac{x-min}{step}+1$。<br/>
由于 $m$ 是整数，所以 $m-1=\frac{x-min}{step}$ 也是整数。

这意味着只需要检查 $\frac{x-min}{step}$ 是否是整数即可。<br/>
因此，只需要判断 $(x-min)\bmod{step}=0$ 是否成立即可。<br/>
同时，我们还需要考虑 $x\in[min,max]$。

这意味着只要下式全部成立，则 $x$ 在给定的条件下是可达的。
```math
\begin{cases} 
(x-min)\bmod{step}=0 \\
x\in[min,max]
\end{cases}
```







# 编辑模态表单中的显式步进滑块
## 概览
```mcfunction
editstepslider <formName: string> <index: int> append <stepCode: string>
editstepslider <formName: string> <index: int> default <indexCode: string>
editstepslider <formName: string> <index: int> insert <index: int> <stepCode: string>
editstepslider <formName: string> <index: int> list
editstepslider <formName: string> <index: int> pop left|right
editstepslider <formName: string> <index: int> sub keep|discard <startIndex: int> <endIndex: int>
editstepslider <formName: string> <index: int> text <textCode: string>
editstepslider <formName: string> <index: int> tooltip [tooltipCode: string]
```





## 语法
该章节的语法和 [编辑模态表单中的下拉框 § 语法](#语法-8) 几乎没有区别，<br/>
因此本处将不再赘述语法，具体参看上面该章节的内容进行理解。





## 示例
```mcfunction
# 创建一个名为 ggb 的模态表单
customform add ggb modal

# 向该模态表单添加一个显式步进滑块
editmodalform ggb append stepslider

# 将该显式步进滑块的标题文本设置为固定的 “Hello, World!”
editstepslider ggb 0 text "return 'Hello, World!'"

# 向该显式步进滑块添加一个选项，文本为固定的 a
editstepslider ggb 0 append "return 'a'"

# 向该显式步进滑块添加一个选项，文本为固定的 b
editstepslider ggb 0 append "return 'b'"

# 向该显式步进滑块添加一个选项，文本为固定的 c
editstepslider ggb 0 append "return 'c'"

# 在该显式步进滑块的第一个选项后插入一个选项，文本为固定的 d
editstepslider ggb 0 insert 1 "return 'd'"

# 在该显式步进滑块的第二个选项后插入一个选项，文本为固定的 e
editstepslider ggb 0 insert 2 "return 'e'"

# 在该显式步进滑块的第三个选项后插入一个选项，文本为固定的 happy
editstepslider ggb 0 insert 3 "return 'happy'"

# 弹出该显式步进滑块的第一个选项
editstepslider ggb 0 pop left

# 将该显式步进滑块的默认选项设置为第二个选项
editstepslider ggb 0 default "return 2"

# 将该显式步进滑块的灯泡提示文本设置为固定的 献给机械の花束
editstepslider ggb 0 tooltip "return '献给机械の花束'"

# 向最近的玩家展示（打开）该模态表单（在命令方块中执行）
customform show @p ~ ~ ~ @p ggb
```





## 效果（示例）
<img width="450" height="400" alt="Image" src="../../images/edit_step_slider_1.png" /><img width="10" height="1" style="border:0;"><img width="450" height="400" alt="Image" src="../../images/edit_step_slider_2.png" />