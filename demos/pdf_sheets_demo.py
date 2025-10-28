import sys
sys.path.append('.')     # So that we can run this from the top directory

import os

from pdf_sheets import PDFSheets
import card_maker_demo


gutter = 4

pdf = PDFSheets(card_width  = 63,    # Units are mm
                card_height = 88,
                gutter      = gutter,
                )

pdf.add(card_maker_demo.simple(gutter),
        back_image_or_file = 'demos/assets/card-back.png',
        )

pdf.add_backs_page()


outdir  = 'demos/out'
outfile = outdir + '/demo.pdf'
if not(os.path.exists(outdir)):
    os.mkdir('demos/out')
pdf.output(outfile)
print(f'Output to {outfile}')
