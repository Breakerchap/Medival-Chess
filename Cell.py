import pygame
CELL_SIZE = 64


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