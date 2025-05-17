import pygame
import sys
import random
from popup import Popup
from chat import chat_page

# Avoid circular imports
if __name__ == "__main__":
    # When run as a script, only import if needed
    pass
else:
    # When imported, avoid circular dependencies
    pass

# Define a function to run the sea level game
def run_sea_level():
    # Initialize variables
    pop_shown = False
    lose_pop_shown = False
    collected_objects = 0
    running = True
    NUM_PLATFORMS = 45
    
    # Initialize Pygame if not already initialized
    if not pygame.get_init():
        pygame.init()
    
    # Set up the screen
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platform Runner Game")
    
    # Load background image
    background = pygame.image.load("background_sea.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    # Load block image (brick block)
    block_image = pygame.image.load("Brick_Block.png")
    block_image = pygame.transform.scale(block_image, (70, 20))

    # Load object images
    objects = {
    "plastic_bottle": pygame.image.load("plastic_bottle.png"),
    "banana_peel": pygame.image.load("banana_peel.png"),
    "shopping_bag": pygame.image.load("shopping_bag.png"),
    "cigarette_filter": pygame.image.load("cigarette_filter.png"),
    "styrofoam_packaging": pygame.image.load("styrofoam_packaging.png"),
    "glass_bottle": pygame.image.load("glass_bottle.png")
}

# Scale objects to ensure they fit on platforms
max_object_width = 70  # Same as platform width
for key in objects:
    img = objects[key]
    if img.get_width() > max_object_width:
        # Maintain aspect ratio
        ratio = max_object_width / img.get_width()
        new_height = int(img.get_height() * ratio)
        objects[key] = pygame.transform.scale(img, (max_object_width, new_height))


# Load sprite sheet
sprite_sheet = pygame.image.load("sprite_sheet.png")
SPRITE_WIDTH, SPRITE_HEIGHT = 408 // 4, 611 // 4  # Each frame size (4x4 grid)

# Extract frames from sprite sheet
player_frames = {"run_right": [], "run_left": [], "idle": []}
for col in range(4):  # 4 columns per row
    player_frames["run_right"].append(pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(col * SPRITE_WIDTH, 2 * SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)), (40, 60)))
    player_frames["run_left"].append(pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(col * SPRITE_WIDTH, 3 * SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)), (40, 60)))
player_frames["idle"].append(pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)), (40, 60)))

# Platform settings
platform_width = block_image.get_width()
platform_height = block_image.get_height()
platform_list = []

# Player settings
player_width, player_height = 40, 60
player_x, player_y = 50, HEIGHT - player_height - platform_height - 10
player_speed = 5
player_y_velocity = 0
gravity = 0.5
jump_strength = -10
on_ground = False
animation_index = 0
animation_speed = 0.2
current_animation = "idle"
is_facing_right = True

# Camera offset
camera_offset_x = 0

# Load bird sprite sheet
bird_sprite_sheet = pygame.image.load("bird.png")
BIRD_SPRITE_WIDTH, BIRD_SPRITE_HEIGHT = bird_sprite_sheet.get_width() // 4, bird_sprite_sheet.get_height() // 2  # 2 rows and 4 columns

# Extract bird frames (rightward and leftward)
bird_frames = {"fly_right": [], "fly_left": []}
for col in range(4):  # 4 columns per row
    # Rightward movement (first row of the sprite sheet)
    bird_frames["fly_right"].append(pygame.transform.scale(bird_sprite_sheet.subsurface(pygame.Rect(col * BIRD_SPRITE_WIDTH, 0, BIRD_SPRITE_WIDTH, BIRD_SPRITE_HEIGHT)), (40, 60)))
    # Leftward movement (second row of the sprite sheet, mirror the frames)
    bird_frames["fly_left"].append(pygame.transform.scale(bird_sprite_sheet.subsurface(pygame.Rect(col * BIRD_SPRITE_WIDTH, BIRD_SPRITE_HEIGHT, BIRD_SPRITE_WIDTH, BIRD_SPRITE_HEIGHT)), (40, 60)))

# Bird settings
bird_x, bird_y = player_x + 50, player_y - 30  # Position bird relative to player
bird_speed = 3
bird_current_animation = "fly_right"
bird_is_facing_right = True
bird_animation_index = 0
bird_animation_speed = 0.1 

parrot_image = pygame.image.load("parrot.png")
parrot_image = pygame.transform.scale(parrot_image, (50, 50))

font = pygame.font.Font(None, 40)
    
chat_button = pygame.Rect(WIDTH - 60, 10, 50, 50)  # Chat button position


popup = Popup(
    parrot_image,
    "The sea is now under pollution and needs your help! Please help clean up by collecting trash and avoiding pollution sources.",
    "Help Now",
    "Thank you for your commitment! Collect 20 pieces of trash to make a difference. Let's protect our oceans!",
    is_it_last=True
)


# Create the ground
def create_starting_ground():
    y = HEIGHT - platform_height - 10
    for i in range(6):
        platform_list.append(pygame.Rect(i * platform_width, y, platform_width, platform_height))

def generate_platforms():
    y = HEIGHT - platform_height - 10
    create_starting_ground()
    platform_positions = [(100, 500), (300, 450), (500, 400), (700, 350), (900, 500), (1100, 450), (1300, 400), (1500, 350), (1700, 300), (1900, 500), (2100, 450), (2300, 400), (2500, 350), (2700, 300), (2900, 500), (3100, 450), (3300, 400), (3500, 350), (3700, 300), (3900, 500), (4100, 450), (4300, 400), (4500, 350), (4700, 300), (4900, 500), (5100, 450), (5300, 400), (5500, 350), (5700, 300), (5900, 500), (6100, 450), (6300, 400), (6500, 350), (6700, 300), (6900, 500), (7100, 450)]

    # Create platforms at specified positions
    for pos in platform_positions:
        platform_list.append(pygame.Rect(pos[0], pos[1], platform_width, platform_height))


generate_platforms()

# Object placement (only allowed on platform positions)
class CollectibleObject(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collected = False

    def update(self, player_rect):
        if self.rect.colliderect(player_rect) and not self.collected:
            self.collected = True
            return True
        return False

# Initialize object spawn
object_list = pygame.sprite.Group()

import random

font = pygame.font.Font(None, 36)

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Function to draw progress bar
def draw_progress_bar(screen, collected_objects):
    percentage_collected = (collected_objects / 20) * 100
    bar_width = 300  # Max width of the progress bar
    bar_height = 30
    filled_width = int((percentage_collected / 100) * bar_width)
    
    # Render percentage text
    percentage_text = font.render(f"Progress: {percentage_collected:.1f}%", True, WHITE)
    
    # Draw progress bar background
    pygame.draw.rect(screen, BLACK, (100, 150, bar_width, bar_height))
    
    # Draw filled progress
    pygame.draw.rect(screen, GREEN, (100, 150, filled_width, bar_height))
    
    # Draw text
    screen.blit(percentage_text, (100, 100))

def generate_objects():
    object_types = [
        ("plastic_bottle", 4),
        ("banana_peel", 5),
        ("shopping_bag", 4),
        ("cigarette_filter", 3),
        ("styrofoam_packaging", 2),
        ("glass_bottle", 1)
    ]
    
    platform_positions = [
        (100, 500, True), (300, 450, False), (500, 400, True), (700, 350, False), (900, 500, True),
        (1100, 450, False), (1300, 400, True), (1500, 350, False), (1700, 300, True), (1900, 500, False),
        (2100, 450, True), (2300, 400, False), (2500, 350, True), (2700, 300, False), (2900, 500, True),
        (3100, 450, False), (3300, 400, True), (3500, 350, True), (3700, 300, True), (3900, 500, False),
        (4100, 450, True), (4300, 400, True), (4500, 350, True), (4700, 300, False), (4900, 500, True),
        (5100, 450, True), (5300, 400, True), (5500, 350, False), (5700, 300, True), (5900, 500, False),
        (6100, 450, True), (6300, 400, False), (6500, 350, True), (6700, 300, False), (6900, 500, True),
        (7100, 450, False)
    ]
    
    # Only pick positions where the third element is True
    valid_positions = [pos for pos in platform_positions if pos[2]]

    # For each valid position, create an object
    print("Valid positions:", valid_positions)
    for platform_pos in valid_positions:
        obj_type, _ = random.choice(object_types)  # Randomly pick an object type
        object_image = objects[obj_type]
        object_x = random.randint(platform_pos[0], platform_pos[0] + platform_width - object_image.get_width())
        object_y = platform_pos[1] - object_image.get_height()  # Place object above the platform
        new_object = CollectibleObject(object_image, object_x, object_y)
        object_list.add(new_object)
        print(f"Object {obj_type} created at ({object_x}, {object_y})")  # Debugging line

generate_objects()


# Game loop
running = True
clock = pygame.time.Clock()
collected_objects = 0
lose_pop_shown = False  # Track if lose popup is shown
def reset_game():
    global platform_list, object_list, player_x, player_y, player_y_velocity, on_ground, collected_objects, camera_offset_x, lose_pop_shown, pop_shown
    platform_list = []
    generate_platforms()
    object_list.empty()
    generate_objects()
    player_x, player_y = 50, HEIGHT - player_height - platform_height - 10
    player_y_velocity = 0
    on_ground = False
    collected_objects = 0
    camera_offset_x = 0
    lose_pop_shown = False
    pop_shown = False  # Ensure win popup is reset if any

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if chat_button.collidepoint(event.pos):
                # Open chat page when button is clicked
                chat_page(screen, font)
        if lose_pop_shown:
            if popup.handle_event(event):
                reset_game()

        popup.handle_event(event)

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_x - player_speed > 5 :
            player_x -= player_speed
            current_animation = "run_right"
            is_facing_right = False
            bird_current_animation = "fly_left"  # Make the bird fly left
            bird_is_facing_right = False
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed
        current_animation = "run_left"
        is_facing_right = True
        bird_current_animation = "fly_right"  # Make the bird fly right
        bird_is_facing_right = True
    else:
        current_animation = "idle"
        bird_current_animation = "fly_right"  # Bird stays facing right when idle

    if keys[pygame.K_SPACE] and on_ground:
        player_y_velocity = jump_strength
        on_ground = False

    # Apply gravity
    player_y_velocity += gravity
    player_y += player_y_velocity

    # Collision detection
    on_ground = False
    for platform in platform_list:
        platform_rect = pygame.Rect(platform.x, platform.y, platform_width, platform_height)

        # Check vertical collision (Landing on top)
        if platform_rect.colliderect(player_x, player_y + player_y_velocity, player_width, player_height):
            if player_y_velocity > 0 and player_y + player_height <= platform.y + 5:  # Allow a small margin
                player_y = platform.y - player_height  # Position player on top of platform
                player_y_velocity = 0
                on_ground = True

    # Check object collection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obj in object_list:
        if obj.update(player_rect):
            collected_objects += 1
    
    # Check if player collects all objects
    if collected_objects >= 20 and not pop_shown:
        popup = Popup(
            parrot_image,
            "Congratulations! You've collected all the trash!",
            "Close",
            "Thank you for helping clean up the ocean! Your efforts make a difference.",
            is_it_last=True,
            is_win = True
        )
        popup.display(screen)
        print("You Win!")
        pop_shown = True
        # pygame.quit()
        # sys.exit() 

    # Move camera
    if player_x > WIDTH // 2:
        camera_offset_x = player_x - WIDTH // 2

    # Check if player falls off the screen
    if player_y > HEIGHT and not lose_pop_shown:
        popup = Popup(
            parrot_image,
            "Great Effort!",
            "Retry",
            "You did a great job, but your luck was bad. Never give up!",
            is_it_last=True,
            is_win=False
        )
        lose_pop_shown = True
        reset_game()


    # Update animation for player
    animation_index += animation_speed
    if animation_index >= len(player_frames[current_animation]):
        animation_index = 0
    current_frame = player_frames[current_animation][int(animation_index)]

    # Update animation for bird
    bird_animation_index += bird_animation_speed
    if bird_animation_index >= len(bird_frames[bird_current_animation]):
        bird_animation_index = 0
    bird_current_frame = bird_frames[bird_current_animation][int(bird_animation_index)]

    # Update bird position to follow the player
    if bird_is_facing_right:
        bird_x = player_x + 50  # Keep bird near the player on the right
    else:
        bird_x = player_x - 50  # Keep bird near the player on the left
    bird_y = player_y - 30  # Keep bird above the player

    # Calculate percentage of objects collected
    
    # Fill the screen
    screen.blit(background, (0, 0))
    screen.blit(parrot_image, (chat_button.x, chat_button.y))
    draw_progress_bar(screen, collected_objects)
    for platform in platform_list:
        screen.blit(block_image, (platform.x - camera_offset_x, platform.y))

    # Draw objects
    for obj in object_list:
        if not obj.collected:
            screen.blit(obj.image, (obj.rect.x - camera_offset_x, obj.rect.y))


    # Draw player
    screen.blit(current_frame, (player_x - camera_offset_x, player_y))

    # Draw bird
    screen.blit(bird_current_frame, (bird_x - camera_offset_x, bird_y))
    popup.display(screen)
    pygame.display.update()
    clock.tick(60)

# Add main entry point to run the game directly
if __name__ == "__main__":
    # When run as a script, execute the sea level directly
    # First initialize pygame
    pygame.init()
    # Run the existing game code
    running = True
    collected_objects = 0
    lose_pop_shown = False
    pop_shown = False
    clock = pygame.time.Clock()
    
    # Set up the screen
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sea Level - Environmental Challenge")
    
    # Initialize necessary game variables and start the game loop
    platform_list = []
    NUM_PLATFORMS = 45
    player_x, player_y = 50, HEIGHT - 60 - 20 - 10
    player_y_velocity = 0
    on_ground = False
    camera_offset_x = 0
    animation_index = 0
    bird_animation_index = 0
    current_animation = "idle"
    bird_current_animation = "fly_right"
    is_facing_right = True
    bird_is_facing_right = True
    
    # Load all assets that are needed
    background = pygame.image.load("background_sea.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    block_image = pygame.image.load("Brick_Block.png")
    block_image = pygame.transform.scale(block_image, (70, 20))
    parrot_image = pygame.image.load("parrot.png")
    parrot_image = pygame.transform.scale(parrot_image, (50, 50))
    
    # Create needed game elements
    create_starting_ground()
    generate_platforms()
    generate_objects()
    
    # Create popup for instructions
    popup = Popup(
        parrot_image,
        "The sea is now under pollution and needs your help! Please help clean up by collecting trash and avoiding pollution sources.",
        "Help Now",
        "Thank you for your commitment! Collect 20 pieces of trash to make a difference. Let's protect our oceans!",
        is_it_last=True
    )
    
    # Define chat button
    chat_button = pygame.Rect(WIDTH - 60, 10, 50, 50)  # Chat button position
    
    # Start the game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Game loop code continues with movement, physics, drawing, etc.
        # This continues with the same game logic as before