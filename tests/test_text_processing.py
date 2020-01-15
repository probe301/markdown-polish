
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




def test_6_pangu_spacing_level2():
  # 需要能保留 `` 内部结构
  sample = '''那么`SelectLeftSpaceChar()`这个函数的作用,就是用来选中这个多余的空格. 在选中这个多余的空格之后'''
  result = '''那么 `SelectLeftSpaceChar()` 这个函数的作用，就是用来选中这个多余的空格。在选中这个多余的空格之后'''
  Polish(sample).pangu_spacing().text.strip() | should.eq(result.strip())

  sample = '當你,凝視著bug,bug也凝視著你'
  result = '當你，凝視著 bug, bug 也凝視著你'





# sample
def test_X_sample():
  sample = '''
xxxxxx
'''
  result = '''
xxxxxx
'''
  Polish(sample).xxxxx().text | should.eq(result)

