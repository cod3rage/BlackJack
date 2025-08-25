import pygame
import deck, interface as gui, camera
from constants import *

class App:
  def __init__(self):
    self.initialize()  
    self.Running   = True
    self.screen    = pygame.display.set_mode(SCREEN_SIZE)
    self.clock     = pygame.time.Clock()
    self.LocalTime = 0
    self.deltaTime = 0
    # global offset
    self.scroll    = (0,0)
    self.mouse_pos = (0,0)
    self.clicks    = [-5,-5]
    #
    self.Gui  = gui.UIObj('Interface_Manager')

    # --- test
    SCALE = 100
    SIZE  = 5
    for x in range(SCALE):
      x1 = (x - SCALE / 2) * SIZE
      for y in range(SCALE):
        y1 = (y - SCALE / 2) * SIZE
        b = self.Gui.add(None,  gui.Button)
        #
        b.color    = (x / SCALE * 255, 255, y / SCALE * 255, )
        b.size     = (SIZE,SIZE)
        b.position = (HALF_X + x1, HALF_Y + y1)

    # --- test
    pygame.display.set_caption(APP_NAME)
    #
    self.deck = deck.Deck()
    self.hand = deck.Deck()
    self.deck.reset()

  #
  def initialize(self):
    pygame.init()
    pygame.font.init()

  def run(self):
    while self.Running:
      if self.keybinds():
        self.exit()
        break
      self.update()
      self.render()
      pygame.display.update()
      self.deltaTime =  self.clock.tick(FRAME_RATE) / 1000
      self.LocalTime += self.deltaTime

  # Main Functions #

  def keybinds(self):
    clicked = False
    #
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return True
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        clicked = True
    #
    self.mouse_pos = pygame.mouse.get_pos()
    if not self.Gui.input(self.mouse_pos, clicked):
      # game click
      pass

  # run 2 #
  def update(self):
    self.scroll = camera.update(
      *self.mouse_pos, 
      *self.scroll,
      self.deltaTime
    )
    # -
    self.Gui.update( 
      self.deltaTime, 
      self.LocalTime, 
      (-self.scroll[0], -self.scroll[1])
    )

  # run 3 #
  def render(self):
    self.screen.fill((0,0,0))
    self.Gui.render(self.screen)
    pygame.draw.circle(self.screen, (255,0,0), (HALF_X, HALF_Y), 2)
  
  # quit func #
  def exit(self):
    pygame.quit()
#


if __name__ == '__main__':
  Blackjack = App()
  Blackjack . run()