from random import random as shake
from constants import *

def update(x, y, x1, y1, tick = 0):

    tick = min(1, tick * 2.5)

    x1 = round(x1 + ((x - HALF_X) / HALF_Y * SCROLL_AMT - x1) * tick + (shake() - .5) * SHAKE_STRENGTH, 2) 

    y1 = round(y1 + ((y - HALF_Y) / HALF_Y * SCROLL_AMT - y1) * tick + (shake() - .5) * SHAKE_STRENGTH, 2)
    
    return x1, y1