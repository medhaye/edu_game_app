import pygame
import sys
import os
import subprocess
from menu import level_selection

# Get the assets path from environment variable
ASSETS_PATH = os.environ.get('ASSETS_PATH', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets'))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def main_menu():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platform Runner - Menu")
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join(ASSETS_PATH, "menu_background.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    button_font = pygame.font.Font(None, 40)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    
    while True:
        screen.blit(background, (0, 0))
        draw_text("Platform Runner", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 4)
        
        pygame.draw.rect(screen, (0, 128, 255), start_button, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), quit_button, border_radius=10)
        draw_text("Start Game", button_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 - 25)
        draw_text("Quit", button_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 45)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    selected_level = level_selection()
                    if selected_level == "sea":
                        # Launch sea level using our new clean implementation
                        pygame.quit()  # Close the current window
                        # Import and run the sea level game
                        from sea_level import run_sea_game
                        run_sea_game()
                        return  # Return after sea level is done
                    return  # Exit menu for other cases
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        clock.tick(30)

# Call the main_menu function when this script is run directly
if __name__ == "__main__":
    main_menu()
