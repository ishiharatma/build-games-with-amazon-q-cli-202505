import pygame
import sys
import random
import math
import os
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
GRID_SIZE = 40
GRID_WIDTH = 6
GRID_HEIGHT = 14
BOARD_LEFT = 50  # Move board to the left side
BOARD_TOP = (SCREEN_HEIGHT - GRID_HEIGHT * GRID_SIZE) // 2
FPS = 60

# Animation constants
CLEAR_BLINK_FRAMES = 20  # Increased number of frames for blinking animation (slower)
CLEAR_DELAY = 800        # Increased milliseconds between chain reactions (slower)
POP_ANIMATION_FRAMES = 10 # Increased number of frames for pop animation (slower)
CHAIN_DISPLAY_DURATION = 1500  # Duration to display chain text in milliseconds

# Game states
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_CONTINUE = 3
STATE_FADE_OUT = 4

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BACKGROUND_COLOR = (240, 240, 240)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (173, 216, 230)

# AWS Service colors (for reference)
# Red: CloudTrail
# Blue: Aurora
# Yellow: EC2
# Green: S3
# Purple: Amazon VPC

# Service types
SERVICE_CLOUDTRAIL = 0  # Red
SERVICE_AURORA = 1      # Blue
SERVICE_EC2 = 2         # Yellow
SERVICE_S3 = 3          # Green
SERVICE_VPC = 4         # Purple

# Game over animation constants
GAME_OVER_AMPLITUDE = 10  # Amplitude of the game over text wobble
GAME_OVER_SPEED = 2       # Speed of the game over text wobble
GAME_OVER_TEXT = "Amazon Q～"  # Game over text
GAME_OVER_FALL_DURATION = 2000  # Duration for game over text to fall (milliseconds)

# Continue screen constants
CONTINUE_COUNTDOWN = 10  # Seconds for countdown
CONTINUE_OPTION_YES = 0
CONTINUE_OPTION_NO = 1

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AWS Puyo Puyo')

# Load images
def load_images():
    images = {}
    service_names = ['cloudtrail', 'aurora', 'ec2', 's3', 'vpc']
    
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Check if images exist, if not create placeholder colored circles
    for i, name in enumerate(service_names):
        image_path = f'images/{name}.png'
        if os.path.exists(image_path):
            images[i] = pygame.image.load(image_path)
            images[i] = pygame.transform.scale(images[i], (GRID_SIZE - 4, GRID_SIZE - 4))
        else:
            # Create colored circle as placeholder
            color_map = {
                0: (220, 60, 60),    # Red for CloudTrail
                1: (60, 60, 220),    # Blue for Aurora
                2: (220, 220, 60),   # Yellow for EC2
                3: (60, 220, 60),    # Green for S3
                4: (180, 60, 220)    # Purple for VPC
            }
            
            # Create a surface for the circle
            img = pygame.Surface((GRID_SIZE - 4, GRID_SIZE - 4), pygame.SRCALPHA)
            pygame.draw.circle(img, color_map[i], (GRID_SIZE // 2 - 2, GRID_SIZE // 2 - 2), GRID_SIZE // 2 - 2)
            images[i] = img
    
    return images

# Font setup
try:
    # Try to use Japanese fonts
    font = pygame.font.SysFont('MS Gothic', 24)  # Windows Japanese font
    large_font = pygame.font.SysFont('MS Gothic', 36)
    game_over_font = pygame.font.SysFont('MS Gothic', 48)  # Larger font for game over
    title_font = pygame.font.SysFont('MS Gothic', 72)  # Large font for title
    countdown_font = pygame.font.SysFont('MS Gothic', 96)  # Extra large font for countdown
except:
    # Fallback to default fonts
    font = pygame.font.SysFont('Arial', 24)
    large_font = pygame.font.SysFont('Arial', 36)
    game_over_font = pygame.font.SysFont('Arial', 48)
    title_font = pygame.font.SysFont('Arial', 72)
    countdown_font = pygame.font.SysFont('Arial', 96)

# Load images
images = load_images()

# Background elements
cloud_positions = []
for _ in range(10):
    cloud_positions.append([
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT // 2),
        random.randint(30, 70),  # Size
        random.random() * 0.5 + 0.2  # Speed
    ])

# AWS icons for title screen
aws_icons = []
for i in range(20):  # Create 20 random AWS icons
    service_type = random.randint(0, 4)
    aws_icons.append({
        'type': service_type,
        'x': random.randint(0, SCREEN_WIDTH),
        'y': random.randint(0, SCREEN_HEIGHT),
        'speed': random.random() * 1 + 0.5,
        'size': random.random() * 0.5 + 0.5  # Scale factor
    })

# Define screen functions
def draw_background():
    # Create a gradient background
    for y in range(SCREEN_HEIGHT):
        # Gradient from light blue at top to white at bottom
        ratio = y / SCREEN_HEIGHT
        color = (
            int(LIGHT_BLUE[0] + (WHITE[0] - LIGHT_BLUE[0]) * ratio),
            int(LIGHT_BLUE[1] + (WHITE[1] - LIGHT_BLUE[1]) * ratio),
            int(LIGHT_BLUE[2] + (WHITE[2] - LIGHT_BLUE[2]) * ratio)
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
    
    # Draw AWS-style clouds
    for cloud in cloud_positions:
        x, y, size, speed = cloud
        
        # Draw a fluffy cloud
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), size)
        pygame.draw.circle(screen, WHITE, (int(x - size*0.6), int(y + size*0.2)), int(size*0.7))
        pygame.draw.circle(screen, WHITE, (int(x + size*0.6), int(y + size*0.2)), int(size*0.7))
        
        # Move cloud
        cloud[0] -= speed
        if cloud[0] < -size:
            cloud[0] = SCREEN_WIDTH + size
            cloud[1] = random.randint(0, SCREEN_HEIGHT // 2)
            cloud[2] = random.randint(30, 70)
            cloud[3] = random.random() * 0.5 + 0.2
    
    # Draw AWS logo-inspired elements
    # Orange arrow
    arrow_points = [
        (SCREEN_WIDTH - 100, 30),
        (SCREEN_WIDTH - 60, 30),
        (SCREEN_WIDTH - 80, 50)
    ]
    pygame.draw.polygon(screen, ORANGE, arrow_points)
    
    # Draw some decorative elements that resemble AWS services
    pygame.draw.rect(screen, LIGHT_GRAY, (20, 20, 40, 40), 2)
    pygame.draw.circle(screen, LIGHT_GRAY, (100, 40), 20, 2)

def draw_title_screen():
    # Draw AWS-themed background
    draw_background()
    
    # Draw floating AWS icons
    for icon in aws_icons:
        # Move icons
        icon['y'] += icon['speed']
        if icon['y'] > SCREEN_HEIGHT:
            icon['y'] = -50
            icon['x'] = random.randint(0, SCREEN_WIDTH)
        
        # Draw the icon
        img = images[icon['type']]
        size = int(GRID_SIZE * icon['size'])
        scaled_img = pygame.transform.scale(img, (size, size))
        screen.blit(scaled_img, (icon['x'], icon['y']))
    
    # Draw title text with orange outline and white fill
    title_text = "あまぷよ！！"
    
    # First render the text in white
    title_surface = title_font.render(title_text, True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    
    # Create orange outline
    outline_size = 4
    for dx in range(-outline_size, outline_size + 1):
        for dy in range(-outline_size, outline_size + 1):
            if dx != 0 or dy != 0:
                outline_rect = title_rect.copy()
                outline_rect.x += dx
                outline_rect.y += dy
                outline_text = title_font.render(title_text, True, ORANGE)
                screen.blit(outline_text, outline_rect)
    
    # Draw the main white text on top
    screen.blit(title_surface, title_rect)
    
    # Draw press space instruction with black outline
    space_text = font.render("スペースキーを押してスタート", True, WHITE)
    space_rect = space_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
    
    # Add black outline to the text
    outline_size = 2
    for dx in range(-outline_size, outline_size + 1):
        for dy in range(-outline_size, outline_size + 1):
            if dx != 0 or dy != 0:
                outline_rect = space_rect.copy()
                outline_rect.x += dx
                outline_rect.y += dy
                outline_text = font.render("スペースキーを押してスタート", True, BLACK)
                screen.blit(outline_text, outline_rect)
    
    # Draw the main white text on top
    screen.blit(space_text, space_rect)
    
    # Make the text blink
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        pygame.draw.rect(screen, WHITE, space_rect, 2)

def draw_continue_screen():
    global continue_option, continue_start_time, game_state, fade_alpha, game_over_start_time
    
    # Draw background with semi-transparency
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(s, (0, 0))
    
    # Calculate game over text position - falling animation
    elapsed_time = min(GAME_OVER_FALL_DURATION, pygame.time.get_ticks() - game_over_start_time)
    progress = elapsed_time / GAME_OVER_FALL_DURATION
    
    # Start from above the screen and fall to the center
    start_y = -50
    end_y = SCREEN_HEIGHT // 3
    current_y = start_y + (end_y - start_y) * progress
    
    # Calculate wobble effect for game over text
    wobble_x = math.sin(pygame.time.get_ticks() / 500 * GAME_OVER_SPEED) * GAME_OVER_AMPLITUDE
    
    # Create a stylized game over text with orange outline and white fill
    game_over_text = game_over_font.render(GAME_OVER_TEXT, True, WHITE)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2 + wobble_x, current_y))
    
    # Create orange outline
    outline_size = 3
    for dx in range(-outline_size, outline_size + 1):
        for dy in range(-outline_size, outline_size + 1):
            if dx != 0 or dy != 0:
                outline_rect = game_over_text.get_rect(
                    center=(SCREEN_WIDTH // 2 + wobble_x + dx, current_y + dy)
                )
                outline_text = game_over_font.render(GAME_OVER_TEXT, True, ORANGE)
                screen.blit(outline_text, outline_rect)
    
    # Draw the main white text on top
    screen.blit(game_over_text, text_rect)
    
    # Only show continue options after the game over text has finished falling
    if elapsed_time >= GAME_OVER_FALL_DURATION:
        # Draw continue text
        continue_text = "コンティニューする？"
        continue_surface = large_font.render(continue_text, True, WHITE)
        continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(continue_surface, continue_rect)
        
        # Draw options
        yes_text = "はい"
        no_text = "いいえ"
        
        yes_color = ORANGE if continue_option == CONTINUE_OPTION_YES else WHITE
        no_color = ORANGE if continue_option == CONTINUE_OPTION_NO else WHITE
        
        yes_surface = font.render(yes_text, True, yes_color)
        no_surface = font.render(no_text, True, no_color)
        
        yes_rect = yes_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        no_rect = no_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        
        screen.blit(yes_surface, yes_rect)
        screen.blit(no_surface, no_rect)
        
        # Start countdown only after the game over text has finished falling
        if continue_start_time == 0:
            continue_start_time = pygame.time.get_ticks()
        
        # Draw countdown
        if continue_start_time > 0:
            elapsed = (pygame.time.get_ticks() - continue_start_time) // 1000
            remaining = max(0, CONTINUE_COUNTDOWN - elapsed)
            
            # If countdown reached 0, start fade out
            if remaining == 0 and game_state != STATE_FADE_OUT:
                game_state = STATE_FADE_OUT
                fade_alpha = 0
            
            # Draw countdown with pop style
            count_text = str(remaining)
            count_surface = countdown_font.render(count_text, True, WHITE)
            
            # Add pulsating effect based on the decimal part of the time
            decimal_part = (pygame.time.get_ticks() - continue_start_time) % 1000 / 1000.0
            scale_factor = 1.0 + 0.2 * math.sin(decimal_part * 2 * math.pi)
            
            scaled_width = int(count_surface.get_width() * scale_factor)
            scaled_height = int(count_surface.get_height() * scale_factor)
            scaled_surface = pygame.transform.scale(count_surface, (scaled_width, scaled_height))
            
            count_rect = scaled_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
            
            # Draw orange outline
            outline_size = 3
            for dx in range(-outline_size, outline_size + 1):
                for dy in range(-outline_size, outline_size + 1):
                    if dx != 0 or dy != 0:
                        outline_rect = count_rect.copy()
                        outline_rect.x += dx
                        outline_rect.y += dy
                        outline_text = pygame.transform.scale(countdown_font.render(count_text, True, ORANGE), 
                                                            (scaled_width, scaled_height))
                        screen.blit(outline_text, outline_rect)
            
            # Draw the main white text on top
            screen.blit(scaled_surface, count_rect)
        
        # Add pulsating effect based on the decimal part of the time
        decimal_part = (pygame.time.get_ticks() - continue_start_time) % 1000 / 1000.0
        scale_factor = 1.0 + 0.2 * math.sin(decimal_part * 2 * math.pi)
        
        scaled_width = int(count_surface.get_width() * scale_factor)
        scaled_height = int(count_surface.get_height() * scale_factor)
        scaled_surface = pygame.transform.scale(count_surface, (scaled_width, scaled_height))
        
        count_rect = scaled_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        
        # Draw orange outline
        outline_size = 3
        for dx in range(-outline_size, outline_size + 1):
            for dy in range(-outline_size, outline_size + 1):
                if dx != 0 or dy != 0:
                    outline_rect = count_rect.copy()
                    outline_rect.x += dx
                    outline_rect.y += dy
                    outline_text = pygame.transform.scale(countdown_font.render(count_text, True, ORANGE), 
                                                        (scaled_width, scaled_height))
                    screen.blit(outline_text, outline_rect)
        
        # Draw the main white text on top
        screen.blit(scaled_surface, count_rect)

def draw_fade_out():
    global fade_alpha, game_state
    
    # Increase alpha for fade effect
    fade_alpha += 3  # Adjust speed of fade
    if fade_alpha >= 255:
        fade_alpha = 255
        game_state = STATE_TITLE  # Return to title screen after fade
    
    # Draw black overlay with increasing opacity
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    s.fill(BLACK)
    s.set_alpha(fade_alpha)
    screen.blit(s, (0, 0))

class Puyo:
    def __init__(self, service_type, x, y):
        self.service_type = service_type
        self.x = x
        self.y = y
        self.wobble_phase = 0
        self.wobble_speed = 5
        self.wobble_amount = 3
        self.is_wobbling = False
        self.wobble_start_time = 0
        self.wobble_duration = 500  # milliseconds
        self.is_clearing = False    # Whether this puyo is being cleared
        self.blink_frame = 0        # Current frame of blink animation
        self.pop_scale = 1.0        # Scale for pop animation (1.0 = normal size)
        self.pop_alpha = 255        # Alpha for pop animation (255 = fully opaque)

    def start_wobble(self):
        self.is_wobbling = True
        self.wobble_start_time = pygame.time.get_ticks()
        self.wobble_phase = random.random() * 2 * math.pi  # Random starting phase

    def update_wobble(self):
        if not self.is_wobbling:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.wobble_start_time > self.wobble_duration:
            self.is_wobbling = False
            return
        
        # Update wobble phase
        self.wobble_phase += 0.1

    def draw(self, surface, offset_x=0, offset_y=0):
        wobble_x = 0
        wobble_y = 0
        
        # Calculate wobble effect if active
        if self.is_wobbling:
            wobble_x = math.sin(self.wobble_phase) * self.wobble_amount
            wobble_y = math.cos(self.wobble_phase) * self.wobble_amount
            self.update_wobble()
        
        # Calculate position
        x_pos = BOARD_LEFT + (self.x + offset_x) * GRID_SIZE + wobble_x
        y_pos = BOARD_TOP + (self.y + offset_y) * GRID_SIZE + wobble_y
        
        # If this puyo is being cleared, make it blink
        if self.is_clearing:
            # Skip drawing on certain frames to create blinking effect
            if (self.blink_frame // 3) % 2 == 0:
                return
        
        # Get the image
        img = images[self.service_type].copy()
        
        # Apply pop animation if needed
        if self.pop_scale != 1.0:
            # Scale the image
            orig_size = img.get_width()
            new_size = int(orig_size * self.pop_scale)
            if new_size > 0:  # Prevent scaling to zero
                img = pygame.transform.scale(img, (new_size, new_size))
            
            # Set transparency
            img.set_alpha(self.pop_alpha)
        
        # Draw the image
        img_rect = img.get_rect(center=(x_pos + GRID_SIZE // 2, y_pos + GRID_SIZE // 2))
        surface.blit(img, img_rect)

class PuyoPair:
    def __init__(self):
        # Randomly select service types for the pair
        self.main_puyo = Puyo(random.randint(0, 4), GRID_WIDTH // 2, 0)
        self.sub_puyo = Puyo(random.randint(0, 4), GRID_WIDTH // 2, 1)
        self.rotation = 0  # 0: sub below, 1: sub right, 2: sub above, 3: sub left
        self.drop_speed = 0  # For fast drop
        self.last_drop_time = 0

    def rotate_clockwise(self):
        # Save original positions
        orig_main_x, orig_main_y = self.main_puyo.x, self.main_puyo.y
        orig_sub_x, orig_sub_y = self.sub_puyo.x, self.sub_puyo.y
        orig_rotation = self.rotation
        
        # Calculate new position based on rotation
        if self.rotation == 0:  # sub is below -> move to right
            self.sub_puyo.x = self.main_puyo.x + 1
            self.sub_puyo.y = self.main_puyo.y
            self.rotation = 1
        elif self.rotation == 1:  # sub is right -> move to above
            self.sub_puyo.x = self.main_puyo.x
            self.sub_puyo.y = self.main_puyo.y - 1
            self.rotation = 2
        elif self.rotation == 2:  # sub is above -> move to left
            self.sub_puyo.x = self.main_puyo.x - 1
            self.sub_puyo.y = self.main_puyo.y
            self.rotation = 3
        elif self.rotation == 3:  # sub is left -> move to below
            self.sub_puyo.x = self.main_puyo.x
            self.sub_puyo.y = self.main_puyo.y + 1
            self.rotation = 0

        # Check if rotation is valid
        if not is_valid_position(self):
            # Try wall kick - move the whole piece left or right if it's against a wall
            if self.sub_puyo.x < 0:
                # Move right
                self.main_puyo.x += 1
                self.sub_puyo.x += 1
            elif self.sub_puyo.x >= GRID_WIDTH:
                # Move left
                self.main_puyo.x -= 1
                self.sub_puyo.x -= 1
            elif self.sub_puyo.y < 0:
                # Move down
                self.main_puyo.y += 1
                self.sub_puyo.y += 1
            elif self.sub_puyo.y >= GRID_HEIGHT:
                # Move up
                self.main_puyo.y -= 1
                self.sub_puyo.y -= 1
            
            # Check if the wall kick worked
            if not is_valid_position(self):
                # Revert to original position
                self.main_puyo.x, self.main_puyo.y = orig_main_x, orig_main_y
                self.sub_puyo.x, self.sub_puyo.y = orig_sub_x, orig_sub_y
                self.rotation = orig_rotation

    def rotate_counterclockwise(self):
        # Save original positions
        orig_main_x, orig_main_y = self.main_puyo.x, self.main_puyo.y
        orig_sub_x, orig_sub_y = self.sub_puyo.x, self.sub_puyo.y
        orig_rotation = self.rotation
        
        # Opposite of rotate_clockwise
        if self.rotation == 0:  # sub is below -> move to left
            self.sub_puyo.x = self.main_puyo.x - 1
            self.sub_puyo.y = self.main_puyo.y
            self.rotation = 3
        elif self.rotation == 3:  # sub is left -> move to above
            self.sub_puyo.x = self.main_puyo.x
            self.sub_puyo.y = self.main_puyo.y - 1
            self.rotation = 2
        elif self.rotation == 2:  # sub is above -> move to right
            self.sub_puyo.x = self.main_puyo.x + 1
            self.sub_puyo.y = self.main_puyo.y
            self.rotation = 1
        elif self.rotation == 1:  # sub is right -> move to below
            self.sub_puyo.x = self.main_puyo.x
            self.sub_puyo.y = self.main_puyo.y + 1
            self.rotation = 0
            
        # Check if rotation is valid
        if not is_valid_position(self):
            # Try wall kick - move the whole piece left or right if it's against a wall
            if self.sub_puyo.x < 0:
                # Move right
                self.main_puyo.x += 1
                self.sub_puyo.x += 1
            elif self.sub_puyo.x >= GRID_WIDTH:
                # Move left
                self.main_puyo.x -= 1
                self.sub_puyo.x -= 1
            elif self.sub_puyo.y < 0:
                # Move down
                self.main_puyo.y += 1
                self.sub_puyo.y += 1
            elif self.sub_puyo.y >= GRID_HEIGHT:
                # Move up
                self.main_puyo.y -= 1
                self.sub_puyo.y -= 1
            
            # Check if the wall kick worked
            if not is_valid_position(self):
                # Revert to original position
                self.main_puyo.x, self.main_puyo.y = orig_main_x, orig_main_y
                self.sub_puyo.x, self.sub_puyo.y = orig_sub_x, orig_sub_y
                self.rotation = orig_rotation

    def move_left(self):
        self.main_puyo.x -= 1
        self.sub_puyo.x -= 1
        if not is_valid_position(self):
            self.main_puyo.x += 1
            self.sub_puyo.x += 1

    def move_right(self):
        self.main_puyo.x += 1
        self.sub_puyo.x += 1
        if not is_valid_position(self):
            self.main_puyo.x -= 1
            self.sub_puyo.x -= 1

    def move_down(self):
        self.main_puyo.y += 1
        self.sub_puyo.y += 1
        if not is_valid_position(self):
            self.main_puyo.y -= 1
            self.sub_puyo.y -= 1
            return False  # Cannot move down
        return True  # Successfully moved down
        
    def start_fast_drop(self):
        self.drop_speed = 30  # Very fast drop speed
        
    def stop_fast_drop(self):
        self.drop_speed = 0
        
    def hard_drop(self):
        # Move down until it can't move anymore
        drop_distance = 0
        while self.move_down():
            drop_distance += 1
        return drop_distance

    def draw(self, surface):
        # Draw the landing prediction
        self.draw_landing_prediction(surface)
        
        # Draw the actual piece
        self.main_puyo.draw(surface)
        self.sub_puyo.draw(surface)
        
    def draw_landing_prediction(self, surface):
        # Create a copy of the current piece to find landing position
        temp_main = Puyo(self.main_puyo.service_type, self.main_puyo.x, self.main_puyo.y)
        temp_sub = Puyo(self.sub_puyo.service_type, self.sub_puyo.x, self.sub_puyo.y)
        temp_piece = PuyoPair()
        temp_piece.main_puyo = temp_main
        temp_piece.sub_puyo = temp_sub
        
        # Move the temp piece down until it can't move anymore
        while True:
            temp_piece.main_puyo.y += 1
            temp_piece.sub_puyo.y += 1
            if not is_valid_position(temp_piece):
                temp_piece.main_puyo.y -= 1
                temp_piece.sub_puyo.y -= 1
                break
        
        # Draw small colored circles at landing position with transparency
        for puyo in [temp_piece.main_puyo, temp_piece.sub_puyo]:
            x_pos = BOARD_LEFT + puyo.x * GRID_SIZE + GRID_SIZE // 2
            y_pos = BOARD_TOP + puyo.y * GRID_SIZE + GRID_SIZE // 2
            
            # Color map for the prediction circles
            color_map = {
                0: (220, 60, 60, 100),    # Red for CloudTrail
                1: (60, 60, 220, 100),    # Blue for Aurora
                2: (220, 220, 60, 100),   # Yellow for EC2
                3: (60, 220, 60, 100),    # Green for S3
                4: (180, 60, 220, 100)    # Purple for VPC
            }
            
            # Draw a small circle with the corresponding color
            circle_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, color_map[puyo.service_type], 
                              (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 4)
            surface.blit(circle_surface, (x_pos - GRID_SIZE // 2, y_pos - GRID_SIZE // 2))

def is_valid_position(piece):
    # Check if the piece is within bounds and not colliding with placed puyos
    for puyo in [piece.main_puyo, piece.sub_puyo]:
        x, y = puyo.x, puyo.y
        
        # Check boundaries
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
            return False
        
        # Check collision with placed puyos
        if y >= 0 and board[y][x] is not None:
            # Special case: if this position was just cleared, allow placement
            if hasattr(board[y][x], 'is_clearing') and board[y][x].is_clearing:
                continue
            return False
    
    return True

def create_new_piece():
    global current_piece, next_piece
    if next_piece is None:
        next_piece = PuyoPair()
    
    current_piece = next_piece
    next_piece = PuyoPair()

def lock_piece():
    global board, score
    
    # Place the main puyo
    if 0 <= current_piece.main_puyo.y < GRID_HEIGHT and 0 <= current_piece.main_puyo.x < GRID_WIDTH:
        board[current_piece.main_puyo.y][current_piece.main_puyo.x] = current_piece.main_puyo
        current_piece.main_puyo.start_wobble()  # Start wobble animation when landing
    
    # Place the sub puyo
    if 0 <= current_piece.sub_puyo.y < GRID_HEIGHT and 0 <= current_piece.sub_puyo.x < GRID_WIDTH:
        board[current_piece.sub_puyo.y][current_piece.sub_puyo.x] = current_piece.sub_puyo
        current_piece.sub_puyo.start_wobble()  # Start wobble animation when landing

def apply_gravity():
    moved = False
    
    # Process each column separately
    for x in range(GRID_WIDTH):
        # First, collect all puyos in this column (from bottom to top)
        puyos = []
        for y in range(GRID_HEIGHT-1, -1, -1):
            if board[y][x] is not None:
                puyos.append(board[y][x])
                board[y][x] = None  # Remove from the board temporarily
        
        # Then place them back starting from the bottom
        current_y = GRID_HEIGHT - 1
        for puyo in puyos:
            # Find the first empty space from the bottom
            while current_y >= 0 and board[current_y][x] is not None:
                current_y -= 1
                
            if current_y >= 0:  # If we found a valid position
                if puyo.y != current_y:  # If the puyo has moved
                    puyo.y = current_y
                    puyo.start_wobble()
                    moved = True
                board[current_y][x] = puyo
                current_y -= 1  # Move up for the next puyo
    
    return moved

def find_connected_groups():
    visited = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    groups = []
    
    def dfs(y, x, service_type, group):
        if (y < 0 or y >= GRID_HEIGHT or x < 0 or x >= GRID_WIDTH or 
            visited[y][x] or board[y][x] is None or 
            board[y][x].service_type != service_type):
            return
        
        visited[y][x] = True
        group.append((y, x))
        
        # Check all four directions
        dfs(y + 1, x, service_type, group)  # down
        dfs(y - 1, x, service_type, group)  # up
        dfs(y, x + 1, service_type, group)  # right
        dfs(y, x - 1, service_type, group)  # left
    
    # Find all connected groups
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not visited[y][x] and board[y][x] is not None:
                group = []
                dfs(y, x, board[y][x].service_type, group)
                if len(group) >= 4:  # Only consider groups of 4 or more
                    groups.append(group)
    
    return groups

def start_clear_animation(groups):
    global clearing_groups, clear_animation_frame, clear_animation_start_time, chain_count, is_chain_active
    global chain_display_time, max_chain, total_cleared
    
    if not groups:
        return False
    
    # Mark all puyos in the groups as clearing
    total_in_groups = 0
    for group in groups:
        total_in_groups += len(group)
        for y, x in group:
            if board[y][x] is not None:
                board[y][x].is_clearing = True
                board[y][x].blink_frame = 0
    
    # Update statistics
    total_cleared += total_in_groups
    
    clearing_groups = groups
    clear_animation_frame = 0
    clear_animation_start_time = pygame.time.get_ticks()
    chain_display_time = pygame.time.get_ticks()
    is_chain_active = True
    chain_count += 1
    
    # Update max chain if current chain is higher
    if chain_count > max_chain:
        max_chain = chain_count
    
    return True

def update_clear_animation():
    global clearing_groups, clear_animation_frame, is_chain_active, score, pop_animations
    
    if not clearing_groups:
        return False
    
    current_time = pygame.time.get_ticks()
    
    # Update blink animation
    for group in clearing_groups:
        for y, x in group:
            if board[y][x] is not None:
                board[y][x].blink_frame += 1
    
    clear_animation_frame += 1
    
    # When animation is complete, remove the puyos and start pop animations
    if clear_animation_frame >= CLEAR_BLINK_FRAMES:
        # Add score based on group size and chain count
        chain_bonus = chain_count * 50  # Bonus increases with chain count
        
        for group in clearing_groups:
            # Add score based on group size
            group_score = len(group) * 10 * (1 + (chain_count - 1) * 0.5)  # Base score + chain bonus
            score += int(group_score)
            
            # Start pop animations for each puyo
            for y, x in group:
                if board[y][x] is not None:
                    # Create a copy of the puyo for the pop animation
                    pop_puyo = Puyo(board[y][x].service_type, x, y)
                    pop_animations.append({
                        'puyo': pop_puyo,
                        'frame': 0,
                        'x': x,
                        'y': y
                    })
                    
                    # Remove the puyo from the board
                    board[y][x] = None
        
        clearing_groups = []
        is_chain_active = False
        return True
    
    return False

def update_pop_animations():
    global pop_animations
    
    if not pop_animations:
        return
    
    # Update each pop animation
    for i in range(len(pop_animations) - 1, -1, -1):
        anim = pop_animations[i]
        anim['frame'] += 1
        
        # Update the puyo's scale and alpha based on the animation frame
        progress = anim['frame'] / POP_ANIMATION_FRAMES
        anim['puyo'].pop_scale = 1.0 + progress * 0.5  # Grow slightly before popping
        anim['puyo'].pop_alpha = 255 * (1 - progress)  # Fade out
        
        # Remove completed animations
        if anim['frame'] >= POP_ANIMATION_FRAMES:
            pop_animations.pop(i)

def check_game_over():
    # Game is over if there are puyos in the top row
    for x in range(GRID_WIDTH):
        if board[0][x] is not None:
            return True
    return False

def draw_board():
    # Draw AWS-themed background
    draw_background()
    
    # Draw board outline
    board_rect = pygame.Rect(BOARD_LEFT - 2, BOARD_TOP - 2, 
                            GRID_WIDTH * GRID_SIZE + 4, GRID_HEIGHT * GRID_SIZE + 4)
    pygame.draw.rect(screen, BLACK, board_rect, 2)
    
    # Draw grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_rect = pygame.Rect(BOARD_LEFT + x * GRID_SIZE, BOARD_TOP + y * GRID_SIZE, 
                                   GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, LIGHT_GRAY, cell_rect, 1)
    
    # Draw placed puyos
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if board[y][x] is not None:
                board[y][x].draw(screen)
    
    # Draw current piece
    if current_piece:
        current_piece.draw(screen)
    
    # Draw pop animations
    for anim in pop_animations:
        anim['puyo'].draw(screen)
    
    # Draw next piece preview - moved to the right side
    next_area_x = BOARD_LEFT + GRID_WIDTH * GRID_SIZE + 30
    next_area_y = BOARD_TOP
    
    # Draw next piece area
    next_rect = pygame.Rect(next_area_x, next_area_y, 120, 120)
    pygame.draw.rect(screen, LIGHT_GRAY, next_rect, 2)
    
    next_text = font.render("NEXT", True, BLACK)
    screen.blit(next_text, (next_area_x + 35, next_area_y - 30))
    
    if next_piece:
        # Draw next piece centered in the next area
        # Fixed positioning for the next piece preview
        next_main_x = next_area_x + 60
        next_main_y = next_area_y + 40
        next_sub_x = next_area_x + 60
        next_sub_y = next_area_y + 80
        
        # Draw main puyo
        main_img = images[next_piece.main_puyo.service_type]
        main_rect = main_img.get_rect(center=(next_main_x, next_main_y))
        screen.blit(main_img, main_rect)
        
        # Draw sub puyo
        sub_img = images[next_piece.sub_puyo.service_type]
        sub_rect = sub_img.get_rect(center=(next_sub_x, next_sub_y))
        screen.blit(sub_img, sub_rect)
    
    # Draw score and level at the bottom right
    info_area_x = next_area_x
    info_area_y = next_area_y + 150
    
    score_text = font.render(f"トータルスコア: {score}", True, BLACK)
    screen.blit(score_text, (info_area_x, info_area_y))
    
    level_text = font.render(f"レベル: {level}", True, BLACK)
    screen.blit(level_text, (info_area_x, info_area_y + 40))
    
    # Draw statistics
    stats_y = info_area_y + 80
    
    # Draw total cleared puyos
    cleared_text = font.render(f"消した数: {total_cleared}", True, BLACK)
    screen.blit(cleared_text, (info_area_x, stats_y))
    
    # Draw max chain
    max_chain_text = font.render(f"最大れんさ数: {max_chain}", True, BLACK)
    screen.blit(max_chain_text, (info_area_x, stats_y + 30))
    
    # Draw play time
    if start_time > 0:
        if game_over:
            # If game is over, use the end time
            play_time = (end_time - start_time) // 1000  # Convert to seconds
        else:
            # If game is still active, use current time
            play_time = (pygame.time.get_ticks() - start_time) // 1000
        
        time_text = font.render(f"プレイタイム: {play_time}秒", True, BLACK)
        screen.blit(time_text, (info_area_x, stats_y + 60))
    
    # Draw controls in the bottom right
    controls_y = stats_y + 100
    controls_title = font.render("操作方法:", True, BLACK)
    screen.blit(controls_title, (info_area_x, controls_y))
    
    controls = [
        "←→: 左右移動",
        "↑/SPACE: 回転",
        "↓: 高速落下"
    ]
    
    for i, control in enumerate(controls):
        control_text = font.render(control, True, BLACK)
        screen.blit(control_text, (info_area_x, controls_y + 25 + i * 20))
    
    # Draw chain count if active
    if chain_count > 1 and is_chain_active:
        # Only display for a certain duration
        if pygame.time.get_ticks() - chain_display_time < CHAIN_DISPLAY_DURATION:
            # Create chain text with orange fill and black outline
            chain_text = large_font.render(f"{chain_count}れんさ！", True, ORANGE)
            
            # Calculate position - center of screen
            chain_rect = chain_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # Draw black outline
            outline_size = 2
            for dx in range(-outline_size, outline_size + 1):
                for dy in range(-outline_size, outline_size + 1):
                    if dx != 0 or dy != 0:
                        outline_rect = chain_text.get_rect(
                            center=(SCREEN_WIDTH // 2 + dx, SCREEN_HEIGHT // 2 + dy)
                        )
                        outline_text = large_font.render(f"{chain_count}れんさ！", True, BLACK)
                        screen.blit(outline_text, outline_rect)
            
            # Draw the main orange text on top
            screen.blit(chain_text, chain_rect)

def reset_game():
    global board, current_piece, next_piece, game_over, score, level, fall_speed, last_fall_time
    global clearing_groups, clear_animation_frame, chain_count, is_chain_active, pop_animations
    global total_cleared, max_chain, start_time, end_time, game_state
    
    board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_piece = None
    next_piece = None
    game_over = False
    score = 0
    level = 1
    fall_speed = 0.5
    last_fall_time = pygame.time.get_ticks()
    
    # Reset animation variables
    clearing_groups = []
    clear_animation_frame = 0
    chain_count = 0
    is_chain_active = False
    pop_animations = []
    
    # Reset statistics
    total_cleared = 0
    max_chain = 0
    start_time = pygame.time.get_ticks()
    end_time = 0
    
    # Set game state to playing
    game_state = STATE_PLAYING
    
    create_new_piece()

# Game variables initialization
clock = pygame.time.Clock()
board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_piece = None
next_piece = None
game_over = False
score = 0
level = 1
fall_speed = 0.5  # Initial fall speed in seconds
last_fall_time = 0

# Game state
game_state = STATE_TITLE
continue_option = CONTINUE_OPTION_YES
continue_start_time = 0
fade_alpha = 0  # For fade out effect
game_over_start_time = 0  # When game over animation started

# Animation variables
clearing_groups = []  # Groups of puyos being cleared
clear_animation_frame = 0  # Current frame of clear animation
clear_animation_start_time = 0  # When the current clear animation started
chain_count = 0  # Current chain count
max_chain = 0  # Maximum chain achieved
is_chain_active = False  # Whether a chain reaction is in progress
pop_animations = []  # List of pop animations in progress
chain_display_time = 0  # When the current chain text started displaying
total_cleared = 0  # Total number of puyos cleared
start_time = 0  # When the game started
end_time = 0   # When the game ended (for game over)

# Initialize game
game_state = STATE_TITLE  # Start at title screen
start_time = pygame.time.get_ticks()  # Record the start time

# Main game loop
while True:
    current_time = pygame.time.get_ticks()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # Title screen controls
        if game_state == STATE_TITLE:
            if event.type == KEYDOWN and event.key == K_SPACE:
                reset_game()  # Start the game
        
        # Playing state controls
        elif game_state == STATE_PLAYING and not is_chain_active:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if current_piece:
                        current_piece.move_left()
                elif event.key == K_RIGHT:
                    if current_piece:
                        current_piece.move_right()
                elif event.key == K_DOWN:
                    if current_piece:
                        current_piece.start_fast_drop()
                elif event.key == K_UP or event.key == K_SPACE:
                    if current_piece:
                        current_piece.rotate_clockwise()
                elif event.key == K_SPACE:
                    if current_piece:
                        current_piece.hard_drop()
            
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    if current_piece:
                        current_piece.stop_fast_drop()
        
        # Continue screen controls
        elif game_state == STATE_CONTINUE:
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_DOWN:
                    # Toggle between Yes and No
                    continue_option = 1 - continue_option
                elif event.key == K_RETURN:
                    if continue_option == CONTINUE_OPTION_YES:
                        reset_game()  # Restart the game
                    else:
                        game_state = STATE_TITLE  # Return to title screen
    
    # Title screen logic
    if game_state == STATE_TITLE:
        draw_title_screen()
    
    # Playing state logic
    elif game_state == STATE_PLAYING:
        # Update pop animations
        update_pop_animations()
        
        # Handle chain reactions
        if is_chain_active:
            # Update clear animation
            if update_clear_animation():
                # When animation is complete, apply gravity
                gravity_applied = True
                while gravity_applied:
                    gravity_applied = apply_gravity()
                    # Small delay to make the falling visible
                    pygame.time.delay(50)
                    # Draw the board to show the falling animation
                    draw_board()
                    pygame.display.flip()
                
                # Find new groups after gravity
                new_groups = find_connected_groups()
                if new_groups:
                    # Start a new chain reaction after a delay
                    pygame.time.delay(CLEAR_DELAY)  # Longer delay between chains
                    start_clear_animation(new_groups)
                else:
                    # No more chains, reset chain count and continue game
                    is_chain_active = False
                    chain_count = 0
                    
                    # Create a new piece if needed
                    if current_piece is None:
                        create_new_piece()
        
        # Handle continuous fast drop when down key is pressed
        elif current_piece:  # Only if not in chain animation and piece exists
            keys = pygame.key.get_pressed()
            if keys[K_DOWN] and current_time - current_piece.last_drop_time > 30:  # Fast drop speed
                current_piece.move_down()
                current_piece.last_drop_time = current_time
            
            # Handle automatic falling
            if current_time - last_fall_time > fall_speed * 1000:
                if not current_piece.move_down():
                    # Piece cannot move down further, lock it in place
                    lock_piece()
                    
                    # Apply gravity immediately after locking a piece
                    gravity_applied = True
                    while gravity_applied:
                        gravity_applied = apply_gravity()
                        # Small delay to make the falling visible
                        pygame.time.delay(50)
                        # Draw the board to show the falling animation
                        draw_board()
                        pygame.display.flip()
                    
                    # Check for chains
                    groups = find_connected_groups()
                    if groups:
                        # Start chain reaction
                        start_clear_animation(groups)
                    else:
                        # No chains, create a new piece
                        create_new_piece()
                    
                    # Check for game over
                    if check_game_over():
                        game_over = True
                        end_time = pygame.time.get_ticks()  # Record end time when game over
                        game_state = STATE_CONTINUE  # Show continue screen
                        continue_start_time = 0  # Will be set after animation completes
                        game_over_start_time = pygame.time.get_ticks()  # Start game over animation
                        continue_option = CONTINUE_OPTION_YES  # Default to Yes
                    
                    # Update level and fall speed based on score
                    new_level = 1 + score // 1000
                    if new_level > level:
                        level = new_level
                        fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)
                
                last_fall_time = current_time
        
        # Draw the game board
        draw_board()
    
    # Continue screen logic
    elif game_state == STATE_CONTINUE:
        # Draw the game board in the background
        draw_board()
        # Draw the continue screen overlay
        draw_continue_screen()
    
    # Fade out logic
    elif game_state == STATE_FADE_OUT:
        # Draw the continue screen in the background
        draw_board()
        draw_continue_screen()
        # Draw the fade out effect
        draw_fade_out()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)
