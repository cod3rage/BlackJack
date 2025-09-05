import services.interface as Ui
from configs.constants import *

class GuiManager():
  UiManager = Ui.UIObj(Ui.UIObj,'UIManager')
  UiMain    = Ui.UIObj(Ui.UIObj,'UIMain')    # camera shake
  UiOverlay = Ui.UIObj(Ui.UIObj,'UIOverlay') # no camera shake
  BindYeild = False

  def update(self, tick = 0, localTime = 0, scroll = (0,0), tick_cycle = 0):
    self.UiMain.update(tick, localTime, scroll, tick_cycle)
    self.UiOverlay.update(tick, localTime, (0,0), tick_cycle)
  
  def render(self, surface):
    self.UiMain.render(surface)
    self.UiOverlay.render(surface)
  
  def input(self, mouse_pos = (0,0), clicked = False, tick_cycle = 0):
    self.BindYeild = self.UiManager.input(mouse_pos, clicked, tick_cycle)

  # -----------[   GAME INTERFACE   ]------------ #

  ply_bttn = UiMain.add(Ui.Button, 'PlayButton')
  ply_bttn.size  = (160, 40)
  ply_bttn.color = (255, 255, 255)
  ply_bttn.position = (HALF_X - 80, SCREEN_Y - 170)

  sttn_bttn = UiMain.add(Ui.Button, 'SettingsButton')
  sttn_bttn.size  = (130, 30)
  sttn_bttn.color = (255, 255, 255)
  sttn_bttn.position = (HALF_X - 65, SCREEN_Y - 115)

  #


  # -----------[   GAME INTERFACE   ]------------ #