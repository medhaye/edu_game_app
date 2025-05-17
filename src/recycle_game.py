import pygame
import sys
import os
import random
from chat import chat_page

# Get the assets path from environment variable
ASSETS_PATH = os.environ.get('ASSETS_PATH', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets'))
parrot_image = pygame.image.load(os.path.join(ASSETS_PATH, "parrot.png"))
parrot_image = pygame.transform.scale(parrot_image, (50, 50))
pygame.init()
class Popup:
    def __init__(self, image, messages, button_texts, is_it_last=False, is_win=False):
        self.image = image
        self.messages = messages  # List of messages to show sequentially
        self.button_texts = button_texts  # List of button texts for each message
        self.is_it_last = is_it_last
        self.is_win = is_win
        self.current_message_index = 0
        self.close_popup = False

        # Set up fonts
        self.font = pygame.font.SysFont("Arial", 24)
        self.button_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.text_color = (255, 255, 255)

        # Button properties
        self.button_width = 160
        self.button_height = 45
        self.button_rect = None

    def display(self, screen):
        if self.close_popup or self.current_message_index >= len(self.messages):
            return

        # Popup dimensions and position
        popup_width, popup_height = 600, 300
        popup_x = (screen.get_width() - popup_width) // 2
        popup_y = (screen.get_height() - popup_height) // 2

        # Semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Popup background
        pygame.draw.rect(screen, (40, 40, 40), (popup_x, popup_y, popup_width, popup_height), border_radius=10)
        
        # Image positioning
        image_x = popup_x + 20
        image_y = popup_y + (popup_height - self.image.get_height()) // 2
        screen.blit(self.image, (image_x, image_y))

        # Text positioning
        text_x = image_x + self.image.get_width() + 20
        text_y = popup_y + 30
        current_message = self.messages[self.current_message_index]

        # Wrap and display text
        wrapped_text = self.wrap_text(current_message, popup_width - 140)
        for line in wrapped_text:
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (text_x, text_y))
            text_y += self.font.get_height() + 8

        # Button setup
        button_text = self.button_texts[self.current_message_index]
        self.button_rect = pygame.Rect(
            popup_x + (popup_width - self.button_width) // 2,
            popup_y + popup_height - 70,
            self.button_width,
            self.button_height
        )
        
        # Draw button
        pygame.draw.rect(screen, (50, 150, 50), self.button_rect, border_radius=5)
        btn_text = self.button_font.render(button_text, True, (255, 255, 255))
        screen.blit(btn_text, (
            self.button_rect.x + (self.button_width - btn_text.get_width()) // 2,
            self.button_rect.y + (self.button_height - btn_text.get_height()) // 2
        ))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.button_rect:
            if self.button_rect.collidepoint(event.pos):
                if self.current_message_index < len(self.messages) - 1:
                    # Move to next message
                    self.current_message_index += 1
                else:
                    # Last message - close popup
                    self.close_popup = True

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        wrapped_lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = self.font.size(word + ' ')[0]
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                wrapped_lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
        wrapped_lines.append(' '.join(current_line))
        return wrapped_lines

# Usage example
popup = Popup(
    parrot_image,
    [
        "Different materials must be recycled in the correct bins!",
        "• Paper (Blue Bin): Newspapers, cardboard, and paper products.",
        "• Metals and Plastics (Yellow Bin): Bottles, bags, and packaging.",
        "• Glass (Green Bin): Glass bottles and jars.",
        "• Biodegradable (Brown Bin): Food waste and biodegradable items.",
        "Help keep the environment clean by sorting these materials correctly!"
    ],
    ["Next", "Next", "Next", "Next", "Next", "Start Sorting"],
    is_it_last=True
)

def recycle_game():
    # Set up screen
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recycle Game")
    chat_button = pygame.Rect(WIDTH - 60, 10, 50, 50)  # Chat button position
    # Load background
    background = pygame.image.load(os.path.join(ASSETS_PATH, "recycle_game_background.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Correct bin mapping
    correct_bins = {
        "plastic_bottle": "Plastic",
        "shopping_bag": "Plastic",
        "banana_peel": "Organic",
        "cigarette_filter": "Organic",
        "styrofoam_packaging": "Plastic",
        "glass_bottle": "Glass"
    }

    # Load bin images
    bin_images = {
        "Plastic": pygame.image.load(os.path.join(ASSETS_PATH, "plastic_bin.png")),
        "Organic": pygame.image.load(os.path.join(ASSETS_PATH, "organic_bin.png")),
        "Paper": pygame.image.load(os.path.join(ASSETS_PATH, "paper_bin.png")),
        "Glass": pygame.image.load(os.path.join(ASSETS_PATH, "glass_bin.png"))
    }

    # Load object images
    objects = {
        "plastic_bottle": pygame.image.load(os.path.join(ASSETS_PATH, "plastic_bottle.png")),
        "banana_peel": pygame.image.load(os.path.join(ASSETS_PATH, "banana_peel.png")),
        "shopping_bag": pygame.image.load(os.path.join(ASSETS_PATH, "shopping_bag.png")),
        "cigarette_filter": pygame.image.load(os.path.join(ASSETS_PATH, "cigarette_filter.png")),
        "styrofoam_packaging": pygame.image.load(os.path.join(ASSETS_PATH, "styrofoam_packaging.png")),
        "glass_bottle": pygame.image.load(os.path.join(ASSETS_PATH, "glass_bottle.png"))
    }

    # Scale images
    bin_width, bin_height = 100, 150
    obj_size = 50
    for key in bin_images:
        bin_images[key] = pygame.transform.scale(bin_images[key], (bin_width, bin_height))
    for key in objects:
        objects[key] = pygame.transform.scale(objects[key], (obj_size, obj_size))

    # Setup bins
    bins = [
        {"type": "Plastic", "items": [], "rect": pygame.Rect(100, 500, bin_width, bin_height)},
        {"type": "Organic", "items": [], "rect": pygame.Rect(250, 500, bin_width, bin_height)},
        {"type": "Paper", "items": [], "rect": pygame.Rect(400, 500, bin_width, bin_height)},
        {"type": "Glass", "items": [], "rect": pygame.Rect(550, 500, bin_width, bin_height)}
    ]

    # Distribute objects randomly
    object_keys = list(objects.keys())
    for _ in range(10):
        chosen_object = random.choice(object_keys)
        random.choice(bins)["items"].append(chosen_object)

    selected_bin = None
    font = pygame.font.SysFont("Arial", 24)
    obj_vertical_spacing = 55  # Space between stacked objects

    def draw_bins():
        for bin in bins:
            screen.blit(bin_images[bin["type"]], bin["rect"].topleft)

            # Draw objects with consistent positioning
            for idx, item in enumerate(bin["items"]):
                obj_x = bin["rect"].x + (bin_width - obj_size) // 2
                obj_y = bin["rect"].y - 60 - idx * obj_vertical_spacing
                screen.blit(objects[item], (obj_x, obj_y))

            # Draw selection border
            border_color = (0, 255, 0) if bin == selected_bin else (0, 255, 255)
            items_count = len(bin["items"])
            if items_count > 0:
                topmost_y = bin["rect"].y - 60 - (items_count - 1) * obj_vertical_spacing
                total_height = (bin["rect"].bottom - topmost_y)
                border_rect = pygame.Rect(bin["rect"].x - 5, topmost_y - 5, bin_width + 10, total_height + 10)
            else:
                border_rect = bin["rect"]
            pygame.draw.rect(screen, border_color, border_rect, 5, border_radius=8)
            # Add this at the top with other game variables
    congrats_popup = None
    congrats_shown = False

    # Game loop
    clock = pygame.time.Clock()
    while True:
        screen.blit(background, (0, 0))  # Draw background
        # Draw game elements
        draw_bins()
        popup.display(screen)
        screen.blit(parrot_image, (chat_button.x, chat_button.y))
        # Display instructions
        text = font.render("Click a bin to select, then another to move the top object", True, (50, 50, 50))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

        # Calculate score
        score = sum(1 for bin in bins for item in bin["items"] if correct_bins.get(item) == bin["type"])
        score_text = font.render(f"Score: {score}", True, (0, 200, 0))
                # Inside the game loop, after calculating the score:
        if score >= 10 and not congrats_shown:
            congrats_popup = Popup(
                parrot_image,
                ["Congratulations!", "You've sorted 10 items correctly!", "Keep up the great environmental work!"],
                ["Close", "Close", "Close"],
                is_it_last=True,
                is_win=True
            )
            congrats_shown = True

        # In the event handling section, add:
        if congrats_popup and not congrats_popup.close_popup:
            congrats_popup.handle_event(event)
            congrats_popup.display(screen)

        screen.blit(score_text, (20, 20))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if chat_button.collidepoint(event.pos):
                    # Open chat page when button is clicked
                    chat_page(screen, font)
                for bin in bins:
                    if bin["rect"].collidepoint(event.pos):
                        if selected_bin is None:
                            selected_bin = bin
                        else:
                            # Move object if valid
                            if selected_bin["items"] and bin != selected_bin:
                                top_item = selected_bin["items"].pop()
                                bin["items"].append(top_item)
                            selected_bin = None
            popup.handle_event(event)
        
        

        clock.tick(30)


# recycle_game()