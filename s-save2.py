import pygame
import random
import math

pygame.init()

# Get display info
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

def draw_gradient(screen, color1, color2, direction="horizontal"):
    """Draw a gradient between two colors"""
    width, height = screen.get_size()
    
    if direction == "horizontal":
        for x in range(width):
            # Calculate color based on x position
            ratio = x / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (x, 0), (x, height))
    else:  # vertical
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

def gradient_screensaver():
    running = True
    clock = pygame.time.Clock()
    
    # Base colors
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 0, 255), (0, 255, 255)
    ]
    
    last_change = pygame.time.get_ticks()
    change_interval = 5000  # Change every 5 seconds
    color_pair = random.sample(colors, 2)
    direction = random.choice(["horizontal", "vertical"])
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                running = False
        
        current_time = pygame.time.get_ticks()
        if current_time - last_change > change_interval:
            color_pair = random.sample(colors, 2)
            direction = random.choice(["horizontal", "vertical"])
            last_change = current_time
        
        draw_gradient(screen, color_pair[0], color_pair[1], direction)
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    gradient_screensaver()
