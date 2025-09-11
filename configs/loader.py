from pygame import image

CARDS  = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
SHAPES = ['Spade','Heart','Club','Diamond']

assets = {
  'Cards':{
  },
  'Realism':{
    'CarryBack':None,
    'CarryFront':None,
    'FistBack':None,
    'FistFront':None,
  },
  'Icons':{
    'Clock':None,
    'Heart':None,
    'Lmb_icon':None,
    'Rmb_icon':None,
    'Star':None,
    'twenty-one-icon':None,
    'Warning':None,
  },
}

def load():
  for shp in range(len(SHAPES)):
    for crd in range(len(CARDS)):
      assets['Cards'][f'{CARDS[crd]}_of_{SHAPES[shp]}s'.lower()] = None

  for group_name, group in assets.items():
    for asset_name in group:
      group[asset_name] = image.load(f'assets/{group_name}/{asset_name}.png')

load()