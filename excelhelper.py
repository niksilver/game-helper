import openpyxl

from openpyxl import Workbook


class ExcelHelper(object):


    def __init__(self, wb):
        self._wb = wb


    def cc(self, coordinate_or_cell):
        """
        Given a coordinate (string) or cell (object) return both the
        coordinate and the cell.
        """
        if type(coordinate_or_cell) is openpyxl.cell.cell.Cell:
            return (coordinate_or_cell.coordinate, coordinate_or_cell)
        else:
            return (coordinate_or_cell, self._wb.active[coordinate_or_cell])


    def down(self, coordinate_or_cell, count = 1):
        """
        Get the cell that is down one (or some other count) from the give cell
        in the active worksheet.
        """

        coord, cell = self.cc(coordinate_or_cell)
        return self._wb.active.cell(row = cell.row + count, column = cell.column)


    def left(self, coordinate_or_cell, count = 1):
        """
        Get the cell that is left one (or some other count) from the give cell
        in the active worksheet.
        """

        coord, cell = self.cc(coordinate_or_cell)
        return self._wb.active.cell(row = cell.row, column = cell.column + count)
