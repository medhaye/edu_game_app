import pygame
import sys
import os
from recycle_game import recycle_game

# Get the assets path from environment variable
ASSETS_PATH = os.environ.get('ASSETS_PATH', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets'))

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Function to round corners of an image
def round_image(image, radius):
    rect = image.get_rect()
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 0), rect, border_radius=radius)
    
    alpha_mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(alpha_mask, (255, 255, 255), rect, border_radius=radius)
    
    rounded_image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    rounded_image.blit(image, (0, 0))
    rounded_image.blit(alpha_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    return rounded_image

# Level selection function
def level_selection(is_win_1 = False):
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Select Level")
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join(ASSETS_PATH, "level_menu_background.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    levels = ["Sea", "Recycle"]  # Change "Jungle" to "Recycle"
    unlocked_levels = 1 + (1 if is_win_1 else 0)  # Unlock level 2 if is_win_1 is True
    buttons = []

    # Load images
    sea_image = pygame.image.load(os.path.join(ASSETS_PATH, "background_sea.png"))
    sea_image = pygame.transform.scale(sea_image, (200, 150))
    sea_image_rounded = round_image(sea_image, 20)

    recycle_image = pygame.image.load(os.path.join(ASSETS_PATH, "recycle.png")) if is_win_1 else None
    if recycle_image:
        recycle_image = pygame.transform.scale(recycle_image, (200, 150))
        recycle_image_rounded = round_image(recycle_image, 20)

    lock_image = pygame.image.load(os.path.join(ASSETS_PATH, "lock_icon.png"))
    lock_image = pygame.transform.scale(lock_image, (50, 50))

    # Create buttons
    for i, level in enumerate(levels):
        x = WIDTH // 2 - 220 + (i * 250)
        y = HEIGHT // 2 - 75
        rect = pygame.Rect(x, y, 200, 150)
        buttons.append((rect, level, i < unlocked_levels))

    while True:
        screen.blit(background, (0, 0))
        draw_text("Select Level", font, (255, 255, 255), screen, WIDTH // 2, 80)

        for i, (rect, name, unlocked) in enumerate(buttons):
            if unlocked:
                pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=20)
                if name == "Sea":
                    screen.blit(sea_image_rounded, (rect.x, rect.y))
                elif name == "Recycle" and recycle_image:
                    screen.blit(recycle_image_rounded, (rect.x, rect.y))
                draw_text(name, pygame.font.Font(None, 40), (255, 255, 255), screen, rect.centerx, rect.bottom + 20)
            else:
                pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=20)
                screen.blit(lock_image, (rect.centerx - 25, rect.centery - 25))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, name, unlocked in buttons:
                    if unlocked and rect.collidepoint(event.pos):
                        if name == "Sea":
                            # Return 'sea' to indicate sea level selection
                            return "sea"  # Start the sea level
                        elif name == "Recycle":
                            return recycle_game()  # Start the recycle level

        clock.tick(30)
