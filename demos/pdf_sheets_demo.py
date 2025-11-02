import sys
sys.path.append('.')     # So that we can run this from the top directory

import os
from   pdf_sheets      import PDFSheets
import card_maker_demo
from   card_maker_demo import base_maker


outdir  = 'demos/out'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')


# In this case we choose not to the gutter size as originally
# set in the CardMaker. We could do, but it's a bit small.

pdf = PDFSheets(card_width  = base_maker.width_with_gutters_mm,
                card_height = base_maker.height_with_gutters_mm,
                gutter      = 3,    # Also mm
                )

pdf.add(card_maker_demo.simple('One!').image_with_gutters(),
        back_image_or_file = 'demos/assets/card-back.png',
        )
pdf.add(card_maker_demo.simple('Two!').image_with_gutters(),
        back_image_or_file = 'demos/assets/card-back.png',
        )
pdf.add(card_maker_demo.html().image_with_gutters(),
        back_image_or_file = 'demos/assets/card-back.png',
        )

pdf.add_backs_page()    # Only needed at the end


outdir  = 'demos/out'
outfile = outdir + '/demo.pdf'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')
pdf.output(outfile)
print(f'Output to {outfile}')
