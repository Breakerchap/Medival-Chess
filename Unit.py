import pygame
import os
CELL_SIZE = 64


class Unit:
    def __init__(self, x, y):
        # Get the base directory where the script is running
        basePath = os.path.dirname(__file__)
        spritePath = os.path.join(basePath, "sprites", "unit_sprites", "spr_red_solider.png")
        
        # Load and scale the sprite
        if os.path.exists(spritePath):
            originalImage = pygame.image.load(spritePath).convert_alpha()
            self.image = pygame.transform.smoothscale(originalImage, (64, 64))
        else:
            print(f"Error: Image not found at {spritePath}")
            self.image = None  # Handle missing image gracefully

        # Position and movement attributes
        self.rect = self.image.get_rect(topleft=(x, y)) if self.image else pygame.Rect(x, y, 64, 64)
        self.isSelected = False

    def handleEvent(self, event, offsetX, offsetY):
        """Handle events for selecting and moving the unit."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouseX, mouseY = event.pos
            adjustedX = mouseX - offsetX
            adjustedY = mouseY - offsetY
            if self.rect.collidepoint(adjustedX, adjustedY):
                self.isSelected = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Release left mouse button
            if self.isSelected:
                # Snap the unit to the nearest grid cell
                self.rect.x = round((self.rect.x - offsetX) / CELL_SIZE) * CELL_SIZE + offsetX
                self.rect.y = round((self.rect.y - offsetY) / CELL_SIZE) * CELL_SIZE + offsetY
                self.isSelected = False
        elif event.type == pygame.MOUSEMOTION and self.isSelected:
            mouseX, mouseY = event.pos
            self.rect.x = mouseX - self.rect.width // 2
            self.rect.y = mouseY - self.rect.height // 2

    def draw(self, surface, offsetX, offsetY):
        """Draw the unit."""
        if self.image:
            adjustedRect = self.rect.move(offsetX, offsetY)
            surface.blit(self.image, adjustedRect.topleft)