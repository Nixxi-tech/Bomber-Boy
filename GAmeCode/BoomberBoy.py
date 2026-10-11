import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
tile_size = 32
cols, rows = WIDTH // tile_size, HEIGHT // tile_size
FPS = 120

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Load images
player_imgs = [
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character1.jpg"),
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character2.jpeg"),
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character3.jpeg"),
    pygame.image.load(r"D:\Python_Code\GAmeCode\character\character4.jpeg")
]
player_imgs = [pygame.transform.scale(img, (tile_size, tile_size)) for img in player_imgs]

block_img = pygame.Surface((tile_size, tile_size))
block_img.fill((150, 75, 0))
bomb_img = pygame.Surface((tile_size, tile_size))
bomb_img.fill(BLACK)
explosion_img = pygame.Surface((tile_size, tile_size))
explosion_img.fill(RED)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomber Bai - Multiplayer")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 74)


# Player class
class Player:
    def __init__(self, x, y, sprite_index):
        self.x = x
        self.y = y
        self.speed = tile_size // 2  # Reduced speed
        self.sprite_index = sprite_index
        self.alive = True

    def move(self, dx, dy, grid):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and grid[new_y // tile_size][new_x // tile_size] != 1:
            self.x, self.y = new_x, new_y

    def draw(self, screen):
        if self.alive:
            screen.blit(player_imgs[self.sprite_index], (self.x, self.y))


# Bomb class
class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = time.time()
        self.exploded = False
        self.range = 2
        self.explosion_effects = []

    def explode(self, grid, players):
        if time.time() - self.timer >= 2:
            self.exploded = True
            x, y = self.x // tile_size, self.y // tile_size

            # Create explosion effect
            self.explosion_effects.append((x, y))
            for i in range(1, self.range + 1):
                self.explosion_effects.append((x + i, y))
                self.explosion_effects.append((x - i, y))
                self.explosion_effects.append((x, y + i))
                self.explosion_effects.append((x, y - i))

            # Destroy blocks within range
            for ex, ey in self.explosion_effects:
                if 0 <= ey < rows and 0 <= ex < cols and grid[ey][ex] == 1:
                    grid[ey][ex] = 0

            # Damage players within range
            for player in players:
                px, py = player.x // tile_size, player.y // tile_size
                if (px, py) in self.explosion_effects:
                    player.alive = False

    def draw(self, screen):
        if not self.exploded:
            screen.blit(bomb_img, (self.x, self.y))
        else:
            for ex, ey in self.explosion_effects:
                screen.blit(explosion_img, (ex * tile_size, ey * tile_size))


# Generate grid with destructible blocks
def generate_grid():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for _ in range(20):
        x, y = random.randint(1, cols - 2), random.randint(1, rows - 2)
        grid[y][x] = 1
    return grid


grid = generate_grid()
players = [
    Player(32, 32, 0),
    Player(WIDTH - 64, HEIGHT - 64, 1),
    Player(32, HEIGHT - 64, 2),
    Player(WIDTH - 64, 32, 3)
]
bombs = []

# Game loop
running = True
winner = None
while running:
    screen.fill((0, 100, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            for i, player in enumerate(players):
                if player.alive:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_RSHIFT, pygame.K_RCTRL] and i == 0:
                        bombs.append(Bomb(player.x, player.y))

    keys = pygame.key.get_pressed()
    for i, player in enumerate(players):
        if player.alive:
            controls = [
                (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN),
                (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s),
                (pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k),
                (pygame.K_KP4, pygame.K_KP6, pygame.K_KP8, pygame.K_KP5)
            ]
            if keys[controls[i][0]]:
                player.move(-player.speed, 0, grid)
            if keys[controls[i][1]]:
                player.move(player.speed, 0, grid)
            if keys[controls[i][2]]:
                player.move(0, -player.speed, grid)
            if keys[controls[i][3]]:
                player.move(0, player.speed, grid)

    # Draw grid
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1:
                screen.blit(block_img, (x * tile_size, y * tile_size))

    # Draw bombs
    for bomb in bombs:
        bomb.explode(grid, players)
        bomb.draw(screen)

    # Draw players
    for player in players:
        player.draw(screen)

    # Check for winner
    alive_players = [p for p in players if p.alive]
    if len(alive_players) == 1:
        winner = alive_players[0].sprite_index + 1

    if winner:
        text = font.render(f"Player {winner} Wins!", True, YELLOW)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(3)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()