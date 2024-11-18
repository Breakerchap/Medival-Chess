import pygame
import sys
from Board import Board

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CAMERA_SPEED = 1.75

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alternating Green Board with Unit")


def main():
    # Create the board
    board = Board()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Pass events to the unit for interaction
            board.unit.handleEvent(event, board.offsetX, board.offsetY)

        # Camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move up
            board.moveCamera(0, CAMERA_SPEED)
        if keys[pygame.K_s]:  # Move down
            board.moveCamera(0, -CAMERA_SPEED)
        if keys[pygame.K_a]:  # Move left
            board.moveCamera(CAMERA_SPEED, 0)
        if keys[pygame.K_d]:  # Move right
            board.moveCamera(-CAMERA_SPEED, 0)

        # Fill the screen with a background colour (optional)
        screen.fill((0, 0, 0))

        # Draw the board
        board.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()