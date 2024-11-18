import pygame
from Cell import Cell
from Unit import Unit

CELL_SIZE = 64
LIGHT_GREEN = (204, 255, 153)
DARK_GREEN = (153, 204, 102)
TOP_BOTTOM_COLS = 15
TOP_BOTTOM_ROWS = 6
MIDDLE_COLS = 21
MIDDLE_ROWS = 16
MIDDLE_OFFSET_X = (TOP_BOTTOM_COLS - MIDDLE_COLS) // 2 * CELL_SIZE


class Board:
    def __init__(self):
        self.offsetX = 0  # Horizontal camera offset
        self.offsetY = 0  # Vertical camera offset

        # Create the grids
        self.topGrid = self.createGrid(TOP_BOTTOM_ROWS, TOP_BOTTOM_COLS, 0, 0, invertColours=False)
        self.middleGrid = self.createGrid(MIDDLE_ROWS, MIDDLE_COLS, MIDDLE_OFFSET_X, TOP_BOTTOM_ROWS * CELL_SIZE, invertColours=True)
        self.bottomGrid = self.createGrid(TOP_BOTTOM_ROWS, TOP_BOTTOM_COLS, 0, (TOP_BOTTOM_ROWS + MIDDLE_ROWS) * CELL_SIZE, invertColours=False)

        # Create a unit and place it at an initial position
        self.unit = Unit(4 * CELL_SIZE, 4 * CELL_SIZE)  # Place unit on the middle grid

    def createGrid(self, rows, cols, offsetX, offsetY, invertColours):
        """Creates a grid of alternating green cells, with optional colour inversion."""
        cells = []
        for row in range(rows):
            row_cells = []
            for col in range(cols):
                x = col * CELL_SIZE + offsetX
                y = row * CELL_SIZE + offsetY
                # Alternate between light and dark green with optional inversion
                if invertColours:
                    colour = DARK_GREEN if (row + col) % 2 == 0 else LIGHT_GREEN
                else:
                    colour = LIGHT_GREEN if (row + col) % 2 == 0 else DARK_GREEN
                row_cells.append(Cell(x, y, colour))
            cells.append(row_cells)
        return cells

    def draw(self, surface):
        """Draws all cells in all grids, applying the same camera offset to each section."""
        # Draw the top grid
        for row in self.topGrid:
            for cell in row:
                cell.draw(surface, self.offsetX, self.offsetY)

        # Draw the middle grid
        for row in self.middleGrid:
            for cell in row:
                cell.draw(surface, self.offsetX, self.offsetY)

        # Draw the bottom grid
        for row in self.bottomGrid:
            for cell in row:
                cell.draw(surface, self.offsetX, self.offsetY)

        # Draw the unit
        self.unit.draw(surface, self.offsetX, self.offsetY)

    def moveCamera(self, dx, dy):
        """Moves the camera by adjusting the offset for all grid sections together."""
        self.offsetX += dx
        self.offsetY += dy
