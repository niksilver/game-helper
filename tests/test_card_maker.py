import pytest

from PIL import Image

from gamehelper.card_maker import CardMaker


class TestCardMaker:


    def test_basically_runs(self):
        maker = CardMaker(width    = 250,
                          height   = 350,
                          unit     = 'px',
                          width_mm = 205,
                          )


    def test_convert_px_to_mm(self):

        # Low resolution
        maker1 = CardMaker(width  = 250,
                           height = 350,
                           gutter = 4,
                           unit   = 'px',
                           width_mm = 1000,    # 0.25mm per px, or 4px per mm
                           )
        assert maker1.width     == 250
        assert maker1.width_px  == 250
        assert maker1.width_mm  == 1000
        assert maker1.height    == 350
        assert maker1.height_px == 350
        assert maker1.height_mm == 1400
        assert maker1.gutter    == 4
        assert maker1.gutter_px == 4
        assert maker1.gutter_mm == 16

        assert maker1.width_with_gutters     == 4 + 250 + 4
        assert maker1.width_with_gutters_px  == 4 + 250 + 4
        assert maker1.width_with_gutters_mm  == 16 + 1000 + 16
        assert maker1.height_with_gutters    == 4 + 350 + 4
        assert maker1.height_with_gutters_px == 4 + 350 + 4
        assert maker1.height_with_gutters_mm == 16 + 1400 + 16

        # Higher resolution
        maker2 = CardMaker(width  = 1000,
                           height = 1200,
                           gutter = 2,
                           unit   = 'px',
                           width_mm = 500,    # 2mm per px, or 0.5px per mm
                           )
        assert maker2.width     == 1000
        assert maker2.width_px  == 1000
        assert maker2.width_mm  == 500
        assert maker2.height    == 1200
        assert maker2.height_px == 1200
        assert maker2.height_mm == 600
        assert maker2.gutter    == 2
        assert maker2.gutter_px == 2
        assert maker2.gutter_mm == 1

        assert maker2.width_with_gutters     == 2 + 1000 + 2
        assert maker2.width_with_gutters_px  == 2 + 1000 + 2
        assert maker2.width_with_gutters_mm  == 1 + 500 + 1
        assert maker2.height_with_gutters    == 2 + 1200 + 2
        assert maker2.height_with_gutters_px == 2 + 1200 + 2
        assert maker2.height_with_gutters_mm == 1 + 600 + 1

        # Floating point
        maker2 = CardMaker(width  = 1001,
                           height = 1201,
                           gutter = 3,
                           unit   = 'px',
                           width_mm = 500,    # 2.002mm per px, or 0.4995px per mm
                           )
        assert maker2.width     == 1001
        assert maker2.width_px  == 1001
        assert maker2.width_mm  == pytest.approx(500, abs = 0.01)
        assert maker2.height    == 1201
        assert maker2.height_px == 1201
        assert maker2.height_mm == pytest.approx(599.90, abs = 0.01)
        assert maker2.gutter    == 3
        assert maker2.gutter_px == 3
        assert maker2.gutter_mm == pytest.approx(1.499, abs = 0.01)


    def test_convert_mm_to_px(self):

        # Highish resolution
        maker1 = CardMaker(width  = 250,
                           height = 350,
                           gutter = 4,
                           unit   = 'mm',
                           width_px = 1000,    # 4px per mm, or 0.25mm per px
                           )
        assert maker1.width     == 250
        assert maker1.width_mm  == 250
        assert maker1.width_px  == 1000
        assert maker1.height    == 350
        assert maker1.height_mm == 350
        assert maker1.height_px == 1400
        assert maker1.gutter    == 4
        assert maker1.gutter_mm == 4
        assert maker1.gutter_px == 16


    def test_constructor_unit_combinations(self):

        # Must specify the unit

        with pytest.raises(ValueError, match = 'Must'):
            maker = CardMaker(width  = 250,
                              height = 350,
                              gutter = 4,
                              width_px = 1000,
                              )

        # Shouldn't be able to specify a nonsense unit

        with pytest.raises(ValueError, match = 'Unit'):
            maker = CardMaker(width  = 250,
                              height = 350,
                              gutter = 4,
                              unit   = '__',
                              width_px = 1000,
                              )

        # Must specify a width of either mm or px

        with pytest.raises(ValueError, match = 'Must'):
            maker = CardMaker(width  = 250,
                              height = 350,
                              gutter = 4,
                              unit   = 'mm',
                              )

        # Shouldn't be able to specify a width of px and mm

        with pytest.raises(ValueError, match = 'both'):
            maker = CardMaker(width  = 250,
                              height = 350,
                              gutter = 4,
                              unit   = 'mm',
                              width_px = 1000,
                              width_mm = 250,
                              )

        # Shouldn't be able to specify a width of px and unit of px

        with pytest.raises(ValueError, match = 'specify'):
            maker = CardMaker(width  = 250,
                              height = 350,
                              gutter = 4,
                              unit   = 'px',
                              width_px = 1000,
                              )

        # Shouldn't be able to specify a width of mm and unit of mm

        with pytest.raises(ValueError, match = 'specify'):
            maker = CardMaker(width  = 250,
                              height = 350,
                              gutter = 4,
                              unit   = 'mm',
                              width_mm = 1000,
                              )


    def test_image(self):

        # Image size when default units are px

        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           gutter = 2,
                           unit   = 'px',
                           width_mm = 500,    # 2px per mm, or 0.5mm per px
                           )
        # Gutters are excluded
        assert maker1.image().width  == 2 + 1000 + 2
        assert maker1.image().height == 2 + 1200 + 2


        # Image size when default units are mm

        maker2 = CardMaker(width  = 1000,
                           height = 1200,
                           gutter = 2,
                           unit   = 'mm',
                           width_px = 500,    # 2mm per px, or 0.5px per mm
                           )

        # Gutters are excluded
        px_per_mm = 0.5
        full_width_px  = (2 + 1000 + 2) * px_per_mm
        full_height_px = (2 + 1200 + 2) * px_per_mm

        assert maker2.image().width  == pytest.approx(full_width_px,  abs = 0.1)
        assert maker2.image().height == pytest.approx(full_height_px, abs = 0.1)


    def test_image(self):

        # Image size when default units are px

        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           gutter = 2,
                           unit   = 'px',
                           width_mm = 500,    # 2px per mm, or 0.5mm per px
                           )
        # Gutters are excluded
        assert maker1.image().width  == 1000
        assert maker1.image().height == 1200


        # Image size when default units are mm

        maker2 = CardMaker(width  = 1000,
                           height = 1200,
                           gutter = 2,
                           unit   = 'mm',
                           width_px = 500,    # 2mm per px, or 0.5px per mm
                           )

        # Gutters are excluded
        px_per_mm = 0.5
        full_width_px  = 1000 * px_per_mm
        full_height_px = 1200 * px_per_mm

        assert maker2.image().width  == pytest.approx(full_width_px,  abs = 0.1)
 

    def test_image_with_gutters(self):

        # Image size when default units are px

        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           gutter = 2,
                           unit   = 'px',
                           width_mm = 500,    # 2px per mm, or 0.5mm per px
                           )
        # Gutters are included
        assert maker1.image_with_gutters().width  == 2 + 1000 + 2
        assert maker1.image_with_gutters().height == 2 + 1200 + 2


        # Image size when default units are mm

        maker2 = CardMaker(width  = 1000,
                           height = 1200,
                           gutter = 2,
                           unit   = 'mm',
                           width_px = 500,    # 2mm per px, or 0.5px per mm
                           )

        # Gutters are included
        px_per_mm = 0.5
        full_width_px  = (2 + 1000 + 2) * px_per_mm
        full_height_px = (2 + 1200 + 2) * px_per_mm

        assert maker2.image_with_gutters().width  == pytest.approx(full_width_px,  abs = 0.1)
        assert maker2.image_with_gutters().height == pytest.approx(full_height_px, abs = 0.1)


    def test_to_px(self):

        # When default unit is px
        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           unit   = 'px',
                           width_mm = 500,    # 2px per mm, or 0.5mm per px
                           )
        assert maker1.to_px(1)    == 1
        assert maker1.to_px(10.5) == 10.5

        # When default unit is mm
        maker1 = CardMaker(width  = 500,
                           height = 600,
                           unit   = 'mm',
                           width_px = 1000,    # 0.5mm per px, or 2px per mm
                           )
        assert maker1.to_px(1)    == 2
        assert maker1.to_px(10.5) == 21

        # When default unit is mm and we need floating point
        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           unit   = 'mm',
                           width_px = 500,    # 2mm per px, or 0.5px per mm
                           )
        assert maker1.to_px(1)    == 0.5
        assert maker1.to_px(10.5) == 5.25

        # Handle None
        assert maker1.to_px(None) is None


    def test_to_mm(self):

        # When default unit is mm
        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           unit   = 'mm',
                           width_px = 500,    # 2mm per px, or 0.5px per mm
                           )
        assert maker1.to_mm(1)    == 1
        assert maker1.to_mm(10.5) == 10.5

        # When default unit is px
        maker1 = CardMaker(width  = 500,
                           height = 600,
                           unit   = 'px',
                           width_mm = 1000,    # 0.5px per mm, or 2mm per px
                           )
        assert maker1.to_mm(1)    == 2
        assert maker1.to_mm(10.5) == 21

        # When default unit is px and we need floating point
        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           unit   = 'px',
                           width_mm = 500,    # 2px per mm, or 0.5mm per px
                           )
        assert maker1.to_mm(1)    == 0.5
        assert maker1.to_mm(10.5) == 5.25

        # Handle None
        assert maker1.to_mm(None) is None


    def test_from_px(self):

        # When default unit is px
        maker1 = CardMaker(width  = 1000,
                           height = 1200,
                           unit   = 'px',
                           width_mm = 500,    # 2px per mm, or 0.5mm per px
                           )
        assert maker1.from_px(1)    == 1
        assert maker1.from_px(10.5) == 10.5

        # When default unit is mm
        maker2 = CardMaker(width  = 500,
                           height = 600,
                           unit   = 'mm',
                           width_px = 1000,    # 0.5mm per px, or 2px per mm
                           )
        assert maker2.from_px(1)    == 0.5
        assert maker2.from_px(10.5) == 5.25

        # Handle None
        assert maker2.from_px(None) is None


    def test_need_resize_px_with_px_maker(self):

        # Some arbitrary CardMaker using pixels
        # and a PNG image.

        px_maker = CardMaker(width  = 100,
                             height = 120,
                             unit   = 'px',
                             width_mm = 50,
                             )

        im = Image.open('tests/100x150.png')
        assert im.width  == 100
        assert im.height == 150

        # No resizing

        (flag, size) = px_maker.need_resize_px(im)

        assert flag == False
        assert size == (100, 150)

        (flag, size) = px_maker.need_resize_px(im, size = (100, 150))

        assert flag == False
        assert size == (100, 150)

        (flag, size) = px_maker.need_resize_px(im, width = 100)

        assert flag == False
        assert size == (100, 150)

        (flag, size) = px_maker.need_resize_px(im, height = 150)

        assert flag == False
        assert size == (100, 150)

        # Some resizing

        (flag, size) = px_maker.need_resize_px(im, size = (150, 200))

        assert flag == True
        assert size == (150, 200)

        (flag, size) = px_maker.need_resize_px(im, width = 150, height = 200)

        assert flag == True
        assert size == (150, 200)

        (flag, size) = px_maker.need_resize_px(im, width = 150)

        assert flag == True
        assert size == (150, 225)

        (flag, size) = px_maker.need_resize_px(im, height = 300)

        assert flag == True
        assert size == (200, 300)

        # Returned size should use ints

        (flag, size) = px_maker.need_resize_px(im, width = 1)    # 1/100

        assert flag == True
        assert size == (1, 1)

        (flag, size) = px_maker.need_resize_px(im, height = 50)    # One third

        assert flag == True
        assert size == (33, 50)


    def test_need_resize_px_with_mm_maker(self):

        # Some arbitrary CardMaker using millimetres
        # and a PNG image.

        mm_maker = CardMaker(width  = 50,
                             height = 60,
                             unit   = 'mm',
                             width_px = 100,    # 2px = 1mm
                             )

        im = Image.open('tests/100x150.png')
        assert im.width  == 100
        assert im.height == 150

        # No resizing - dimensions in mm

        (flag, size_px) = mm_maker.need_resize_px(im)

        assert flag    == False
        assert size_px == (100, 150)

        (flag, size_px) = mm_maker.need_resize_px(im, size = (50, 75))

        assert flag    == False
        assert size_px == (100, 150)

        (flag, size_px) = mm_maker.need_resize_px(im, width = 50)

        assert flag    == False
        assert size_px == (100, 150)

        (flag, size_px) = mm_maker.need_resize_px(im, height = 75)

        assert flag    == False
        assert size_px == (100, 150)

        # Shouldn't resize if new dimensions are almost the same

        (flag, size_px) = mm_maker.need_resize_px(im)

        assert flag    == False
        assert size_px == (100, 150)

        (flag, size_px) = mm_maker.need_resize_px(im, size = (50.1, 75.1))

        assert flag    == False
        assert size_px == (100, 150)

        (flag, size_px) = mm_maker.need_resize_px(im, width = 50.1)

        assert flag    == False
        assert size_px == (100, 150)

        (flag, size_px) = mm_maker.need_resize_px(im, height = 75.1)

        assert flag    == False
        assert size_px == (100, 150)

        # Some resizing

        (flag, size_px) = mm_maker.need_resize_px(im, size = (75, 100))

        assert flag    == True
        assert size_px == (150, 200)

        (flag, size_px) = mm_maker.need_resize_px(im, width = 75, height = 100)

        assert flag    == True
        assert size_px == (150, 200)

        (flag, size) = mm_maker.need_resize_px(im, width = 75)

        assert flag    == True
        assert size_px == (150, 200)

        (flag, size_px) = mm_maker.need_resize_px(im, height = 150)

        assert flag    == True
        assert size_px == (200, 300)


    def test_load_image_px_maker(self):

        # Some arbitrary CardMaker using pixels
        # and an SVG image.

        px_maker = CardMaker(width  = 100,
                             height = 120,
                             unit   = 'px',
                             width_mm = 50,
                             )

        # No resizing

        im2 = px_maker.load_image('tests/123x82.svg')

        assert im2.width  == 123
        assert im2.height == 82

        # Some resizing

        im2 = px_maker.load_image('tests/123x82.svg', width = 100)

        assert im2.width  == 100
        assert im2.height == int(82 / (123/100))


    def test_load_image_mm_maker(self):

        # Some arbitrary CardMaker using pixels
        # and an SVG image.

        px_maker = CardMaker(width    = 70,
                             height   = 70,
                             unit     = 'mm',
                             width_px = 100,    # 70mm = 100px
                             )

        # No resizing

        im2 = px_maker.load_image('tests/123x82.svg')

        assert im2.width  == 123
        assert im2.height == 82

        # Some resizing

        im2 = px_maker.load_image('tests/123x82.svg', width = 70)    # mm

        assert im2.width  == 100                    # Image is in px
        assert im2.height == int(82 / (123/100))    # Image is in px


    def test_load_image_resize_bug(self):

        # Some arbitrary CardMaker using pixels
        # and an SVG image.

        mm_maker = CardMaker(width    = 70,
                             height   = 70,
                             unit     = 'mm',
                             width_px = 150,    # 70mm = 100px
                             )

        im = mm_maker.load_image('tests/100x150.png', width = 70)    # mm

        assert im.width  == 150
        assert im.height == 225


    def test_paste_requires_correct_arguments(self):

        # When default unit is px
        maker = CardMaker(width  = 1000,
                          height = 1200,
                          unit   = 'px',
                          width_mm = 500,    # 2px per mm, or 0.5mm per px
                          )

        # Needs exactly one x argument

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png')
        assert 'one of x_left, x_centre, x_right' in valerr.value.args[0]

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png',
                             x_left   = 0,
                             x_centre = 0,
                             y_top    = 0,
                             )
        assert 'one of x_left, x_centre, x_right' in valerr.value.args[0]

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png',
                             x_centre = 0,
                             x_right  = 0,
                             y_top    = 0,
                             )
        assert 'one of x_left, x_centre, x_right' in valerr.value.args[0]

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png',
                             x_left   = 0,
                             x_centre = 0,
                             x_right  = 0,
                             y_top    = 0,
                             )
        assert 'one of x_left, x_centre, x_right' in valerr.value.args[0]

        im = maker.paste('tests/100x150.png', x_left   = 0, y_top = 0)    # Okay
        im = maker.paste('tests/100x150.png', x_centre = 0, y_top = 0)    # Okay
        im = maker.paste('tests/100x150.png', x_right  = 0, y_top = 0)    # Okay

        # Needs exactly one y argument

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png', x_left = 0)
        assert 'one of y_top, y_middle, y_bottom' in valerr.value.args[0]

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png',
                             x_left   = 0,
                             y_top    = 0,
                             y_middle = 0,
                             )
        assert 'one of y_top, y_middle, y_bottom' in valerr.value.args[0]

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png',
                             x_left   = 0,
                             y_middle = 0,
                             y_bottom = 0,
                             )
        assert 'one of y_top, y_middle, y_bottom' in valerr.value.args[0]

        with pytest.raises(ValueError) as valerr:
            im = maker.paste('tests/100x150.png',
                             x_left   = 0,
                             y_top    = 0,
                             y_middle = 0,
                             y_bottom = 0,
                             )
        assert 'one of y_top, y_middle, y_bottom' in valerr.value.args[0]

        im = maker.paste('tests/100x150.png', x_left = 0, y_top    = 0)    # Okay
        im = maker.paste('tests/100x150.png', x_left = 0, y_middle = 0)    # Okay
        im = maker.paste('tests/100x150.png', x_left = 0, y_bottom = 0)    # Okay


class TestTextLineSpacing:
    """Tests for text_line_spacing properties."""

    def test_default_value_mm_unit(self):
        """Default text_line_spacing should be 1.5mm when unit is mm."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,
                          )
        assert maker.text_line_spacing    == 1.5
        assert maker.text_line_spacing_mm == 1.5
        assert maker.text_line_spacing_px == 3  # 2px per mm

    def test_default_value_px_unit(self):
        """Default text_line_spacing should be equivalent to 1.5mm when unit is px."""
        maker = CardMaker(width    = 200,
                          height   = 200,
                          unit     = 'px',
                          width_mm = 100,  # 2px per mm
                          )
        assert maker.text_line_spacing    == 3  # 1.5mm * 2px/mm
        assert maker.text_line_spacing_mm == 1.5
        assert maker.text_line_spacing_px == 3

    def test_set_text_line_spacing_mm_unit(self):
        """Setting text_line_spacing when unit is mm."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,  # 2px per mm
                          )
        maker.text_line_spacing = 3
        assert maker.text_line_spacing    == 3
        assert maker.text_line_spacing_mm == 3
        assert maker.text_line_spacing_px == 6

    def test_set_text_line_spacing_px_unit(self):
        """Setting text_line_spacing when unit is px."""
        maker = CardMaker(width    = 200,
                          height   = 200,
                          unit     = 'px',
                          width_mm = 100,  # 2px per mm
                          )
        maker.text_line_spacing = 6
        assert maker.text_line_spacing    == 6
        assert maker.text_line_spacing_mm == 3
        assert maker.text_line_spacing_px == 6

    def test_set_text_line_spacing_mm(self):
        """Setting text_line_spacing_mm should update all properties."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,  # 2px per mm
                          )
        maker.text_line_spacing_mm = 4
        assert maker.text_line_spacing    == 4
        assert maker.text_line_spacing_mm == 4
        assert maker.text_line_spacing_px == 8

    def test_set_text_line_spacing_px(self):
        """Setting text_line_spacing_px should update all properties."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,  # 2px per mm
                          )
        maker.text_line_spacing_px = 10
        assert maker.text_line_spacing    == 5
        assert maker.text_line_spacing_mm == 5
        assert maker.text_line_spacing_px == 10

    def test_set_to_none_reverts_to_default(self):
        """Setting text_line_spacing to None reverts to 1.5mm equivalent."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,  # 2px per mm
                          )
        maker.text_line_spacing = 5
        assert maker.text_line_spacing == 5

        maker.text_line_spacing = None
        assert maker.text_line_spacing    == 1.5
        assert maker.text_line_spacing_mm == 1.5
        assert maker.text_line_spacing_px == 3

    def test_set_mm_to_none_reverts_to_default(self):
        """Setting text_line_spacing_mm to None reverts to 1.5mm."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,  # 2px per mm
                          )
        maker.text_line_spacing_mm = 5
        assert maker.text_line_spacing    == 5
        assert maker.text_line_spacing_mm == 5
        assert maker.text_line_spacing_px == 10

        maker.text_line_spacing_mm = None
        assert maker.text_line_spacing    == 1.5
        assert maker.text_line_spacing_mm == 1.5
        assert maker.text_line_spacing_px == 3

    def test_set_px_to_none_reverts_to_default(self):
        """Setting text_line_spacing_px to None reverts to 1.5mm equivalent."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,  # 2px per mm
                          )
        maker.text_line_spacing_px = 10
        assert maker.text_line_spacing    == 5
        assert maker.text_line_spacing_mm == 5
        assert maker.text_line_spacing_px == 10

        maker.text_line_spacing_px = None
        assert maker.text_line_spacing    == 1.5
        assert maker.text_line_spacing_mm == 1.5
        assert maker.text_line_spacing_px == 3
