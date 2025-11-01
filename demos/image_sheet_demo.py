import sys
sys.path.append('.')     # So that we can run this from the top directory

import os

from image_sheet import ImageSheet
import card_maker_demo


outdir  = 'demos/out'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')


gutter = 0    # No gutter for image sheets

sheet = ImageSheet(card_width  = card_maker_demo.card_width_px,    # Units are pixels
                   card_height = card_maker_demo.card_height_px,
                   columns     = 6,
                   rows        = 2,
                   )

sheet.add(card_maker_demo.simple('One!', gutter))
sheet.add(card_maker_demo.simple('Two!', gutter))
sheet.add(card_maker_demo.html('Oh, <i>hi</i>'))


outfile = outdir + '/demo.png'
sheet.save(outfile)
print(f'Output to {outfile}')

