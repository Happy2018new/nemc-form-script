# 目录
- [目录](#目录)
- [指令概览](#指令概览)
  - [操作菜单（表单）](#操作菜单表单)
  - [长表单相关](#长表单相关)
    - [编辑长表单](#编辑长表单)
    - [编辑长表单中的按钮](#编辑长表单中的按钮)
  - [编辑长表单或模态表单中的文本元素](#编辑长表单或模态表单中的文本元素)
  - [信息表单相关](#信息表单相关)
  - [模态表单相关](#模态表单相关)
    - [编辑模态表单](#编辑模态表单)
    - [编辑模态表单中的输入框](#编辑模态表单中的输入框)
    - [编辑模态表单中的开关](#编辑模态表单中的开关)
    - [编辑模态表单中的下拉框](#编辑模态表单中的下拉框)
    - [编辑模态表单中的隐式步进滑块](#编辑模态表单中的隐式步进滑块)
    - [编辑模态表单中的显式步进滑块](#编辑模态表单中的显式步进滑块)
  - [自定义函数](#自定义函数)
  - [服务器事件](#服务器事件)
  - [代码缓存器](#代码缓存器)
  - [查询命令方块输出](#查询命令方块输出)





# 指令概览
## 操作菜单（表单）
```mcfunction
customform add <name: string> long|popup|modal
customform list [name: string]
customform oncancel <name: string> <code: string> [onCodeError: string]
customform onsubmit <name: string> <code: string> [onCodeError: string]
customform remove <name: string>
customform save <name: string>
customform show <executor: target> <position: x y z> <player: target> <name: string>
customform style <player: target> [speed_40|speed_35|speed_30|speed_25|speed_20|speed_15|speed_10|speed_05|speed_00]
customform close <player: target>
```



## 长表单相关
### 编辑长表单
```mcfunction
editlongform <formName: string> append [button|label|header|divider]
editlongform <formName: string> content <contentCode: string>
editlongform <formName: string> insert <index: int> [button|label|header|divider]
editlongform <formName: string> list
editlongform <formName: string> pop left|right
editlongform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
editlongform <formName: string> title <titleCode: string>
```

### 编辑长表单中的按钮
```mcfunction
editbutton <formName: string> <index: int> icon [textureCode: string]
editbutton <formName: string> <index: int> text <textCode: string>
```



## 编辑长表单或模态表单中的文本元素
```mcfunction
editlabel <formName: string> <index: int> header <headerCode: string>
editlabel <formName: string> <index: int> label <labelCode: string>
```



## 信息表单相关
```mcfunction
editpopupform <formName: string> button1 <firstButtonCode: string>
editpopupform <formName: string> button2 <secondButtonCode: string>
editpopupform <formName: string> content <contentCode: string>
editpopupform <formName: string> title <titleCode: string>
```



## 模态表单相关
### 编辑模态表单
```mcfunction
editmodalform <formName: string> append label|header|divider|input|toggle|dropdown|slider|stepslider
editmodalform <formName: string> insert <index: int> label|header|divider|input|toggle|dropdown|slider|stepslider
editmodalform <formName: string> list
editmodalform <formName: string> pop left|right
editmodalform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
editmodalform <formName: string> title <titleCode: string>
```

### 编辑模态表单中的输入框
```mcfunction
editinput <formName: string> <index: int> default <defaultCode: string>
editinput <formName: string> <index: int> placeholder <placeHolderCode: string>
editinput <formName: string> <index: int> text <textCode: string>
editinput <formName: string> <index: int> tooltip [tooltipCode: string]
```

### 编辑模态表单中的开关
```mcfunction
edittoggle <formName: string> <index: int> default <stateCode: string>
edittoggle <formName: string> <index: int> text <textCode: string>
edittoggle <formName: string> <index: int> tooltip [tooltipCode: string]
```

### 编辑模态表单中的下拉框
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

### 编辑模态表单中的隐式步进滑块
```mcfunction
editslider <formName: string> <index: int> default <defaultCode: string>
editslider <formName: string> <index: int> min <minCode: string>
editslider <formName: string> <index: int> max <maxCode: string>
editslider <formName: string> <index: int> step <stepCode: string>
editslider <formName: string> <index: int> text <textCode: string>
editslider <formName: string> <index: int> tooltip [tooltipCode: string]
```

### 编辑模态表单中的显式步进滑块
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



## 自定义函数
```mcfunction
customfunction add <name: string> <code: string>
customfunction call <executor: target> <position: x y z> <name: string>
customfunction list [name: string]
customfunction remove <name: string>
```



## 服务器事件
```mcfunction
systemevent destroy <funcName: string>
systemevent list [eventName: string]
systemevent listen <eventName: string> <funcName: string> <code: string> [onCodeError: string]
systemevent query <funcName: string>
```



## 代码缓存器
```mcfunction
compilecache compile <code: string>
compilecache query
compilecache set [size: int]
```



## 查询命令方块输出
```mcfunction
commandblockoutput <commandBlockPosition: x y z>
```