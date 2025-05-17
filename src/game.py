import pygame
import random
import sqlite3

class Game:
    def __init__(self, screen, width, height, player_x, player_y, tries_left, current_world):
        self.screen = screen
        self.width = width
        self.height = height
        self.player_x = player_x
        self.player_y = player_y
        self.tries_left = tries_left
        self.current_world = current_world
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False
        self.animation_index = 0
        self.current_animation = "idle"
        self.is_facing_right = True
        self.camera_offset_x = 0
        self.platform_list = []
        self.generate_platforms()

    def generate_platforms(self):
        y = self.height - 20 - 10
        for i in range(6):
            self.platform_list.append(pygame.Rect(i * 70, y, 70, 20))
        platform_positions = [
            (100, self.height - 100),
            (300, self.height - 150),
            (500, self.height - 200),
            (700, self.height - 250),
            (900, self.height - 100),
            (1100, self.height - 150),
        ]
        for pos in platform_positions:
            self.platform_list.append(pygame.Rect(pos[0], pos[1], 70, 20))

    def reset(self):
        self.player_x, self.player_y = 50, self.height - 60 - 20 - 10
        self.tries_left = 3
        self.on_ground = False
        self.platform_list.clear()
        self.generate_platforms()

    def load_progress(self, player_x, player_y, tries_left, current_world):
        self.player_x = player_x
        self.player_y = player_y
        self.tries_left = tries_left
        self.current_world = current_world

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "back_to_menu"

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_x -= 5
                self.is_facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.player_x += 5
                self.is_facing_right = True
            if keys[pygame.K_SPACE] and self.on_ground:
                self.player_y_velocity = self.jump_strength
                self.on_ground = False

            # Apply gravity
            self.player_y_velocity = getattr(self, 'player_y_velocity', 0) + self.gravity
            self.player_y += self.player_y_velocity

            # Collision detection
            self.on_ground = False
            for platform in self.platform_list:
                if platform.colliderect(pygame.Rect(self.player_x, self.player_y + self.player_y_velocity, 40, 60)):
                    if self.player_y_velocity > 0:
                        self.player_y = platform.y - 60
                        self.player_y_velocity = 0
                        self.on_ground = True

            # Check if player falls off the screen
            if self.player_y > self.height:
                self.tries_left -= 1
                if self.tries_left <= 0:
                    return "back_to_menu"
                self.player_x, self.player_y = 50, self.height - 60 - 20 - 10

            # Move camera
            if self.player_x > self.width // 2:
                self.camera_offset_x = self.player_x - self.width // 2

            # Draw everything
            self.screen.fill((135, 206, 250))  # Sky blue background
            for platform in self.platform_list:
                pygame.draw.rect(self.screen, (165, 42, 42), 
                                 (platform.x - self.camera_offset_x, platform.y, 70, 20))
            pygame.draw.rect(self.screen, (255, 0, 0), 
                             (self.player_x - self.camera_offset_x, self.player_y, 40, 60))

            pygame.display.update()
            clock.tick(60)