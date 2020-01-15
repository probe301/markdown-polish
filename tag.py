


import re
import os

import jieba.analyse



def text_load(path, encoding=None):
  ''' 读取文本, 尝试不同的解码 '''
  if not os.path.exists(path):
    raise ValueError("path `{}` not exist".format(path))
  if encoding is None:  # 猜测 encoding
    try:
      open(path, 'r', encoding='utf-8').read()
      encoding = 'utf-8'
    except UnicodeDecodeError:
      encoding = 'gbk'
  with open(path, 'r', encoding=encoding) as f:
    ret = f.read()
  return ret
def text_save(path, data, encoding='utf-8'):
  with open(path, 'w', encoding=encoding) as f:
    f.write(data)
  return True

# FOLDER = r'D:\TodoSwap\我的坚果云\Evernote-md\\'

# texts = [ 'Social Notes\历史上俄罗斯和克里米亚的关系是怎样的-俄罗斯为什么这么重视克里米亚-知乎.md',
#           'CSharp LINQ Tips - 一起学习一点微小的 Linq 技巧.md',
#           'Game Notes\泰拉瑞亚相对来说比较简单好懂的对新手友好的上手指南 - 四川担担面酱的专栏 老妈子式念念叨叨的游戏攻略及相谈.md',
#           'Chrome Tools Notes\Awesome-Chrome-插件集锦.md',
#           'Network Notes\GET 和 POST 到底有什么区别？.md',
# ]
# for line in texts:
#   text = text_load(FOLDER + line)
#   tags = jieba.analyse.extract_tags(text, topK=20)
#   print(line)
#   print('TF-IDF:  ', ', '.join(tags))
#   tags = jieba.analyse.textrank(text, topK=20)
#   print('TextRank:', ', '.join(tags))
#   print()



# for line in texts:
#   text = text_load(FOLDER + line)
#   tags = jieba.analyse.extract_tags(text, topK=20)
#   print(line)
#   print('TF-IDF:  ', ', '.join(tags))
#   tags = jieba.analyse.textrank(text, topK=20)
#   print('TextRank:', ', '.join(tags))
#   print()


def extract_tags(text, topK=20):
  result = {}

  jieba.analyse.set_idf_path("idf.txt")
  tags = jieba.analyse.extract_tags(text, topK=20)
  result['idf.txt,tf-idf'] = tags
  tags = jieba.analyse.textrank(text, topK=20)
  result['idf.txt,textrank'] = tags

  jieba.analyse.set_idf_path("idf.txt.big.txt")
  tags = jieba.analyse.extract_tags(text, topK=20)
  result['idf.big,tf-idf'] = tags
  tags = jieba.analyse.textrank(text, topK=20)
  result['idf.big,textrank'] = tags

  return result