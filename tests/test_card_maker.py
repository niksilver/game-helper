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
        maker1 = CardMaker(width  = 250,
                           height = 350,
                           gutter = 4,
                           unit   = 'px',
                           width_mm = 1000,    # 0.25px per mm, or 4px per mm
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

