from PIL import Image
from PIL import ImageFont
from card_maker import CardMaker


card_width  = 400
card_height = 560

assets_dir  = 'demos/assets'

font_file = '/usr/share/fonts/opentype/urw-base35/URWBookman-LightItalic.otf'
font = ImageFont.truetype(font = font_file,
                          size = 58,
                          )


def simple(wording, gutter):
    maker = CardMaker(width  = card_width,
                      height = card_height,
                      gutter = gutter,
                      )

    im = None
    if gutter == 0:
        im = Image.open(assets_dir + '/card-border-no-gutter.png')
    else:
        im = Image.open(assets_dir + '/card-border-with-gutter.png')
    im = im.resize(size = (card_width, card_height))

    maker.paste(im     = im,
                x_left = 0,
                y_top  = 0)
    maker.text(text     = wording,
               x_centre = maker.width / 2,
               y_middle = maker.height / 2,
               font     = font,
               )
    return maker.image()


def html(content):
    maker = CardMaker(width  = card_width,
                      height = card_height,
                      colour = (255, 255, 0, 255),
                      )
    maker.html(content,
               width_px  = 200,
               height_px = 300,
               )

    return maker.image()
