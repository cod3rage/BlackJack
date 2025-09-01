import services.interface as Ui
from configs.constants import *

class GuiManager():
  UiManager = Ui.UIObj(Ui.UIObj,'UIManager')
  UiMain    = Ui.UIObj(Ui.UIObj,'UIMain')    # camera shake
  UiOverlay = Ui.UIObj(Ui.UIObj,'UIOverlay') # no camera shake

  BindYeild = False

  amt = 20
  size  = 12
  for x in range(amt):
    x1 = (x - amt / 2) * size
    for y in range(amt):
      y1 = (y - amt / 2) * size
      B = UiMain.add(Ui.Button)
      A = UiOverlay.add(Ui.Button)
      #
      A.color    = (x / amt * 255, y / amt * 255, 255)
      A.size     = (size,size)
      A.position = (HALF_X + x1 + amt*size, HALF_Y + y1)
      B.color    = (y / amt * 255, x / amt * 255, 255 )
      B.size     = (size,size)
      B.position = (HALF_X + x1, HALF_Y + y1)

  def update(self, tick = 0, localTime = 0, scroll = (0,0), tick_cycle = 0):
    self.UiMain.update(tick, localTime, scroll, tick_cycle)
    self.UiOverlay.update(tick, localTime, (0,0), tick_cycle)
  
  def render(self, surface):
    self.UiMain.render(surface)
    self.UiOverlay.render(surface)
  
  def input(self, mouse_pos = (0,0), clicked = False, tick_cycle = 0):
    self.BindYeild = self.UiManager.input(mouse_pos, clicked, tick_cycle)