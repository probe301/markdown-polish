


import re
import win32clipboard
import clipboard

from tag import extract_tags
import pangu
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

  def _split_markdown_lines(self, text):
    in_code_block = False
    code_block = ''
    quote_block = ''
    indent_block = ''
    for line in self._sep_split(text, sep=r"([\n]+)"):
      if line.startswith('```'):
        in_code_block = not(in_code_block)
        code_block += line
        if in_code_block:
          if quote_block: 
            yield 'quote', quote_block
            quote_block = ''
          if indent_block: 
            yield 'indent', indent_block
            indent_block = ''
        else:
          yield 'code', code_block
          code_block = ''
      elif in_code_block:
        code_block += line
      elif line.startswith('>'):
        quote_block += line
      elif line.startswith('    '):
        indent_block += line

      else: 
        if quote_block: 
          yield 'quote', quote_block
          quote_block = ''
        if indent_block: 
          yield 'indent', indent_block
          indent_block = ''

        # switch single line
        if line.startswith('#'):
          yield 'title', line
        elif line.startswith('----'):
          yield 'sep', line
        else:
          yield 'paragraph', line
          



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

    lines = self._split_markdown_lines(self.text)
    result = []
    header_pat = tuple('#'*int(h[1])+' ' for h in headers.split(','))

    for kind, line in lines:
      if kind == 'title' and line.startswith(header_pat):
        result.append(line.strip())
    return result




  def extract_notes(self, highlight=True, annotation=True):
    result = []
    highlight_pat1 = r'(==(.+?)==)'
    highlight_pat2 = r'(<(span|font)[^>]+?color ?(=|:) ?([\'\"]?).+?\4;?[^>]+?>.+?</ ?\2>)'

    lines = self._split_markdown_lines(self.text)
    for kind, line in lines:
      if kind in ('title', 'code', 'sep'):
        continue
      else:
        for m in re.findall(highlight_pat1, line):
          result.append(('highlight', m[0]))

        for m in re.findall(highlight_pat2, line):
          result.append(('highlight', m[0]))

    return result


