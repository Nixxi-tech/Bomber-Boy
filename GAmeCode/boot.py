import pygame
import random

class Boot:
    def __init__(self, grid, tile_size):
        self.grid = grid
        self.tile_size = tile_size
        self.x, self.y = self.get_random_spawn()
        self.image = pygame.image.load(r"D:\Python_Code\GAmeCode\battlefield\enemy1.gif")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.speed = 1  # 50% slower than player
        self.move_timer = 0
        self.move_interval = 10  # Delay for tile-by-tile movement
        self.alive = True

    def get_random_spawn(self):
        while True:
            x = random.randint(1, len(self.grid[0]) - 2)
            y = random.randint(1, len(self.grid) - 2)
            if self.grid[y][x] == 0:
                return x * self.tile_size, y * self.tile_size

    def update(self, grid, players):
        if not self.alive:
            return

        self.move_timer += 1
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0

        target = min(players, key=lambda p: abs(p.x - self.x) + abs(p.y - self.y) if p.alive else float('inf'))
        dx = dy = 0
        target_tile_x = int(target.x // self.tile_size)
        target_tile_y = int(target.y // self.tile_size)
        boot_tile_x = int(self.x // self.tile_size)
        boot_tile_y = int(self.y // self.tile_size)

        if target_tile_x > boot_tile_x and grid[boot_tile_y][boot_tile_x + 1] == 0:
            dx = self.speed
        elif target_tile_x < boot_tile_x and grid[boot_tile_y][boot_tile_x - 1] == 0:
            dx = -self.speed
        elif target_tile_y > boot_tile_y and grid[boot_tile_y + 1][boot_tile_x] == 0:
            dy = self.speed
        elif target_tile_y < boot_tile_y and grid[boot_tile_y - 1][boot_tile_x] == 0:
            dy = -self.speed

        # Move per tile
        if abs(self.x % self.tile_size) == 0 and abs(self.y % self.tile_size) == 0:
            self.x += dx
            self.y += dy

        # Check collision with player
        for player in players:
            if self.x == player.x and self.y == player.y and player.alive:
                player.alive = False
                self.alive = False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))
