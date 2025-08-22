import pygame

class UIObj():
  def __init__(self, name = 'NONAME'):
    self.children = {}
    self.name     = name
  
  def __call__(self, child = ''):
    if child in self.children:
      return self.children[child]
  
  def update(self, tick = 0, localTime = 0):
    self.loop('update', tick, localTime)

  def render(self, surface):
    if surface:
      self.loop('render', surface)
    print(self.name, surface)
  
  def input(self):
    self.loop('input')

  def loop(self, call:str, *values:any):
    if not call: return
    for item in self.children.values():
      if hasattr(item, call):
        getattr(item, call)(*values)
  
  def add(self, name:str, obj:any = None):
    if not name:
      name = f'Frame-{len(self.children) + 1}'
    if not obj:
      obj = Frame(name)
    self.children[name] = obj
    return obj
  
#
class Frame(UIObj):
  def __init__(self, name=''):
    super().__init__(name)
    self.visible  = False
    self.position = (0,0)

  def update(self, tick = 0, localTime = 0):
    super().update(tick, localTime)
  
  def render(self, surface):
    super().render(surface)
  
  def input(self):
    super().input()

  def add(self, name):
    return super().add(name)
# ----
class UIManager(UIObj):
  def __init__(self, name = 'UIManager'):
    return super().__init__(name)
  
  def add(self, name):
    return super().add(name)
  
  def update(self, tick = 0, localTime = 0):
    super().update(tick, localTime)
  
  def render(self, surface):
    super().render(surface)
  
  def input(self):
    super().input()

