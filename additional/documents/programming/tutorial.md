# 目录
- [目录](#目录)
- [教程一](#教程一)
- [教程二](#教程二)
- [教程三](#教程三)
- [教程四](#教程四)
- [教程五](#教程五)
- [教程六](#教程六)
- [教程七](#教程七)
- [教程八](#教程八)



# 教程一
```python
number = 233
result = ''

if 100000 <= number and number <= 999999:
    result = str(number)
fi
if 10000 <= number and number <= 99999:
    result = '0' + str(number)
fi
if 1000 <= number and number <= 9999:
    result = '00' + str(number)
fi
if 100 <= number and number <= 999:
    result = '000' + str(number)
fi
if 10 <= number and number <= 99:
    result = '0000' + str(number)
fi
if 0 <= number and number <= 9:
    result = '00000' + str(number)
fi

return result
```

---

这段代码的主要作用是对数字进行类似下面这样的处理。
- 821321 => 821321
- 82132 => 082132
- 8213 => 008213
- 821 => 000821
- 21 => 000021
- 1 => 000001

这意味着我们会把数字补全到六位数。<br/>
不足六位数的部分用 `0` 代替。

注意，我们只需要考虑那些范围在 0 到 999999 之间的数字。<br/>
这是因为上面的代码只考虑了在这个范围内的数据，其他情况没有纳入。

---

首先，从思路来说，上面的代码将可能存在的情况分为了下面几类，并且给出了对应的处理。

| 分类            | 对应的处理                |
| --------------- | ------------------------- |
| 100000 ~ 999999 | 无需特别处理              |
| 10000 ~ 99999   | 只需要在数字前面加 1 个零 |
| 1000 ~ 9999     | 只需要在数字前面加 2 个零 |
| 100 ~ 999       | 只需要在数字前面加 3 个零 |
| 10 ~ 99         | 只需要在数字前面加 4 个零 |
| 0 ~ 9           | 只需要在数字前面加 5 个零 |

---

然后，基于这样的分类，我们就可以编写对应的代码。<br/>
不过为了便于理解，您可以先着手整理一下思路，就像下面这样。

```python
数字 = ...

如果“数字”在 100000 到 999999 之间：
    那么“数字”就无需特别处理
如果“数字”在 10000 到 99999 之间：
    那么只需要在“数字”前面加 1 个零即可
如果“数字”在 1000 到 9999 之间：
    那么只需要在“数字”前面加 2 个零即可
如果“数字”在 100 到 999 之间：
    那么只需要在“数字”前面加 3 个零即可
如果“数字”在 10 到 99 之间：
    那么只需要在“数字”前面加 4 个零即可
如果“数字”在 0 到 9 之间：
    那么只需要在“数字”前面加 5 个零即可

返回“数字”代表的值
```

那么现在的问题就变成了，应该如何表示 `“数字”在“谁”到“谁”之间` 呢？<br/>

假设我们要表示的是 `“数字”在 100000 到 999999 之间`。<br/>
首先，这个问题等价于 `100000 小于或等于 “数字”` 并且 `999999 大于或等于 “数字”`。

翻译为代码就是这样的。
```python
100000 <= 数字 and 999999 <= 数字
```

现在我们会表示一个数字是否在某个范围内了，<br/>那么我们就可以把我们的思路翻译为实际的代码。

---

我们现在有了一个初步的代码。
```python
number = 233

if 100000 <= number and number <= 999999:
    number = number
fi
if 10000 <= number and number <= 99999:
    number = '0' + number
fi
if 1000 <= number and number <= 9999:
    number = '00' + number
fi
if 100 <= number and number <= 999:
    number = '000' + number
fi
if 10 <= number and number <= 99:
    number = '0000' + number
fi
if 0 <= number and number <= 9:
    number = '00000' + number
fi

return number
```

不过您会发现这段代码其实会报错。原因是因为下面的代码会被执行。
```python
if 100 <= number and number <= 999:
    number = '000' + number
fi
```

在执行到 `number = '000' + number` 的时候将报错。<br/>
这是因为你试图将字符串 '000' 和储存了整数的变量 `number` 相加。

很显然，你只能让数与数之间相加，或者让字符串与字符串之间相加。<br/>
这意味着让字符串和数之间相加是一种不正确的操作，您需要更正。

我们可以通过将变量 `number` 强制转换为字符串，<br/>
然后再将其与字符串 '000' 相加来解决问题。

---

在解决问题后，我们可以得到下面的这个代码。

```python
number = 233

if 100000 <= number and number <= 999999:
    number = str(number)
fi
if 10000 <= number and number <= 99999:
    number = '0' + str(number)
fi
if 1000 <= number and number <= 9999:
    number = '00' + str(number)
fi
if 100 <= number and number <= 999:
    number = '000' + str(number)
fi
if 10 <= number and number <= 99:
    number = '0000' + str(number)
fi
if 0 <= number and number <= 9:
    number = '00000' + str(number)
fi

return number
```

不过您会发现这段代码其实仍然会报错。<br/>
这是因为 `number = '000' + str(number)` 在被执行后，变量 `number` 变成了字符串，<br/>
而后面代码中这个的**条件语句**仍然会尝试执行。

```python
if 10 <= number and number <= 99:
    number = '0000' + str(number)
fi
```

但是变量 `number` 现在已经是字符串了，而不是整数，因此 `10 <= number and number <= 99` 会失败。<br/>
失败的原因是因为你不能比较数字和字符串，因为它们很显然不具备可比性。

要解决这个问题，我们可以单独使用一个变量 `result` 来保存结果，就像这样。
```python
number = 233
result = ''

if 100000 <= number and number <= 999999:
    result = str(number)
fi
if 10000 <= number and number <= 99999:
    result = '0' + str(number)
fi
if 1000 <= number and number <= 9999:
    result = '00' + str(number)
fi
if 100 <= number and number <= 999:
    result = '000' + str(number)
fi
if 10 <= number and number <= 99:
    result = '0000' + str(number)
fi
if 0 <= number and number <= 9:
    result = '00000' + str(number)
fi

return result
```

最终，我们得到了和开始的一模一样的代码。



# 教程二
您可能发现了，我们可以简化[教程一](#教程一)提到的代码，把它变成下面这样。
```python
number = 233
result = ''

if 100000 <= number:
    result = str(number)
elif 10000 <= number:
    result = '0' + str(number)
elif 1000 <= number:
    result = '00' + str(number)
elif 100 <= number:
    result = '000' + str(number)
elif 10 <= number:
    result = '0000' + str(number)
elif 0 <= number:
    result = '00000' + str(number)
fi

return result
```

那如果我们反转条件的顺序呢？就像这样。
```python
number = 233
result = ''

if 0 <= number:
    result = '00000' + str(number)
elif 10 <= number:
    result = '0000' + str(number)
elif 100 <= number:
    result = '000' + str(number)
elif 1000 <= number:
    result = '00' + str(number)
elif 10000 <= number:
    result = '0' + str(number)
elif 100000 <= number:
    result = str(number)
fi

return result
```

你会发现，在反转条件后，任何大于或等于 0 的 `number` 都会落入下面的条件中。<br/>
因此，其他条件不会被执行，所以代码总是给“数字”添加五个零。

```python
if 0 <= number:
    result = '00000' + str(number)
```

然而，如果不进行反转，而是从 `100000 <= number` 开始判断，则不会具有这个问题。<br/>
但是为什么这么做是有效的呢？让我们列表来观察一下。

| number 的范围                         | 反转前命中的条件      | 反转后命中的条件  |
| ------------------------------------- | --------------------- | ----------------- |
| 100000 <= number and number <= 999999 | if 100000 <= number:  | elif 0 <= number: |
| 10000 <= number and number <= 99999   | elif 10000 <= number: | elif 0 <= number: |
| 1000 <= number and number <= 9999     | elif 1000 <= number:  | elif 0 <= number: |
| 100 <= number and number <= 999       | elif 100 <= number:   | elif 0 <= number: |
| 10 <= number and number <= 99         | elif 10 <= number:    | elif 0 <= number: |
| 0 <= number and number <= 9           | elif 0 <= number:     | elif 0 <= number: |

您将发现简化后的代码（也就是反转前的代码）与[教程一](#教程一)的代码的效果是相同的。<br/>
并且您现在也可以理解为什么反转条件之后，代码将无法按预期正常工作。

另外，下面的写法跟本例中的代码也是等效的。<br/>
您很容易就能发现，下面的代码避免使用了 `elif` 关键字。<br/>
这意味着下面的代码通过某种方式把 `elif` 通过 `if` 和 `else` 替代了。

```python
number = 233
result = ''

if 100000 <= number:
    result = str(number)
else:
    if 10000 <= number:
        result = '0' + str(number)
    else:
        if 1000 <= number:
            result = '00' + str(number)
        else:
            if 100 <= number:
                result = '000' + str(number)
            else:
                if 10 <= number:
                    result = '0000' + str(number)
                else:
                    if 0 <= number:
                        result = '00000' + str(number)
                    fi
                fi
            fi
        fi
    fi
fi


return result
```

尽管上面的代码具有相同的作用，您在实际编程时也不应该使用它。<br/>
很显然，这样的代码非常难以阅读，并且编写的时候也很容易出错。



# 教程三
基于[教程二](#教程二)，我们可以存在下面这样的写法。
```python
number = 233

if 100000 <= number:
    return str(number)
elif 10000 <= number:
    return '0' + str(number)
elif 1000 <= number:
    return '00' + str(number)
elif 100 <= number:
    return '000' + str(number)
elif 10 <= number:
    return '0000' + str(number)
elif 0 <= number:
    return '00000' + str(number)
fi
```

您应该很容易看出区别，并且理解为什么可以这么做。



# 教程四
现在让我们在游戏内通过 `say` 命令输出一个三角形。<br/>
类似于下面这种模式（这是一个直角三角形）。

```python
*
***
*****
*******
*********
***********
```

我们可以使用下面的代码。
```python
repeat = 6
star = -1

for _, repeat:
    star = star + 2
    line = 'say ' + '*'*star
    {command, line}
rof
```

这段代码会按顺序依次执行下面的指令。
```mcfunction
say *
say ***
say *****
say *******
say *********
say ***********
```

其中，变量 `repeat` 代表了三角形的行数。或者换句话说，它也代表最终要执行的指令的数量。<br/>
变量 `star` 在会在每次循环执行时发生改变，它用于动态控制每个要执行的指令中的 `*` 的数量。

您可以画一张表来进一步理解代码。<br/>
这张表揭示了每轮循环结束时，各个变量的状态。

| 循环轮次 | star 的值 | line 的值         |
| -------- | --------- | ----------------- |
| 1        | 1         | 'say *'           |
| 2        | 3         | 'say ***'         |
| 3        | 5         | 'say *****'       |
| 4        | 7         | 'say *******'     |
| 5        | 9         | 'say *********'   |
| 6        | 11        | 'say ***********' |

您会发现在每轮循环结束时，变量 `star` 的值和变量 `line` 中的 `*` 的数量是相同的。<br/>
这意味着我们实际上是通过变量 `star` 来控制每轮循环时变量 `line` 中的 `*` 的数量。

另外，您可以注意到该代码没有**返回语句**。这个问题在本例中不是特别重要，您只需要着重关注指令到底是如何构造和执行的。<br/>
需要注意的是，在每轮循环即将结束前，我们执行了 **Command** 语句，也就是下方的这个语句。它用于执行变量 `line` 指示的指令。
```python
{command, line}
```



# 教程五
基于[教程四](#教程四)，如果我们希望得到诸如下方的这样的三角形呢？
```python
*
***
*****
*******
*********
***********
*********
*******
*****
***
*
```

相应的代码实际上如下。
```python
repeat = 6
star = -1

for _, repeat:
    star = star + 2
    line = 'say ' + '*'*star
    {command, line}
rof

for _, repeat-1:
    star = star - 2
    line = 'say ' + '*'*star
    {command, line}
rof
```

它将依次执行下面的命令。
```mcfunction
say *
say ***
say *****
say *******
say *********
say ***********
say *********
say *******
say *****
say ***
say *
```

我们不会解释上面的代码为何可行。<br/>
请您发挥您的聪明才智，自行探索。



# 教程六
```python
repeat = 6
star = 2*repeat-1
space = 0

for _, repeat:
    line = 'say ' + ' '*space + '*'*star + ' '*space
    star = star - 2
    space = space + 1
    {command, line}
rof
```

上面的代码最终会依次执行下面的指令。
```mcfunction
say ***********
say  *********
say   *******
say    *****
say     ***
say      *
```



# 教程七
```python
repeat = 6
star = 1
space = repeat-1

for _, repeat:
    line = 'say ' + ' '*space + '*'*star + ' '*space
    star = star + 2
    space = space - 1
    {command, line}
rof
```

上面的代码最终会依次执行下面的指令。
```mcfunction
say      *
say     ***
say    *****
say   *******
say  *********
say ***********
```



# 教程八
```python
repeat = 6
total = 2*repeat-1

for i, repeat:
    star = 2*i + 1
    space = int((total-star)/2)
    line = 'say ' + ' '*space + '*'*star + ' '*space
    {command, line}
rof

for i, repeat-1:
    star = 2*(repeat-(i+1)) - 1
    space = int((total-star)/2)
    line = 'say ' + ' '*space + '*'*star + ' '*space
    {command, line}
rof
```

上面的代码最终会依次执行下面的指令。
```mcfunction
say      *
say     ***
say    *****
say   *******
say  *********
say ***********
say  *********
say   *******
say    *****
say     ***
say      *
```