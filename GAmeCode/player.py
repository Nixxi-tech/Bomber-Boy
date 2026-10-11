import pygame
import random

tile_size = 32
cols, rows = 23, 13
WIDTH, HEIGHT = cols * tile_size, rows * tile_size

# Load player images
player_imgs = [
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character1.jpg"),
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character2.jpeg"),
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character3.jpeg"),
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character4.jpeg")
]
player_imgs = [pygame.transform.scale(img, (tile_size, tile_size)) for img in player_imgs]

class Player:
    def __init__(self, x, y, sprite_index, ai_controlled=False):
        self.x = x * tile_size
        self.y = y * tile_size
        self.sprite_index = sprite_index
        self.alive = True
        self.ai_controlled = ai_controlled
        self.ai_move_timer = 0
        self.explosion_range = 1  # Default explosion range

    def move(self, dx, dy, grid):
        new_x, new_y = self.x + dx * tile_size, self.y + dy * tile_size
        grid_x, grid_y = new_x // tile_size, new_y // tile_size

        # Check boundaries and collisions with walls and bombs
        if (
            0 <= grid_x < cols and
            0 <= grid_y < rows and
            grid[grid_y][grid_x] != 1 and  # Wall
            grid[grid_y][grid_x] != 2 and  # Destructible obstacle
            grid[grid_y][grid_x] != 3      # Bomb
        ):
            self.x, self.y = new_x, new_y

    def handle_controls(self, event, grid):
        if self.sprite_index == 0:  # Player 1 (WASD)
            if event.key == pygame.K_a:
                self.move(-1, 0, grid)
            elif event.key == pygame.K_d:
                self.move(1, 0, grid)
            elif event.key == pygame.K_w:
                self.move(0, -1, grid)
            elif event.key == pygame.K_s:
                self.move(0, 1, grid)
        elif self.sprite_index == 1:  # Player 2 (Arrow Keys)
            if event.key == pygame.K_LEFT:
                self.move(-1, 0, grid)
            elif event.key == pygame.K_RIGHT:
                self.move(1, 0, grid)
            elif event.key == pygame.K_UP:
                self.move(0, -1, grid)
            elif event.key == pygame.K_DOWN:
                self.move(0, 1, grid)

    def ai_move(self, grid):
        if pygame.time.get_ticks() - self.ai_move_timer > 500:
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.move(*direction, grid)
            self.ai_move_timer = pygame.time.get_ticks()

    def draw(self, screen):
        if self.alive:
            screen.blit(player_imgs[self.sprite_index], (self.x, self.y))
