import sys
import os
sys.path.append('.')     # So that we can run this from the top directory

from PIL                   import Image
from gamehelper.pdf_sheets import PDFSheets

import card_maker_demo
from   card_maker_demo import base_maker


outdir  = 'demos/out'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')


# In this case we choose not to the gutter size as originally
# set in the CardMaker. We could do, but it's a bit small.

pdf = PDFSheets(card_width  = base_maker.width_mm,
                card_height = base_maker.height_mm,
                gutter      = 3,    # Also mm
                # gutter      = base_maker.gutter_mm,    # Also mm
                )

pdf.add(card_maker_demo.simple('One!'),
        back_image_or_file = 'demos/assets/card-back.png',
        )
pdf.add(card_maker_demo.simple('Two!'),
        back_image_or_file = 'demos/assets/card-back.png',
        )
pdf.add(card_maker_demo.html(),
        back_image_or_file = 'demos/assets/card-back.png',
        )
pdf.add(card_maker_demo.text_positioning())
pdf.add(card_maker_demo.bounding_box_demo())
pdf.add(Image.open('demos/assets/womble.jpg'))    # This image bleeds into the gutters.
pdf.add('demos/assets/womble.jpg')                # We can use a filename instead.
pdf.add('demos/assets/womble.jpg',                # Scales to fit inside the gutters.
        x_offset = base_maker.gutter_mm,
        y_offset = base_maker.gutter_mm,
        )

pdf.add_backs_page()    # Only needed at the end


outdir  = 'demos/out'
outfile = outdir + '/demo.pdf'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')
pdf.output(outfile)
print(f'Output to {outfile}')
