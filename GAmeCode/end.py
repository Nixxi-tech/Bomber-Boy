import pygame
import sys

def show_victory_screen(screen, WIDTH, HEIGHT):
    font = pygame.font.Font(None, 74)
    text = font.render("VICTORY!", True, (0, 255, 0))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))

    button_font = pygame.font.Font(None, 50)

    start_button = button_font.render("Start Again", True, (255, 255, 255))
    exit_button = button_font.render("Exit", True, (255, 255, 255))

    start_rect = start_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    exit_rect = exit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))

    screen.blit(start_button, start_rect)
    screen.blit(exit_button, exit_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    waiting = False  # Restart the game
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
