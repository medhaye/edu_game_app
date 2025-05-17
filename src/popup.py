import pygame
from chat import chat_page

class Popup:
    def __init__(self, image, text, button_text, next_text, is_it_last=False, is_win=False):
        self.image = image
        self.text = text
        self.button_text = button_text
        self.next_text = next_text
        self.is_it_last = is_it_last
        self.showing_first_message = True
        self.is_win = is_win
        self.close_popup = False

        # Set up fonts
        self.font = pygame.font.SysFont("Arial", 24)
        self.button_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.text_color = (255, 255, 255)

        # Button properties
        self.button_width = 160
        self.button_height = 45
        self.button_x = 0  # Will be calculated in display()
        self.button_y = 0
        self.ask_button_width = 160
        self.ask_button_height = 45
        self.ask_button_x = 0  # Will be calculated in display()
        self.ask_button_y = 0

    def display(self, screen):
        if self.close_popup:
            return

        # Popup dimensions and position
        popup_width, popup_height = 600, 300
        popup_x = (screen.get_width() - popup_width) // 2
        popup_y = (screen.get_height() - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        # Semi-transparent background overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Popup background with border
        pygame.draw.rect(screen, (40, 40, 40), popup_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2, border_radius=10)

        # Calculate positions
        image_margin = 20
        text_margin = 20
        image_x = popup_x + image_margin
        image_y = popup_y + (popup_height - self.image.get_height()) // 2

        # Draw the image centered vertically
        screen.blit(self.image, (image_x, image_y))

        # Text area dimensions
        text_width = popup_width - self.image.get_width() - image_margin * 3
        text_x = image_x + self.image.get_width() + image_margin
        text_y = popup_y + 30

        # Wrap and render text
        wrapped_text = self.wrap_text(self.text, text_width)
        for line in wrapped_text:
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (text_x, text_y))
            text_y += self.font.get_height() + 8

        # Button positioning for "Next" or "Close"
        self.button_x = popup_x + (popup_width - self.button_width) // 2
        self.button_y = popup_y + popup_height - 120  # Adjusted to create space for new button

        # Button styling for "Next"/"Close"
        button_color = (50, 150, 50) if not self.is_it_last else (200, 50, 50)
        button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=5)

        # Button text for "Next" or "Close"
        button_text = self.button_font.render(self.button_text, True, (255, 255, 255))
        text_pos = (
            self.button_x + (self.button_width - button_text.get_width()) // 2,
            self.button_y + (self.button_height - button_text.get_height()) // 2
        )
        screen.blit(button_text, text_pos)

        # Button positioning for "Ask Question"
        self.ask_button_x = popup_x + (popup_width - self.ask_button_width) // 2
        self.ask_button_y = popup_y + popup_height - 170  # Adjusted to fit above the other button

        # Button styling for "Ask Question"
        ask_button_color = (50, 150, 200)  # Choose a color for the "Ask Question" button
        ask_button_rect = pygame.Rect(self.ask_button_x, self.ask_button_y, self.ask_button_width, self.ask_button_height)
        pygame.draw.rect(screen, ask_button_color, ask_button_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), ask_button_rect, 2, border_radius=5)

        # Button text for "Ask Question"
        ask_button_text = self.button_font.render("Ask Question", True, (255, 255, 255))
        ask_text_pos = (
            self.ask_button_x + (self.ask_button_width - ask_button_text.get_width()) // 2,
            self.ask_button_y + (self.ask_button_height - ask_button_text.get_height()) // 2
        )
        screen.blit(ask_button_text, ask_text_pos)

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

    def handle_event(self, event):
        if self.close_popup:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check for "Next"/"Close" button click
            button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
            if button_rect.collidepoint(mouse_x, mouse_y):
                if self.showing_first_message:
                    self.showing_first_message = False
                    self.text = self.next_text
                    self.button_text = "Next Level" if self.is_win else ("Next" if self.is_it_last else "Close")
                else:
                    if self.is_win:
                        # Instead of calling level_selection directly, set a flag and let the calling code handle it
                        self.close_popup = True
                        # Return True to indicate a win and level unlock should happen
                        return True
                    elif self.is_it_last:
                        self.close_popup = True

            # Check for "Ask Question" button click
            ask_button_rect = pygame.Rect(self.ask_button_x, self.ask_button_y, self.ask_button_width, self.ask_button_height)
            if ask_button_rect.collidepoint(mouse_x, mouse_y):
                font = pygame.font.Font(None, 40)
                WIDTH, HEIGHT = 800, 600
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                chat_page(screen, font)

