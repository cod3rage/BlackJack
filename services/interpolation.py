from random import random
from configs.constants import *

def linear(start, end, time):
    return start + (end - start) * time
#-----------

def shake(A, B, center, shake_force, scroll_strength, tick):
    return round((B + ((A - center) / center * scroll_strength - B) * tick) + (random() - 0.5 * shake_force), 2)
#
def cam_shake(x, y, x1, y1, tick = 0):
    tick = min(1, tick * 2.5)
    #
    x1 = shake(x, x1, HALF_X, SHAKE_STRENGTH, SCROLL_AMT, tick)
    y1 = shake(y, y1, HALF_Y, SHAKE_STRENGTH, SCROLL_AMT, tick)
    #
    return x1, y1
#