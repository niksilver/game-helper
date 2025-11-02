import sys
sys.path.append('.')     # So that we can run this from the top directory

import os
from   image_sheet     import ImageSheet
import card_maker_demo
from   card_maker_demo import base_maker


outdir  = 'demos/out'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')


sheet = ImageSheet(card_width  = base_maker.width_px,    # Units are pixels
                   card_height = base_maker.height_px,
                   columns     = 6,
                   rows        = 2,
                   )

# For our first two cards we'll get them and extract the image,
# which exludes gutters.

sheet.add(card_maker_demo.simple('One!').image())
sheet.add(card_maker_demo.simple('Two!').image())
sheet.add(card_maker_demo.centred_text().image())

sheet.add(card_maker_demo.html().image())

sheet.add(card_maker_demo.bounding_box_demo().image())


outfile = outdir + '/demo.png'
sheet.save(outfile)
print(f'Output to {outfile}')

