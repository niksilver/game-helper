import sys
sys.path.append('.')     # So that we can run this from the top directory

import os

outdir  = 'demos/out'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')


from   image_sheet     import ImageSheet
import card_maker_demo
from   card_maker_demo import base_maker


sheet = ImageSheet(card_width  = base_maker.width_px,    # Units are pixels
                   card_height = base_maker.height_px,
                   columns     = 6,
                   rows        = 2,
                   )

sheet.add(card_maker_demo.simple('One!'))
sheet.add(card_maker_demo.simple('Two!'))
# sheet.add(card_maker_demo.html('Oh, <i>hi</i>'))


outfile = outdir + '/demo.png'
sheet.save(outfile)
print(f'Output to {outfile}')

