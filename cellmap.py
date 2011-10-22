#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cell, CellMap
"""


class Cell(object):
    """It keeps status alive or dead and next generation status.
    """
    def __init__(self, alive=False):
        """
        Arguments:
            alive -- dead or alive flag(True: alive, False: dead)
        """
        self.alive = alive
        self.next = False

    def set_alive(self, alive):
        """Modifies the status
        Arguments:
            alive -- dead or alive flag(True: alive, False: dead)
        """
        self.alive = alive

    def calc_next(self, cells):
        """Calculate next generation.
        Arguments:
            cells -- around cell list
        """
        count = 0
        for cell in cells:
            if cell.is_alive():
                count += 1

        if self.alive == False:
            if count == 3:
                self.next = True
            else:
                self.next = False
        else:
            if count <= 1 or count >= 4:
                self.next = False
            else:
                self.next = True

    def change_next(self):
        """Change next generation.
        """
        self.alive = self.next

    def is_alive(self):
        """Return true if alive, false otherwise.
        Returns:
            alive -- dead or alive flag(True: alive, False: dead)
        """
        return self.alive


class CellMap(object):
    """It keeps cells and have way to access them.
    """
    def __init__(self, width, height):
        """
        Arguments:
            width -- map width
            height -- map height
        """
        self.width = width
        self.height = height
        self.dummy = Cell(False)
        self.cells = []
        for i in range(self.width * self.height):
            self.cells.append(Cell())

    def set_all(self, alive):
        """It set all cell status.
        Arguments:
            alive -- True: alive, False: dead
        """
        for i in range(self.width * self.height):
            self.cells[i].set_alive(alive)

    def is_contain(self, x, y):
        """Return true if map contains the given position, false otherwise.
        Arguments:
            x -- map coordinate
            y -- map coordinate
        Retuens:
            flag -- True: contain, False: not contain
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True

    def get(self, x, y):
        """Returns the cell at the given position.
        Arguments:
            x -- map coordinate
            y -- map coordinate
        Retuens:
            cell -- Cell object
        """
        if self.is_contain(x, y):
            return self.cells[y * self.width + x]
        else:
            return self.dummy

    def set_alive(self, x, y, alive):
        """Modifies the cell status at the given position.
        Arguments:
            x -- map coordinate
            y -- map coordinate
            alive -- True: alive, False: dead
        """
        if self.is_contain(x, y):
            cell = self.get(x, y)
            cell.set_alive(alive)

    def get_around(self, x, y):
        """Returns cells around the given position.
        Arguments:
            x -- map coordinate
            y -- map coordinate
        Returns:
            cells -- around cell list
        """
        cells = []
        for cy in range(y - 1, y + 2):
            for cx in range(x - 1, x + 2):
                if cy == y and cx == x:
                    continue
                cells.append(self.get(cx, cy))
        return cells

    def set_positions(self, positions, alive=True):
        """Modifies the cell status at the given position.
        Arguments:
            postions -- [(x, y), (x, y), ...]
            alive -- setting cell status.
        """
        for (x, y) in positions:
            self.set_alive(x, y, alive)

    def get_positions(self, alive=True):
        """Returns positions where cell is alive.
        Arguments:
            alive -- pickup cell status.
        Returns:
            positions -- [(x, y), (x, y), ...]
        """
        positions = []
        for i in range(self.width * self.height):
            if self.cells[i].is_alive() == alive:
                cx = i % self.width
                cy = i // self.width
                positions.append((cx, cy))
        return positions

    def is_alive(self, x, y):
        """Return true if cell at the given position is alive, false otherwise.
        Arguments:
            x -- map coordinate
            y -- map coordinate
        """
        return self.get(x, y).is_alive()

    def change_next(self):
        """Calculate next generation and change it.
        """
        for ty in range(self.height):
            for tx in range(self.width):
                cells = self.get_around(tx, ty)
                cell = self.get(tx, ty)
                cell.calc_next(cells)
        for ty in range(self.height):
            for tx in range(self.width):
                cell = self.get(tx, ty)
                cell.change_next()


if __name__ == "__main__":

    def dump(cm, chr_alive='#', chr_dead='.'):
        """It displays cellmap with text.
        Arguments:
            cm -- CellMap object
            chr_allive -- charcter of alive
            chr_dead -- charcter of dead
        Returns:
            text
        """
        lines = []
        for ty in range(cm.height):
            line = []
            for tx in range(cm.width):
                cell = cm.get(tx, ty)
                if cell.is_alive():
                    line.append(chr_alive)
                else:
                    line.append(chr_dead)
            lines.append(line)

        return '\n'.join([''.join(line) for line in lines])

    glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    ox = 0
    oy = 0

    cm = CellMap(16, 16)
    for (cx, cy) in glider:
        cm.set_alive(cx + ox, cy + oy, True)

    for i in range(30):
        print '[%02d]' % i
        print dump(cm)
        cm.change_next()
