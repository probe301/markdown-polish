
import os, sys, re 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0, parentdir)
import shutil
import arrow
from pyshould import should
from datetime import datetime

import dictdiffer
import pytest
import time
import difflib



def sep_split(text, sep=r"([.。!！?？\n+])"):
  result = re.split(sep, text)
  values = result[::2]
  delimiters = result[1::2] + ['']
  return [v+d for v, d in zip(values, delimiters)]

def show_diff(old_code, new_code):
  diff = difflib.ndiff(sep_split(old_code), sep_split(new_code))
  # diff = difflib.ndiff(old_code.splitlines(1), new_code.splitlines(1)) # splitlines(1) 保留行尾的换行
  print('\n'.join(line for line in diff if not line.startswith(' ')))



from polish import Polish

def test_1_hello_world():
  print('hello')


def test_2_merge_line_for_mdlink():
  sample = '''

[

笔记



](https://www.zhihu.com/topic/19554982)

[

知识管理工具

](https://www.zhihu.com/topic/19627718)

[

笔记类应用



](https://www.zhihu.com/topic/19821486)

'''
  result = '''

[笔记](https://www.zhihu.com/topic/19554982)

[知识管理工具](https://www.zhihu.com/topic/19627718)

[笔记类应用](https://www.zhihu.com/topic/19821486)

'''

  Polish(sample).join_markdown_link().text  | should.eq(result)



def test_3_read_clipboard():
  p = Polish.from_clipboard()
  print(p.text)


def test_4_fix_image_assets():
  sample = '''

1. 为你的编辑器安装LiveReload插件
   ![](assets/15780-bb29aa6.png)  

     
2. 如何使用?默认情况下
[![icon](assets/15781-21a54b384.webp)](https://www.xxx.com)

[userlink](assets/15780-bb29aa6.png)关注

职能

![](assets/15781-370d0a66.webp)

Chrome
'''
  result = '''

1. 为你的编辑器安装LiveReload插件
   ![](filename.assets/15780-bb29aa6.png)  

     
2. 如何使用?默认情况下
[![icon](filename.assets/15781-21a54b384.webp)](https://www.xxx.com)

[userlink](assets/15780-bb29aa6.png)关注

职能

![](filename.assets/15781-370d0a66.webp)

Chrome
'''
  Polish(sample).update_image_url(prefix='filename.').text  | should.eq(result)







def test_5_pangu_spacing():
  sample = '當你,凝視著bug，bug也凝視著你'
  result = '當你，凝視著 bug，bug 也凝視著你'
  Polish(sample).pangu_spacing().text | should.eq(result)

  sample = '''
这里需要特别说明的是，`::;c::` 定义了热键`;c`，那么`;c`就相当于一个单词，当你输入这个单词后，这个热键的代码就会被执行。既然是单词，在输入的时候前后都要输入空格来与其他单词分隔，AutoHotkey才会认为它是一个单词，才会激活这个热键。比如，当你输入this;c 时,Autohotkey会认为你输入的this;c才是一个完整的单词，而`;c`只是单词的一部分，从而不会激活`;c`热键。因此，如果你想在输入this 之后通过热键`;c`来切换中文输入法，那么在输入this之后需要加个 空格再输入`;c` , 即`this;c`。如此一来，就多输入了一个空格，有的时候这个空格是多余的, 我们不希望这个空格的存在。那么这个函数的作用,就是用来选中这个多余的空格。在选中这个多余的空格之后，你再输入内容时，会自动替换掉了这个空格，从而无需手工退格删除这个空格了。
'''
  result = '''
这里需要特别说明的是，`::;c::` 定义了热键 `;c`，那么 `;c` 就相当于一个单词，当你输入这个单词后，这个热键的代码就会被执行。既然是单词，在输入的时候前后都要输入空格来与其他单词分隔，AutoHotkey 才会认为它是一个单词，才会激活这个热键。比如，当你输入 this;c 时，Autohotkey 会认为你输入的 this;c 才是一个完整的单词，而 `;c` 只是单词的一部分，从而不会激活 `;c` 热键。因此，如果你想在输入 this 之后通过热键 `;c` 来切换中文输入法，那么在输入 this 之后需要加个 空格再输入 `;c` , 即 `this;c`。如此一来，就多输入了一个空格，有的时候这个空格是多余的，我们不希望这个空格的存在。那么这个函数的作用，就是用来选中这个多余的空格。在选中这个多余的空格之后，你再输入内容时，会自动替换掉了这个空格，从而无需手工退格删除这个空格了。
'''
  # show_diff(Polish(sample).pangu_spacing().text.strip(), result.strip())
  Polish(sample).pangu_spacing().text.strip() | should.eq(result.strip())




@pytest.mark.skip(reason="wait")
def test_6_pangu_spacing_level2():
  # 需要能保留 `` 内部结构
  sample = '''那么`SelectLeftSpaceChar()`这个函数的作用,就是用来选中这个多余的空格. 在选中这个多余的空格之后'''
  result = '''那么 `SelectLeftSpaceChar()` 这个函数的作用，就是用来选中这个多余的空格。在选中这个多余的空格之后'''
  Polish(sample).pangu_spacing().text.strip() | should.eq(result.strip())

  sample = '當你,凝視著bug,bug也凝視著你'
  result = '當你，凝視著 bug, bug 也凝視著你'





# sample
def test_7_transword():
  sample = '''登陆网站异常, 请稍后, 您可以定义对象所期望的操作和属性, 而不是显示声明其类型'''
  result = '''登录网站异常, 请稍候, 您可以定义对象所期望的操作和属性, 而不是显式声明其类型'''
  Polish(sample).transword().text | should.eq(result)

  sample = '''那么`SelectLeftSpaceChar（）`这个“函数”的作用'''
  result = '''那么`SelectLeftSpaceChar()`这个"函数"的作用'''
  Polish(sample).transword().text | should.eq(result)



def test_8_extract_outline():
  # 提取标题
  sample = '''
# title1

## title2
text
text

## title3

text

#### sub1

text


## title4

#### sub2

### sub3

#### sub4

text

> quote paragraph
> 
> # quote title1
> 

```python
code
# comments
## comments
code
```

\## not title5

    ## title6

## title7

'''

  result = '''# title1
## title2
## title3
## title4
### sub3
## title7'''.splitlines()
  # Polish(sample).extract_outline(headers='h1,h2,h3', paragraph='full,preview,none') | should.eq(result)
  Polish(sample).extract_outline(headers='h1,h2,h3') | should.eq(result)


def test_9a_extract_notes_highlight():
  sample = '''
提取高亮 即 ==xxx== 之间的内容

==高亮== 有可能==在同一行中==出现两次

提取<span color='red'>自定义的</span>颜色

## 可能出现在<span color=#7ed>标题</ span>里

    可能出现在缩进块里, 可能有<font style='background:#def; font-size:1.5rem; color: #edb;'>不同的颜色定义</font>标签

不提取<span color='red'>带有换行

换行之后</span>的内容


'''
  # highlight
  result_should = [
    ('highlight', '==xxx=='),
    ('highlight', '==高亮=='),
    ('highlight', '==在同一行中=='),
    ('highlight', "<span color='red'>自定义的</span>"),
    ('highlight', "<span color=#7ed>标题</ span>"),
    ('highlight', "<font style='background:#def; font-size:1.5rem; color: #edb;'>不同的颜色定义</font>"),
  ]
  Polish(sample).extract_highlights() | should.eq(result_should)




def test_9b_extract_notes_annotations():
  sample = '''
提取注记

注记 提取block note

!!! note

    xxxx
    xxxx

sep

!!! danger
    xxxx
      
    xxxx

    xxxx

text


'''
  result_should = [
    ('annotation', '!!! note\n\n    xxxx\n    xxxx\n\n'),
    ('annotation', '!!! danger\n    xxxx\n      \n    xxxx\n\n    xxxx\n\n'),
    ]
  Polish(sample).extract_annotations() | should.eq(result_should)


@pytest.mark.skip(reason="wait")
def test_9c_extract_notes_annotations_level2():
  sample = '''
提取高亮, 注记, 以及自定义容器

注记 提取两种 block note

!!! note

    xxxx
    xxxx

::: tip

也应该包括这种提示

:::

::::: container
:::: row
::: col-xs-6 alert alert-success
success text
:::
::: col-xs-6 alert alert-info
warning text
:::
::::
:::::

'''
  # annotation
  result_should = [
    ('annotation', '!!! note\n\n    xxxx\n    xxxx\n\n'),
    ('annotation', '::: tip\n\n这是一个提示\n\n:::\n\n'),
    ]
  Polish(sample).extract_notes(highlight=False, annotation=True) | should.eq(result_should)






def test_10_split_md_blocks():
  sample = '''
# title1

## title2
text
text

## title3

text

#### sub1

text


## title4

#### sub2

### sub3

#### sub4

text

> quote paragraph
> 
> # quote title1
      
> text

```python
code
# comments
## comments
code
```

----------sep----

\## not title5

    ## title6
    
    indent2

## title7

text

!!! note

    xxxx
    xxxx

text

'''
  from polish import BlockType
  result_should = [
  (BlockType.title, '# title1\n\n'),
  (BlockType.title, '## title2\n'),
  (BlockType.p, 'text\n'),
  (BlockType.p, 'text\n\n'),
  (BlockType.title, '## title3\n\n'),
  (BlockType.p, 'text\n\n'),
  (BlockType.title, '#### sub1\n\n'),
  (BlockType.p, 'text\n\n\n'),
  (BlockType.title, '## title4\n\n'),
  (BlockType.title, '#### sub2\n\n'),
  (BlockType.title, '### sub3\n\n'),
  (BlockType.title, '#### sub4\n\n'),
  (BlockType.p, 'text\n\n'),
  (BlockType.quote, '> quote paragraph\n> \n> # quote title1\n      \n> text\n\n'),
  (BlockType.fencecode, '```python\ncode\n# comments\n## comments\ncode\n```\n\n'),
  (BlockType.sepline, '----------sep----\n\n'),
  (BlockType.p, '\\## not title5\n\n'),
  (BlockType.indent, '    ## title6\n    \n    indent2\n\n'),
  (BlockType.title, '## title7\n\n'),
  (BlockType.p, 'text\n\n'),
  (BlockType.admonition, '!!! note\n\n    xxxx\n    xxxx\n\n'),
  (BlockType.p, 'text'),
  
  ]
  result = list(Polish(sample)._split_markdown_blocks(sample.strip()))

  from pprint import pprint as pp
  pp(result)

  len(result) | should.eq(len(result_should))
  for line_actual, line_should in zip(result, result_should):
    line_actual | should.eq(line_should)






# sample
def test_playground():
  import re
  sample = '''
1

2

> quote paragraph
> 
> # quote title1
      
> text


5
'''


  result = re.split(r"([\n]+)", sample.strip())
  print(result)
  values = result[::2]
  delimiters = result[1::2] + ['']
  result = [v+d for v, d in zip(values, delimiters)] 
  print(result)

  text = r'abc 123 bsdf 223 jn 1123'
  result = re.findall(r'((\d)\2)', text)
  print(result)

  text = '''提取<span color='red'>自定义的</span>颜色
    可能出现在缩进块里, 可能有<font style='background:#def; font-size:1.5rem; color: #edb;'>不同的颜色定义</font>型式
# '''
  pat2 = r'(<(span|font)[^>]+?color ?(=|:) ?([\'\"]?).+?\4;?[^>]+?>.+?</ ?\2>)'

  result = re.findall(pat2, text)
  print(result)


# sample
def test_X_sample():
  sample = '''
xxxxxx
'''
  result = '''
xxxxxx
'''
  Polish(sample).text | should.eq(result)

