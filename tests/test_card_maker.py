import pytest

from card_maker import CardMaker


class TestCardMaker:


    def test_basically_runs(self):
        maker = CardMaker(width    = 250,
                          height   = 350,
                          width_mm = 205,
                          )

        """
        xh = ExcelHelper(wb)

        # Check it works with coordinates

        cell = xh.down('C5')
        assert cell.coordinate == 'C6'

        cell = xh.down('E1', 3)
        assert cell.coordinate == 'E4'

        # Check it works with cells

        cell = xh.down(wb.active['C5'])
        assert cell.coordinate == 'C6'

        cell = xh.down(wb.active['E1'], 3)
        assert cell.coordinate == 'E4'

        """

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

