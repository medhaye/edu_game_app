import pygame
import sys
import threading  # Permet d'exécuter l'IA sans bloquer l'interface
from risk_env_project_llm_rag import generate_answer  # Import du modèle IA
import os

# Get the assets path from environment variable
ASSETS_PATH = os.environ.get('ASSETS_PATH', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets'))  # Import du modèle IA

# Initialisation de Pygame
pygame.init()

# Charger les images
bg_image = pygame.image.load(os.path.join(ASSETS_PATH, "chat_background.png"))
send_icon = pygame.image.load(os.path.join(ASSETS_PATH, "send.png"))
back_icon = pygame.image.load(os.path.join(ASSETS_PATH, "back.png"))

# Redimensionner les icônes
send_icon = pygame.transform.scale(send_icon, (40, 40))
back_icon = pygame.transform.scale(back_icon, (40, 40))

# Configuration de la zone de saisie
min_input_height = 50  # Hauteur minimale
max_input_height = 150  # Hauteur maximale
padding = 15  # Marge intérieure
line_spacing = 20  # Espacement entre les lignes

# Fonction pour afficher du texte avec gestion des sauts de ligne
def draw_text_chat(surface, text, font, color, x, y, max_width):
    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    y_offset = 0
    for line in lines:
        text_obj = font.render(line, True, color)
        surface.blit(text_obj, (x, y + y_offset))
        y_offset += font.get_height()
    return y_offset

def chat_page(screen, main_font):
    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()
   
    # Position elements relative to screen size
    input_box = pygame.Rect(100, screen_height - 150, 500, 50)
    send_button = pygame.Rect(620, screen_height - 150, 50, 50)
    back_button = pygame.Rect(20, 20, 40, 40)
   
    # Font configuration
    chat_font = pygame.font.SysFont("Arial", 20)
    bubble_padding = 10
    max_bubble_width = 500
    scroll_offset = 0
    chat_scroll = 0

    # Colors and styling
    colors = {
        "chat_bubble": (50, 50, 50),
        "user_msg": (100, 180, 255),
        "bot_msg": (200, 200, 200),
        "input_bg": (40, 40, 40),
        "border": pygame.Color('dodgerblue2'),
        "text": (255, 255, 255)
    }

    active = False
    text = ''
    messages = [("How can I help you?", colors["bot_msg"])]

    def get_bot_response(question):
        messages.append(("Thinking...", colors["bot_msg"]))
        response = generate_answer(question)
        print(f"Generated response: {response} (Type: {type(response)})")  # Debugging print

        messages.pop()
        
        if response:  # Ensure response is not None or empty
            messages.append((response, colors["bot_msg"]))
            print(messages)
        else:
            messages.append(("I couldn't generate a response.", colors["bot_msg"]))

    def calculate_text_height(text, font, max_width):
        words = text.split(' ')
        lines = []
        line = ''
        for word in words:
            test_line = f'{line} {word}'.strip()
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return len(lines) * font.get_height()

    while True:
        # Background setup
        bg_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "chat_background.png")),
                                        (screen_width, screen_height))
        screen.blit(bg_image, (0, 0))
        screen.blit(back_icon, back_button.topleft)

        # Calculate message display area
        message_area_height = screen_height - input_box.height - 100
        y_offset = 50 + chat_scroll

        # Display messages with auto-sizing bubbles
        for msg, color in messages:
            text_height = calculate_text_height(msg, chat_font, max_bubble_width - 2*bubble_padding)
            bubble_height = text_height + 2*bubble_padding
           
            # if y_offset + bubble_height > input_box.top - 20:
            #     break

            # Draw chat bubble
            bubble_rect = pygame.Rect(80, y_offset, 540, bubble_height)
            pygame.draw.rect(screen, colors["chat_bubble"], bubble_rect, border_radius=10)
           
            # Draw wrapped text
            draw_text_chat(screen, msg, chat_font, color,
                         bubble_rect.x + bubble_padding,
                         bubble_rect.y + bubble_padding,
                         max_bubble_width - 2*bubble_padding)
           
            y_offset += bubble_height + 10

        # Input box with scrolling text
        pygame.draw.rect(screen, colors["input_bg"], input_box, border_radius=10)
        pygame.draw.rect(screen, colors["border"] if active else (100, 100, 100),
                       input_box, 2, border_radius=10)

        # Text rendering with clipping
        txt_surface = chat_font.render(text, True, colors["text"])
        text_width = txt_surface.get_width()
       
        # Handle text scrolling
        if text_width > input_box.width - 20:
            scroll_offset = max(0, text_width - (input_box.width - 20))
            src_rect = pygame.Rect(scroll_offset, 0, input_box.width - 20, 50)
        else:
            scroll_offset = 0
            src_rect = txt_surface.get_rect()

        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 15), src_rect)
        screen.blit(send_icon, send_button.topleft)

        pygame.display.flip()
        clock.tick(30)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if send_button.collidepoint(event.pos) and text.strip():
                    messages.append((text, colors["user_msg"]))
                    threading.Thread(target=get_bot_response, args=(text,), daemon=True).start()
                    text = ''
                    chat_scroll = -50

                if back_button.collidepoint(event.pos):
                    return

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        text += "\n"
                    elif text.strip():
                        messages.append((text, colors["user_msg"]))
                        threading.Thread(target=get_bot_response, args=(text,), daemon=True).start()
                        text = ''
                        chat_scroll = -50
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            # Mouse wheel scrolling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: chat_scroll += 20
                if event.button == 5: chat_scroll -= 20



# import pygame
# import sys
# # Load assets
# bg_image = pygame.image.load(os.path.join(ASSETS_PATH, "chat_background.png"))  # Load background image
# send_button = pygame.image.load(os.path.join(ASSETS_PATH, "send.png"))  # Load send icon
# back_icon = pygame.image.load(os.path.join(ASSETS_PATH, "back.png"))  # Load back icon

# # Resize icons
# send_icon = pygame.transform.scale(send_icon, (40, 40))
# back_icon = pygame.transform.scale(back_icon, (40, 40))

# # Function to draw text with word wrapping
# def draw_text_chat(surface, text, font, color, x, y, max_width):
#     words = text.split(' ')
#     lines = []
#     line = ''
#     for word in words:
#         test_line = line + word + ' '
#         if font.size(test_line)[0] < max_width:
#             line = test_line
#         else:
#             lines.append(line)
#             line = word + ' '
#     lines.append(line)

#     y_offset = 0
#     for line in lines:
#         text_obj = font.render(line, True, color)
#         surface.blit(text_obj, (x, y + y_offset))
#         y_offset += font.get_height()
#     return y_offset

# # Chat Page
# def chat_page(screen, font):
#     clock = pygame.time.Clock()
#     screen_width, screen_height = screen.get_size()
    
#     # Position input at bottom with proper spacing
#     input_box = pygame.Rect(100, screen_height - 70, 500, 50)  # 70px from bottom
#     send_button = pygame.Rect(620, screen_height - 70, 50, 50)
#     back_button = pygame.Rect(20, 20, 40, 40)
    
#     # Create smaller font
#     chat_font = pygame.font.SysFont("Arial", 20)
#     bubble_padding = 10
#     max_width = 500
#     scroll_offset = 0  # For text input scrolling

#     # Colors (keep existing)
#     chat_bubble_color = (50, 50, 50)
#     user_msg_color = (100, 180, 255)
#     bot_msg_color = (200, 200, 200)
#     input_bg_color = (40, 40, 40)
#     border_color = pygame.Color('dodgerblue2')

#     active = False
#     text = ''
#     messages = [("Welcome to the chat!", bot_msg_color)]

#     while True:
#         bg_image = pygame.transform.scale(pygame.image.load("chat_background.png"), 
#                                         (screen_width, screen_height))
#         screen.blit(bg_image, (0, 0))
        
#         # Draw back button
#         screen.blit(back_icon, back_button.topleft)
        
#         # Calculate available space for messages (above input box)
#         messages_height = screen_height - input_box.height - 100  # 100px margin
#         y_offset = max(50, messages_height - len(messages)*60)  # Auto-scroll
        
#         # Render chat messages
#         for msg, color in messages:
#             # Measure text height
#             temp_surface = pygame.Surface((1, 1))
#             text_height = draw_text_chat(temp_surface, msg, chat_font, (0,0,0), 
#                                        0, 0, max_width - 2*bubble_padding)
            
#             # Create bubble
#             bubble_rect = pygame.Rect(
#                 80, 
#                 y_offset, 
#                 540, 
#                 text_height + bubble_padding * 2
#             )
            
#             # Only draw visible bubbles
#             if bubble_rect.bottom > input_box.top - 20:
#                 break
            
#             pygame.draw.rect(screen, chat_bubble_color, bubble_rect, border_radius=10)
#             draw_text_chat(screen, msg, chat_font, color, 
#                          bubble_rect.x + bubble_padding, 
#                          bubble_rect.y + bubble_padding, 
#                          max_width - 2*bubble_padding)
            
#             y_offset += bubble_rect.height + 10

#         # Draw input box with scrolling text
#         pygame.draw.rect(screen, input_bg_color, input_box, border_radius=10)
#         pygame.draw.rect(screen, border_color if active else (100, 100, 100), 
#                        input_box, 2, border_radius=10)
        
#         # Render text with clipping
#         txt_surface = chat_font.render(text, True, (255, 255, 255))
#         text_width = txt_surface.get_width()
        
#         # Calculate scroll position
#         if text_width > input_box.width - 20:
#             scroll_offset = max(0, text_width - (input_box.width - 20))
#             src_rect = pygame.Rect(scroll_offset, 0, 
#                                  input_box.width - 20, txt_surface.get_height())
#         else:
#             scroll_offset = 0
#             src_rect = pygame.Rect(0, 0, text_width, txt_surface.get_height())
        
#         # Draw clipped text
#         screen.blit(txt_surface, (input_box.x + 10, input_box.y + 15), src_rect)
        
#         # Draw send button
#         pygame.draw.rect(screen, (255, 255, 255), send_button, border_radius=10)
#         screen.blit(send_icon, (send_button.x + 5, send_button.y + 5))
        
#         pygame.display.flip()
#         clock.tick(30)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if input_box.collidepoint(event.pos):
#                     active = True
#                 else:
#                     active = False
#                 if send_button.collidepoint(event.pos) and text.strip():
#                     messages.append((text, user_msg_color))
#                     responses = ["Interesting!", "Tell me more!", "Nice!", "Let's chat!"]
#                     messages.append((responses[len(messages) % len(responses)], bot_msg_color))
#                     text = ''
#                 if back_button.collidepoint(event.pos):
#                     return

#             if event.type == pygame.KEYDOWN and active:
#                 if event.key == pygame.K_RETURN and text.strip():
#                     messages.append((text, user_msg_color))
#                     responses = ["Interesting!", "Tell me more!", "Nice!", "Let's chat!"]
#                     messages.append((responses[len(messages) % len(responses)], bot_msg_color))
#                     text = ''
#                 elif event.key == pygame.K_BACKSPACE:
#                     text = text[:-1]
#                 else:
#                     text += event.unicode
