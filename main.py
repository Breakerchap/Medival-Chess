import pygame
import sys

# Initialise Pygame
pygame.init()

# Constants
CELL_SIZE = 64
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
LIGHT_GREEN = (204, 255, 153)  # Light yellowy-green
DARK_GREEN = (153, 204, 102)   # Darker yellow-green
CAMERA_SPEED = 1.75  # Adjust camera speed here

# Grid dimensions
TOP_BOTTOM_COLS = 15
TOP_BOTTOM_ROWS = 6
MIDDLE_COLS = 21
MIDDLE_ROWS = 16

# Middle grid offset for centring
MIDDLE_OFFSET_X = (TOP_BOTTOM_COLS - MIDDLE_COLS) // 2 * CELL_SIZE

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alternating Green Grid with Centre Alignment")

class Cell:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def draw(self, surface, offsetX, offsetY):
        # Adjust the position of the cell based on the camera offset
        adjustedRect = self.rect.move(offsetX, offsetY)
        pygame.draw.rect(surface, self.colour, adjustedRect)

class Grid:
    def __init__(self):
        self.offsetX = 0  # Horizontal camera offset
        self.offsetY = 0  # Vertical camera offset

        # Create the grids
        self.topGrid = self.createGrid(TOP_BOTTOM_ROWS, TOP_BOTTOM_COLS, 0, 0, invertColours=False)
        self.middleGrid = self.createGrid(MIDDLE_ROWS, MIDDLE_COLS, MIDDLE_OFFSET_X, TOP_BOTTOM_ROWS * CELL_SIZE, invertColours=True)
        self.bottomGrid = self.createGrid(TOP_BOTTOM_ROWS, TOP_BOTTOM_COLS, 0, (TOP_BOTTOM_ROWS + MIDDLE_ROWS) * CELL_SIZE, invertColours=False)

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

    def moveCamera(self, dx, dy):
        """Moves the camera by adjusting the offset for all grid sections together."""
        self.offsetX += dx
        self.offsetY += dy

def main():
    # Create the grid
    grid = Grid()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move up
            grid.moveCamera(0, CAMERA_SPEED)
        if keys[pygame.K_s]:  # Move down
            grid.moveCamera(0, -CAMERA_SPEED)
        if keys[pygame.K_a]:  # Move left
            grid.moveCamera(CAMERA_SPEED, 0)
        if keys[pygame.K_d]:  # Move right
            grid.moveCamera(-CAMERA_SPEED, 0)

        # Fill the screen with a background colour (optional)
        screen.fill((0, 0, 0))

        # Draw the grid
        grid.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()


# TODO:
# Fix camera movement
# Add a background colour
# Add pieces