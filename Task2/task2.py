import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SCROLL_SPEED = 3  # Speed at which the text scrolls

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configure the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bitmap Font Scrolling Text")

# Load the TrueType font
font = pygame.font.Font("Task2/Px437_IBM_PGC-2x.ttf", 32)

# The text to be displayed
paragraph = "This is Task 2, bitmap font rendering and scrolling text in Pygame.  "

# Create the text surface
text_surface = font.render(paragraph * 10, True, BLACK)  # Repeat the paragraph to make it long enough for scrolling
text_rect = text_surface.get_rect(topleft=(SCREEN_WIDTH, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))

# Clock to control FPS
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the position of the text
    text_rect.x -= SCROLL_SPEED
    if text_rect.right < 0:
        text_rect.left = SCREEN_WIDTH

    # Draw background
    screen.fill(WHITE)

    # Draw the scrolling text
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

    # Control FPS speed
    clock.tick(FPS)

# Exit the game
pygame.quit()
sys.exit()
