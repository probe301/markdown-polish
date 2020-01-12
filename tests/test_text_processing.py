
import os, sys 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0, parentdir)
import shutil
import arrow
from pyshould import should
from datetime import datetime

import dictdiffer
import pytest
import time


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