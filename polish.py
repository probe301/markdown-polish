


import re
import win32clipboard
import clipboard

from tag import extract_tags
import pangu

import enum  

BlockType = enum.Enum('BlockType', ('p', 
                                    'title',   
                                    'fencecode',    
                                    'sepline',  
                                    'indent', 
                                    'admonition', 
                                    'table', 
                                    'list', 
                                    'quote', 
                                    'frontmatter'
                     ))


class Polish:
  def __init__(self, text):
    self.text = text
    self.source = text

  @classmethod
  def from_clipboard(cls):
    text = clipboard.paste()
    return cls(text)

  def to_clipboard(self):
    clipboard.copy(self.text)
    return self

  def join_markdown_link(self):
    t = re.sub(r'\n\[\n{1,4}(.+)\n{1,6}\]\((https?://.+?)\)', 
               r'\n[\1](\2)', 
               self.text)
    self.text = t
    return self

  def update_image_url(self, prefix=None, replacer=None):

    if replacer:
      self._replace(r'!\[(.*?)\]\((.+?)\)', replacer)
    else:
      self._replace(r'!\[(.*?)\]\((.+?)\)',  r'![\1](' + prefix + r'\2)')

    return self

  def _replace(self, pat, repl):
    self.text = re.sub(pat, repl, self.text)



  def _tag_markdown_blocks(self, lines):
    '''
    单行 tag: title p sepline...
    多行 tag: quote indent admonition fencecode frontmatter...
    fencecode frontmatter 通过结束符关闭
    quote indent admonition 自行关闭
    '''
    last_blocktype = None
    for line, farseer in zip(lines, lines[1:] + ['']): # farseer 前瞻一行
      
      if last_blocktype is BlockType.fencecode:
        yield BlockType.fencecode
        if line.startswith('```'):
          last_blocktype = None
      elif last_blocktype is BlockType.frontmatter:
        yield BlockType.frontmatter
        if line.strip() == '---':
          last_blocktype = None
      elif last_blocktype is BlockType.admonition and line.startswith('    '):
        yield BlockType.admonition
      elif line.strip() == '' and last_blocktype in (BlockType.admonition, BlockType.indent, BlockType.quote):
        yield last_blocktype

      elif line.startswith('```'):
        last_blocktype = BlockType.fencecode
        yield BlockType.fencecode
      elif line.startswith('    '):
        last_blocktype = BlockType.indent
        yield BlockType.indent
      elif line.strip() == '---':
        last_blocktype = BlockType.frontmatter
        yield BlockType.frontmatter
      elif line.startswith('!!! '):
        last_blocktype = BlockType.admonition
        yield BlockType.admonition
      elif line.startswith('>'):
        last_blocktype = BlockType.quote
        yield BlockType.quote

      else:
        if line.startswith('#'):
          yield BlockType.title
        elif line.startswith((r'----', r'\----', r'====', r'\====', r'\=\=\=\=')):
          yield BlockType.sepline
        else:
          yield BlockType.p

  # end def _tag_markdown_blocks


  def _split_markdown_blocks(self, text):
    '''
    单行 tag: title p sepline...
    多行 tag: quote indent admonition fencecode frontmatter...

    聚合相同的多行 tag
    '''
    lines = self._sep_split(text.strip(), sep=r"([\n]+)")
    tags = list(self._tag_markdown_blocks(lines))

    block_cache = ''

    for tag, next_tag, line in zip(tags, tags[1:] + [None], lines):
      # print(tag, line)
      if tag in (BlockType.title, BlockType.p, BlockType.sepline):
        yield tag, line
        block_cache = ''
      elif tag == next_tag:
        block_cache += line
      else:
        block_cache += line
        yield tag, block_cache
        block_cache = ''

  # end def _split_markdown_blocks




  def _sep_split(self, text, sep=r"([.。!！?？\n]+)"):
    result = re.split(sep, text)
    values = result[::2]
    delimiters = result[1::2] + ['']
    return [v+d for v, d in zip(values, delimiters)]



  def extract_tags(self, n=10):
    return extract_tags(self.text, topK=n)


  def pangu_spacing(self):
    self.text = pangu.spacing_text(self.text)
    return self

  def transword(self):
    transdict = { '显示': '显式',
                  '登陆': '登录',
                  '稍后': '稍候',
                  '（': '(',
                  '）': ')',
                  '“': '"',
                  '”': '"',}
    for k, v in transdict.items():
      self.text = self.text.replace(k, v)
    return self



  def extract_outline(self, headers='h1,h2,h3'):

    lines = self._split_markdown_blocks(self.text)
    result = []
    header_pat = tuple('#'*int(h[1])+' ' for h in headers.split(','))

    for kind, line in lines:
      if kind == BlockType.title and line.startswith(header_pat):
        result.append(line.strip())
    return result




  def extract_highlights(self):
    '''针对行内高亮, 非块级元素'''
    result = []
    highlight_pat1 = r'(==(.+?)==)'
    highlight_pat2 = r'(<(span|font)[^>]+?color ?(=|:) ?([\'\"]?).+?\4;?[^>]+?>.+?</ ?\2>)'

    for kind, line in self._split_markdown_blocks(self.text):
      if kind in (BlockType.fencecode, BlockType.sepline):
        continue
      else:
        for m in re.findall(highlight_pat1, line):
          result.append(('highlight', m[0]))

        for m in re.findall(highlight_pat2, line):
          result.append(('highlight', m[0]))

    return result


  def extract_annotations(self):
    '''针对块级注释'''
    result = []

    for kind, block in self._split_markdown_blocks(self.text):
      # print(kind, block)
      if kind in (BlockType.admonition, ):
        result.append(('annotation', block))
    return result
