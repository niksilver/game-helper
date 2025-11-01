if __name__ == '__main__':
    print("This is a module, not a standalone script")
    import sys
    sys.exit(0)


from PIL import Image
from PIL import ImageFont
from card_maker import CardMaker


assets_dir  = 'demos/assets'

font_file = '/usr/share/fonts/opentype/urw-base35/URWBookman-LightItalic.otf'
font = ImageFont.truetype(font = font_file,
                          size = 58,
                          )

base_maker = CardMaker(width    = 400,
                       height   = 500,
                       gutter   = 10,
                       unit     = 'px',
                       width_mm = 40,
                       )


def simple(wording):
    maker = base_maker.copy()

    border_im = Image.open(assets_dir + '/card-border-with-gutter.png')
    border_im = border_im.resize(size = maker.size_with_gutters_px)

    maker.paste(im     = border_im,
                x_left = 0,
                y_top  = 0)
    maker.text(text     = wording,
               x_centre = maker.width / 2,
               y_middle = maker.height / 2,
               font     = font,
               )
    return maker.image()


def html(content):
    maker = CardMaker(width  = card_width_px,
                      height = card_height_px,
                      unit     = 'px',
                      width_mm = card_width_mm,
                      colour = (255, 255, 0, 255),
                      )
    maker.html(content,
               width_px  = 200,
               height_px = 300,
               )

    return maker.image()
