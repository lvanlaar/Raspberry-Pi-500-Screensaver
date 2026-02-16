#!/usr/bin/env python3
"""
Screensaver for Pi 500 - Activates after period of inactivity
"""

import pygame
import random
import time
import os
import sys
from datetime import datetime, timedelta

# Configuration
INACTIVITY_TIMEOUT = 180  # 3 minutes in seconds (adjust as needed)
CHECK_INTERVAL = 1  # Check input every second

# Initialize Pygame
pygame.init()

# Get the display info
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

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

class Screensaver:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()
        self.last_activity = datetime.now()
        self.screensaver_active = False
        
    def check_activity(self):
        """Check for any user activity"""
        # Check for mouse movement
        if pygame.mouse.get_rel() != (0, 0):
            self.last_activity = datetime.now()
            if self.screensaver_active:
                self.stop_screensaver()
            return True
        
        # Check for key presses
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN]:
                self.last_activity = datetime.now()
                if self.screensaver_active:
                    self.stop_screensaver()
                return True
        
        return False
    
    def start_screensaver(self):
        """Activate the screensaver"""
        if self.screensaver_active:
            return
            
        print("Activity timeout - starting screensaver")
        self.screensaver_active = True
        
        # Set up fullscreen display
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), 
            pygame.FULLSCREEN | pygame.NOFRAME
        )
        pygame.mouse.set_visible(False)
        
        # Start the selected screensaver mode
        self.run_color_cycle()
    
    def stop_screensaver(self):
        """Deactivate the screensaver"""
        print("Activity detected - stopping screensaver")
        self.screensaver_active = False
        pygame.mouse.set_visible(True)
        pygame.display.quit()
        # Re-initialize display to return to normal
        self.screen = None
    
    def run_color_cycle(self):
        """Option 1: Smooth color transitions"""
        transition_time = 3
        last_change = time.time()
        current_color = random.choice(BASE_COLORS)
        next_color = random.choice(BASE_COLORS)
        
        running = True
        while running and self.screensaver_active:
            # Check for activity to exit
            if self.check_activity():
                return
            
            # Calculate transition
            elapsed = time.time() - last_change
            if elapsed >= transition_time:
                current_color = next_color
                next_color = random.choice([c for c in BASE_COLORS if c != current_color])
                last_change = time.time()
                elapsed = 0
            
            # Smooth color transition
            t = elapsed / transition_time
            blended_color = tuple(
                int(current_color[i] * (1 - t) + next_color[i] * t)
                for i in range(3)
            )
            
            self.screen.fill(blended_color)
            pygame.display.flip()
            self.clock.tick(60)
    
    def run_gradient_pattern(self):
        """Option 2: Gradient patterns"""
        colors = BASE_COLORS[:6]  # Use first 6 colors
        last_change = pygame.time.get_ticks()
        change_interval = 5000
        color_pair = random.sample(colors, 2)
        direction = random.choice(["horizontal", "vertical"])
        
        while self.screensaver_active:
            if self.check_activity():
                return
            
            current_time = pygame.time.get_ticks()
            if current_time - last_change > change_interval:
                color_pair = random.sample(colors, 2)
                direction = random.choice(["horizontal", "vertical"])
                last_change = current_time
            
            self.draw_gradient(color_pair[0], color_pair[1], direction)
            pygame.display.flip()
            self.clock.tick(30)
    
    def draw_gradient(self, color1, color2, direction):
        """Helper for gradient drawing"""
        if direction == "horizontal":
            for x in range(screen_width):
                ratio = x / screen_width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(self.screen, (r, g, b), (x, 0), (x, screen_height))
        else:
            for y in range(screen_height):
                ratio = y / screen_height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (screen_width, y))
    
    def run_color_blocks(self):
        """Option 3: Animated color blocks"""
        grid_size = 4
        block_width = screen_width // grid_size
        block_height = screen_height // grid_size
        
        class Block:
            def __init__(self, x, y):
                self.rect = pygame.Rect(x, y, block_width, block_height)
                self.color = random.choice(BASE_COLORS)
                self.target = random.choice([c for c in BASE_COLORS if c != self.color])
                self.speed = random.uniform(0.01, 0.03)
                self.progress = random.random()
            
            def update(self):
                self.progress += self.speed
                if self.progress >= 1:
                    self.progress = 0
                    self.color = self.target
                    self.target = random.choice([c for c in BASE_COLORS if c != self.color])
                
                r = int(self.color[0] * (1 - self.progress) + self.target[0] * self.progress)
                g = int(self.color[1] * (1 - self.progress) + self.target[1] * self.progress)
                b = int(self.color[2] * (1 - self.progress) + self.target[2] * self.progress)
                return (r, g, b)
        
        blocks = []
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * block_width
                y = row * block_height
                blocks.append(Block(x, y))
        
        while self.screensaver_active:
            if self.check_activity():
                return
            
            for block in blocks:
                color = block.update()
                pygame.draw.rect(self.screen, color, block.rect)
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def run(self, mode=1):
        """
        Main loop - monitors inactivity and runs screensaver
        mode: 1=color cycle, 2=gradient, 3=color blocks
        """
        print(f"Screensaver started. Will activate after {INACTIVITY_TIMEOUT} seconds of inactivity.")
        print("Press Ctrl+C to exit")
        
        # Set up a small window for monitoring (invisible)
        pygame.display.set_mode((100, 100), pygame.NOFRAME)
        pygame.mouse.set_visible(True)
        
        try:
            while True:
                # Check for activity
                self.check_activity()
                
                # Calculate inactive time
                inactive_seconds = (datetime.now() - self.last_activity).total_seconds()
                
                # Show status occasionally
                if int(time.time()) % 60 == 0:  # Every minute
                    print(f"Inactive for {int(inactive_seconds)} seconds")
                
                # Check if we should activate screensaver
                if not self.screensaver_active and inactive_seconds >= INACTIVITY_TIMEOUT:
                    if mode == 1:
                        self.start_screensaver()
                        self.run_color_cycle()
                    elif mode == 2:
                        self.start_screensaver()
                        self.run_gradient_pattern()
                    else:
                        self.start_screensaver()
                        self.run_color_blocks()
                
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\nScreensaver stopped by user")
        finally:
            pygame.quit()
            sys.exit(0)

if __name__ == "__main__":
    # Choose mode by changing the number:
    # 1 = Color cycle (smooth transitions)
    # 2 = Gradient patterns
    # 3 = Animated color blocks
    MODE = 1
    
    saver = Screensaver()
    saver.run(mode=MODE)

