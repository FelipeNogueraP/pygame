import pygame
import sys


# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
ANIMATION_SPEED = 0.15  # Animation speed

# Colors
WHITE = (255, 255, 255)

# Configure the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Walking Animation")

# Load the animation image
sprite_sheet = pygame.image.load("Task1/walking_animation.png").convert_alpha()

# Split the image into frames
NUM_FRAMES = 8  # Assuming 8 frames per row
ORIGINAL_FRAME_WIDTH = sprite_sheet.get_width() // NUM_FRAMES
FRAME_HEIGHT = sprite_sheet.get_height() // 2
FRAME_WIDTH = (ORIGINAL_FRAME_WIDTH * 2) // 3

# Extract frames for both directions with adjusted width
frames_right = [sprite_sheet.subsurface(pygame.Rect(i * ORIGINAL_FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)) for i in range(NUM_FRAMES)]
frames_left = [sprite_sheet.subsurface(pygame.Rect(i * ORIGINAL_FRAME_WIDTH + (ORIGINAL_FRAME_WIDTH - FRAME_WIDTH), FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)) for i in range(NUM_FRAMES)]

# Initialize character variables
x_pos = 0
y_pos = SCREEN_HEIGHT - FRAME_HEIGHT
x_speed = 5
current_frame = 0
direction = 1  # 1 for right, -1 for left

# Clock to control FPS
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update character position
    x_pos += x_speed * direction

    # Check screen boundaries
    if x_pos + FRAME_WIDTH > SCREEN_WIDTH or x_pos < 0:
        direction *= -1

    # Update animation frame
    current_frame += ANIMATION_SPEED
    if current_frame >= NUM_FRAMES:
        current_frame = 0

    # Draw background
    screen.fill(WHITE)

    # Draw current frame
    if direction == 1:
        screen.blit(frames_right[int(current_frame)], (x_pos, y_pos))
    else:
        screen.blit(frames_left[int(current_frame)], (x_pos, y_pos))

    # Update the display
    pygame.display.flip()

    # Control FPS speed
    clock.tick(FPS)

# Exit the game
pygame.quit()
sys.exit()
