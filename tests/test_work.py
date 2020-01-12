
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


def test_1_work_update_image_url():
  p = Polish.from_clipboard()
  p.update_image_url(prefix='Awesome-Chrome-插件集锦.')
  print(p.text)
  p.to_clipboard()


def test_2_work_join_markdown_link():
  p = Polish.from_clipboard()
  p.join_markdown_link()
  print(p.text)
  p.to_clipboard()


