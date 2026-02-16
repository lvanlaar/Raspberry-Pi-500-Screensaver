import pygame
import random

pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

# Base colors
BASE_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (255, 255, 255)
]

class ColorBlock:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = random.choice(BASE_COLORS)
        self.target_color = random.choice(BASE_COLORS)
        self.speed = random.uniform(0.01, 0.03)
        self.progress = random.random()  # Start at random progress
        
    def update(self):
        # Smooth color transition
        self.progress += self.speed
        if self.progress >= 1:
            self.progress = 0
            self.color = self.target_color
            self.target_color = random.choice([c for c in BASE_COLORS if c != self.color])
        
        # Interpolate color
        r = int(self.color[0] * (1 - self.progress) + self.target_color[0] * self.progress)
        g = int(self.color[1] * (1 - self.progress) + self.target_color[1] * self.progress)
        b = int(self.color[2] * (1 - self.progress) + self.target_color[2] * self.progress)
        
        return (r, g, b)

def block_screensaver():
    running = True
    clock = pygame.time.Clock()
    
    # Create grid of blocks
    grid_size = 4  # 4x4 grid
    block_width = screen_width // grid_size
    block_height = screen_height // grid_size
    
    blocks = []
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * block_width
            y = row * block_height
            blocks.append(ColorBlock(x, y, block_width, block_height))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                running = False
        
        # Draw all blocks
        for block in blocks:
            color = block.update()
            pygame.draw.rect(screen, color, block.rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    block_screensaver()
