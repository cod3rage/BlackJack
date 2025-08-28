from interpolation import *

class TweenSys:
  anims = []
  #
  def new(self, obj:object, props:dict, time = 0, interpolation = linear):
    change_vector = {}

    for index in props:
      if not hasattr(obj, index): continue
      end, start = props[index], getattr(obj, index)
      if isinstance(end, (list, tuple, int, float)) and type(end) == type(start):
        change_vector[index] = (start, end)

    tween_object = {
      'anim'   : interpolation, # animation type include start, end and time
      'vecs'   : change_vector, # property to change as vector
      'obj'    : obj,       # reference
      'length' : max(time, 0.01), # total length of time
      'watch'  : 0,         # time tracker
    }

    self.anims.append(tween_object)
    return tween_object

  #
  def update(self, tick = 0):
    cache, i = [], -1
    for tween in self.anims:
      anim   = tween['anim']
      watch  = tween['watch']
      length = tween['length']
      vecs   = tween['vecs']
      obj    = tween['obj']
      i += 1
      tween['watch'] += tick
      scale  = min(watch/length, 1)

      if scale == 1:
        cache.append(i)

      for prop in vecs:
        start, end = vecs[prop]
        if isinstance(start, (int, float)):
          setattr(obj, prop, anim(start, end, scale))
        elif isinstance(start, (list, tuple)):
          final = []
          for i0, v0 in enumerate(end):
            final.append(anim(start[i0], v0, scale))
          if type(start) == tuple:
            final = tuple(final)
          setattr(obj, prop, final)

    self.anims = [item for index , item in enumerate(self.anims) if not (index in cache)]