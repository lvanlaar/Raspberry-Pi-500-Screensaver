import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Get the display info (will use your TV resolution)
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up fullscreen display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)  # Hide the mouse cursor

# Base colors (RGB tuples)
BASE_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 255),# White
    (128, 0, 128),  # Purple
    (255, 165, 0),  # Orange
]

def color_cycle_screensaver():
    running = True
    clock = pygame.time.Clock()
    
    # Transition time in seconds
    transition_time = 3
    last_change = time.time()
    current_color = random.choice(BASE_COLORS)
    next_color = random.choice(BASE_COLORS)
    
    while running:
        # Check for any key press or mouse movement to exit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                running = False
        
        # Calculate transition
        elapsed = time.time() - last_change
        if elapsed >= transition_time:
            # Switch to new color
            current_color = next_color
            next_color = random.choice([c for c in BASE_COLORS if c != current_color])
            last_change = time.time()
            elapsed = 0
        
        # Smooth color transition
        t = elapsed / transition_time
        # Interpolate between colors
        blended_color = tuple(
            int(current_color[i] * (1 - t) + next_color[i] * t)
            for i in range(3)
        )
        
        # Fill screen with current color
        screen.fill(blended_color)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    color_cycle_screensaver()
