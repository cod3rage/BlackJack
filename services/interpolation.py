from random import random
from configs.constants import *

def linear(start, end, time):
    return start + (end - start) * time
#-----------

def noise(shake_force):
    return (random() - .5 ) * shake_force
#
def cam_scroll(A, B, center, scroll_strength, tick = 0):
    return (B + ((A - center) / center * scroll_strength - B) * tick)
#
def cam_shake(x, y, x1, y1, tick = 0):
    tick = min(1, tick * 2.5)
    #
    x1 = round(cam_scroll(x, x1, HALF_X, SCROLL_AMT, tick) + noise(SHAKE_STRENGTH), 3)
    y1 = round(cam_scroll(y, y1, HALF_Y, SCROLL_AMT, tick) + noise(SHAKE_STRENGTH), 3)
    #
    return x1, y1


#