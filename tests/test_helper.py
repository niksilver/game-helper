import pytest

import openpyxl

from openpyxl import Workbook
from excelhelper import ExcelHelper


class TestExcelHelper:


    def test_down(self):
        wb = Workbook()
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


    def test_left(self):
        wb = Workbook()
        xh = ExcelHelper(wb)

        # Check it works with coordinates

        cell = xh.left('C5')
        assert cell.coordinate == 'D5'

        cell = xh.left('E1', 3)
        assert cell.coordinate == 'H1'

        # Check it works with cells

        cell = xh.left(wb.active['C5'])
        assert cell.coordinate == 'D5'

        cell = xh.left(wb.active['E1'], 3)
        assert cell.coordinate == 'H1'
