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


