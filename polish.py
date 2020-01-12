


import re
import win32clipboard
import clipboard

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






