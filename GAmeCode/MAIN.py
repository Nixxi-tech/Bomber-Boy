import pygame
import random
import time
from player import Player
from bomb import Bomb
import end
import boot

pygame.init()

# Game settings
tile_size = 32
cols, rows = 23, 13
WIDTH, HEIGHT = cols * tile_size, rows * tile_size
FPS = 60

# Load images
steel_wall = pygame.image.load(r"D:\Python_Code\GAmeCode\battlefield\istockphoto-639251818-612x612.jpg")
steel_wall = pygame.transform.scale(steel_wall, (tile_size, tile_size))

brick_wall = pygame.image.load(r"D:\Python_Code\GAmeCode\battlefield\wall.webp")
brick_wall = pygame.transform.scale(brick_wall, (tile_size, tile_size))

powerbomb_img = pygame.image.load(r"D:\Python_Code\GAmeCode\battlefield\powerbomb.png")
powerbomb_img = pygame.transform.scale(powerbomb_img, (tile_size, tile_size))

gate_img = pygame.image.load(r"D:\Python_Code\GAmeCode\battlefield\hole.png")
gate_img = pygame.transform.scale(gate_img, (tile_size, tile_size))

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def generate_grid():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for y in range(rows):
        grid[y][0] = grid[y][cols - 1] = 1
    for x in range(cols):
        grid[0][x] = grid[rows - 1][x] = 1

    for y in range(2, rows - 2, 2):
        for x in range(2, cols - 2, 2):
            grid[y][x] = 1

    obstacle_positions = []
    while len(obstacle_positions) < 50:
        x = random.randint(1, cols - 2)
        y = random.randint(1, rows - 2)

        if (
            grid[y][x] == 0 and
            not (x < 3 and y < 3) and
            not (x > cols - 4 and y > rows - 4) and
            not (x < 3 and y > rows - 4) and
            not (x > cols - 4 and y < 3)
        ):
            grid[y][x] = 2
            obstacle_positions.append((x, y))

    gate_position = random.choice(obstacle_positions)
    return grid, gate_position

# Generate battlefield
grid, gate_position = generate_grid()
gate_revealed = False

# Players and bombs
players = [
    Player(1, 1, 0),
    Player(cols - 2, rows - 2, 1)
]
bombs = []
enemies = [boot.Boot(grid, tile_size) for _ in range(2)]

running = True
while running:
    screen.fill((0, 100, 0))  # Green background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            for player in players:
                if player.alive:
                    player.handle_controls(event, grid)
                    if (event.key == pygame.K_SPACE and player.sprite_index == 0) or (event.key == pygame.K_RETURN and player.sprite_index == 1):
                        if grid[player.y // tile_size][player.x // tile_size] == 0:
                            bombs.append(Bomb(player.x, player.y, player.explosion_range))
                            grid[player.y // tile_size][player.x // tile_size] = 3

    bombs = [bomb for bomb in bombs if not bomb.explode(grid, players, screen)]

    # Reveal gate when its obstacle is destroyed
    if not gate_revealed and grid[gate_position[1]][gate_position[0]] == 0:
        grid[gate_position[1]][gate_position[0]] = 5
        gate_revealed = True

    # Check for powerbomb pickup or gate interaction
    for player in players:
        player_tile = (player.x // tile_size, player.y // tile_size)
        if grid[player_tile[1]][player_tile[0]] == 4:
            player.explosion_range += 1
            grid[player_tile[1]][player_tile[0]] = 0
        elif grid[player_tile[1]][player_tile[0]] == 5:  # Gate interaction
            end.show_victory_screen(screen, WIDTH, HEIGHT)
            running = False

    for enemy in enemies:
        enemy.update(grid, players)
        enemy.draw(screen)

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1:
                screen.blit(steel_wall, (x * tile_size, y * tile_size))
            elif grid[y][x] == 2:
                screen.blit(brick_wall, (x * tile_size, y * tile_size))
            elif grid[y][x] == 4:
                screen.blit(powerbomb_img, (x * tile_size, y * tile_size))
            elif grid[y][x] == 5:
                screen.blit(gate_img, (x * tile_size, y * tile_size))

    for player in players:
        player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
