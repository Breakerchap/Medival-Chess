import pygame
import sys

# Initialise Pygame
pygame.init()

# Constants
CELL_SIZE = 64
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
LIGHT_GREEN = (204, 255, 153)
DARK_GREEN = (153, 204, 102)
CAMERA_SPEED = 1.75

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
        adjustedRect = self.rect.move(offsetX, offsetY)
        pygame.draw.rect(surface, self.colour, adjustedRect)

class Unit:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.color = (255, 0, 0)  # Red colour for the unit
        self.isSelected = False
        self.highlightedMoves = []

    def draw(self, surface, offsetX, offsetY):
        adjustedRect = self.rect.move(offsetX, offsetY)
        pygame.draw.rect(surface, self.color, adjustedRect)
        
        # Draw possible moves if selected
        for move in self.highlightedMoves:
            move_rect = pygame.Rect(move[0], move[1], CELL_SIZE, CELL_SIZE).move(offsetX, offsetY)
            pygame.draw.rect(surface, (255, 255, 0, 100), move_rect, 0)  # Semi-transparent yellow

    def highlight_moves(self):
        # Example movement options (one cell in each direction)
        x, y = self.rect.topleft
        self.highlightedMoves = [
            (x + CELL_SIZE, y), (x - CELL_SIZE, y),
            (x, y + CELL_SIZE), (x, y - CELL_SIZE)
        ]

    def move_to(self, pos):
        self.rect.topleft = pos
        self.isSelected = False
        self.highlightedMoves.clear()

class Grid:
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        self.topGrid = self.createGrid(TOP_BOTTOM_ROWS, TOP_BOTTOM_COLS, 0, 0, invertColours=False)
        self.middleGrid = self.createGrid(MIDDLE_ROWS, MIDDLE_COLS, MIDDLE_OFFSET_X, TOP_BOTTOM_ROWS * CELL_SIZE, invertColours=True)
        self.bottomGrid = self.createGrid(TOP_BOTTOM_ROWS, TOP_BOTTOM_COLS, 0, (TOP_BOTTOM_ROWS + MIDDLE_ROWS) * CELL_SIZE, invertColours=False)
        self.unit = Unit(4 * CELL_SIZE, 4 * CELL_SIZE)  # Place unit in initial position

    def createGrid(self, rows, cols, offsetX, offsetY, invertColours):
        cells = []
        for row in range(rows):
            row_cells = []
            for col in range(cols):
                x = col * CELL_SIZE + offsetX
                y = row * CELL_SIZE + offsetY
                if invertColours:
                    colour = DARK_GREEN if (row + col) % 2 == 0 else LIGHT_GREEN
                else:
                    colour = LIGHT_GREEN if (row + col) % 2 == 0 else DARK_GREEN
                row_cells.append(Cell(x, y, colour))
            cells.append(row_cells)
        return cells

    def draw(self, surface):
        for row in self.topGrid:
            for cell in row:
                cell.draw(surface, self.offsetX, self.offsetY)
        for row in self.middleGrid:
            for cell in row:
                cell.draw(surface, self.offsetX, self.offsetY)
        for row in self.bottomGrid:
            for cell in row:
                cell.draw(surface, self.offsetX, self.offsetY)
        self.unit.draw(surface, self.offsetX, self.offsetY)

    def moveCamera(self, dx, dy):
        self.offsetX += dx
        self.offsetY += dy

    def on_click(self, mouse_pos):
        # Translate mouse click position to grid space
        grid_pos = (mouse_pos[0] - self.offsetX, mouse_pos[1] - self.offsetY)
        if self.unit.rect.collidepoint(grid_pos):
            self.unit.isSelected = not self.unit.isSelected
            if self.unit.isSelected:
                self.unit.highlight_moves()
            else:
                self.unit.highlightedMoves.clear()
        elif self.unit.isSelected:
            # Move unit to a valid highlighted move if clicked
            for move in self.unit.highlightedMoves:
                move_rect = pygame.Rect(move[0], move[1], CELL_SIZE, CELL_SIZE)
                if move_rect.collidepoint(grid_pos):
                    self.unit.move_to(move)
                    break

def main():
    grid = Grid()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                grid.on_click(event.pos)

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

        screen.fill((0, 0, 0))
        grid.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()

# TODO:
# - Add Sprites
# - Add 2 teams
# - Add Attacking