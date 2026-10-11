import pygame
import time
import random

tile_size = 32

# Load images
bomb_img = pygame.image.load(r"D:\Python_Code\GAmeCode\character\boom.png")
bomb_img = pygame.transform.scale(bomb_img, (tile_size, tile_size))

explosion_img = pygame.Surface((tile_size, tile_size))
explosion_img.fill((255, 0, 0))  # Red explosion mark


class Bomb:
    def __init__(self, x, y, explosion_range=1):
        self.x = x // tile_size
        self.y = y // tile_size
        self.explosion_range = explosion_range
        self.timer = time.time()
        self.exploded = False
        self.explosion_time = None
        self.explosion_pattern = []  # Store explosion pattern for both explosion and red mark

    def explode(self, grid, players, screen):
        current_time = time.time()

        # Bomb explodes after 2 seconds
        if not self.exploded and current_time - self.timer >= 2:
            self.exploded = True
            self.explosion_time = current_time
            grid[self.y][self.x] = 0  # Remove bomb from grid

            # Damage players at the bomb's location
            for player in players:
                if player.x // tile_size == self.x and player.y // tile_size == self.y:
                    player.alive = False

            # Explosion logic — stop after hitting obstacles
            self.explosion_pattern = [(self.x, self.y)]  # Add center explosion
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                for i in range(1, self.explosion_range + 1):
                    nx, ny = self.x + dx * i, self.y + dy * i

                    if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                        # Stop explosion at indestructible wall
                        if grid[ny][nx] == 1:
                            break

                        # Add explosion to pattern (for red mark consistency)
                        self.explosion_pattern.append((nx, ny))

                        # Break destructible obstacle and stop explosion
                        if grid[ny][nx] == 2:
                            # 20% chance to drop Powerbomb
                            if random.random() < 0.2:
                                grid[ny][nx] = 4
                            else:
                                grid[ny][nx] = 0
                            break

                        # Damage players in the explosion range
                        for player in players:
                            if player.x // tile_size == nx and player.y // tile_size == ny:
                                player.alive = False

        # Show explosion for 0.5 seconds after detonation
        if self.exploded:
            self.draw_explosion(screen)
            if current_time - self.explosion_time >= 0.5:
                return True  # Remove bomb after explosion effect ends

        # Draw bomb if not exploded
        self.draw(screen)
        return False

    def draw(self, screen):
        if not self.exploded:
            screen.blit(bomb_img, (self.x * tile_size, self.y * tile_size))

    def draw_explosion(self, screen):
        # Draw explosion effect (center + correct pattern)
        for nx, ny in self.explosion_pattern:
            screen.blit(explosion_img, (nx * tile_size, ny * tile_size))
