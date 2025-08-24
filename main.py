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
    self.Gui = gui.UIObj('Interface_Manager')
    #test
    b = self.Gui.add('hello',gui.Frame)
    b.color = 'red'
    b.size  = (20,20)
    b.position = (HALF_X,HALF_Y)
    #
    pygame.display.set_caption(APP_NAME)
    #
    self.deck = deck.Deck()

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
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return True
      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          if self.LocalTime - self.clicks[0] <= DOUBLE_CLICK:
            print('lmb x2')
          self.clicks[0] = self.LocalTime
        if event.button == 3:
          if self.LocalTime - self.clicks[1] <= DOUBLE_CLICK:
            print('rmb x2')
          self.clicks[1] = self.LocalTime

    
    self.mouse_pos = pygame.mouse.get_pos()
    self.Gui.input()

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
  
  # quit func #
  def exit(self):
    pygame.quit()
#


if __name__ == '__main__':
  Blackjack = App()
  Blackjack . run()