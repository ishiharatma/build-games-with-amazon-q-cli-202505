import pygame
import random
import math

# AWS color scheme
AWS_ORANGE = (255, 153, 0)
AWS_BLUE = (0, 124, 173)
AWS_DARK_BLUE = (35, 47, 62)
AWS_LIGHT_BLUE = (0, 160, 210)
AWS_LIGHT_GRAY = (240, 240, 240)
WHITE = (255, 255, 255)

def create_aws_background(width, height):
    """Create an AWS-themed background surface"""
    # Create the base surface with dark blue color
    surface = pygame.Surface((width, height))
    surface.fill(AWS_DARK_BLUE)
    
    # Add some cloud-like shapes
    for _ in range(10):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(50, 150)
        alpha = random.randint(10, 40)
        
        cloud = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(cloud, (255, 255, 255, alpha), (size//2, size//2), size//2)
        surface.blit(cloud, (x, y))
    
    # Add some AWS-style grid lines
    for i in range(0, width, 50):
        pygame.draw.line(surface, (255, 255, 255, 20), (i, 0), (i, height), 1)
    for i in range(0, height, 50):
        pygame.draw.line(surface, (255, 255, 255, 20), (0, i), (width, i), 1)
    
    # Add some AWS-style diagonal lines
    for i in range(0, width + height, 100):
        pygame.draw.line(surface, (255, 255, 255, 10), (i, 0), (0, i), 2)
    
    # Add AWS-style orange accent at the bottom
    pygame.draw.rect(surface, AWS_ORANGE, (0, height - 10, width, 10))
    
    return surface

def draw_aws_button(surface, text, font, x, y, width, height, active=False):
    """Draw an AWS-style button"""
    color = AWS_ORANGE if active else AWS_LIGHT_BLUE
    
    # Draw button background with rounded corners
    button_rect = pygame.Rect(x - width//2, y - height//2, width, height)
    pygame.draw.rect(surface, color, button_rect, border_radius=5)
    
    # Draw button text
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)
    
    return button_rect

def draw_aws_title(surface, text, font, x, y, color=AWS_ORANGE):
    """Draw an AWS-style title with orange underline"""
    # Draw the main text
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)
    
    # Draw the orange underline
    line_width = text_rect.width * 0.8
    pygame.draw.line(surface, color, 
                    (x - line_width//2, y + text_rect.height//2 + 5),
                    (x + line_width//2, y + text_rect.height//2 + 5), 3)
    
    return text_rect

def draw_aws_text_box(surface, text, font, x, y, width, height, bg_color=AWS_LIGHT_GRAY, text_color=AWS_DARK_BLUE):
    """Draw an AWS-style text box with multiple lines if needed"""
    # Create the text box background
    box_rect = pygame.Rect(x - width//2, y - height//2, width, height)
    pygame.draw.rect(surface, bg_color, box_rect, border_radius=5)
    
    # Split text into multiple lines if needed
    words = text.split(' ')
    lines = []
    current_line = words[0] if words else ""
    
    for word in words[1:]:
        test_line = current_line + ' ' + word
        test_surf = font.render(test_line, True, text_color)
        
        if test_surf.get_width() < width - 20:  # 20px padding
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:  # Add the last line if it exists
        lines.append(current_line)
    
    # Draw each line of text
    if lines:
        line_height = font.get_linesize()
        total_text_height = len(lines) * line_height
        start_y = y - (total_text_height // 2) + (line_height // 2)
        
        for i, line in enumerate(lines):
            text_surf = font.render(line, True, text_color)
            text_rect = text_surf.get_rect(center=(x, start_y + i * line_height))
            surface.blit(text_surf, text_rect)
    
    return box_rect
