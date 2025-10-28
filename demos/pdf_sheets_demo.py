import sys
sys.path.append('.')     # So that we can run this from the top directory
sys.path.append('..')    # So that we can run this from this directory

from pdf_sheets import PDFSheets

"""
import card_images as cardims
from card_images import CardImages


gutter = 4

pdf = PDFSheets(card_width = 63,
                card_height = 88,
                gutter = gutter,
                )
pixels_per_mm = cardims.card_height / 63
cards = CardImages(gutter = gutter * pixels_per_mm)

for i in range(0, len(cardims.cards)):
    im = cards.image(i)
    pdf.add(im,
            x_offset = 0,
            y_offset = 0,
            back_image_or_file = 'assets/card-back.png',
            )

pdf.add_backs_page()
pdf.output('out/all-cards-printable.pdf')
"""
