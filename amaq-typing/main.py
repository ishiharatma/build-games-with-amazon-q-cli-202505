import pygame
import sys
import random
import os
import time
from pygame.locals import *
from images.aws_background import create_aws_background, draw_aws_title, draw_aws_button, draw_aws_text_box

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AWS Service Typing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# AWS Colors
AWS_ORANGE = (255, 153, 0)
AWS_BLUE = (0, 124, 173)
AWS_DARK_BLUE = (35, 47, 62)
AWS_LIGHT_BLUE = (0, 160, 210)

# Fonts - Using system fonts
try:
    # Try to use system fonts
    font_title = pygame.font.SysFont('meiryo', 48, bold=True)  # Japanese system font
    font_large = pygame.font.SysFont('meiryo', 36)
    font_medium = pygame.font.SysFont('meiryo', 28)
    font_small = pygame.font.SysFont('meiryo', 24)
except:
    # Fallback to default fonts if not available
    font_title = pygame.font.SysFont('arial', 48, bold=True)
    font_large = pygame.font.SysFont('arial', 36)
    font_medium = pygame.font.SysFont('arial', 28)
    font_small = pygame.font.SysFont('arial', 24)

# Game variables
game_time = 100  # seconds
correct_count = 0
mistake_count = 0
current_service = ""
current_image = None
user_input = ""
game_active = False
game_over = False
start_time = 0
elapsed_time = 0
typing_count = 0
last_answer = ""
answer_feedback = ""
feedback_timer = 0

# AWS Services with their corresponding image filenames
aws_services = [
    "S3", "EC2", "Lambda", "DynamoDB", "CloudFront", 
    "RDS", "SQS", "SNS", "CloudWatch", "IAM",
    "Route53", "ECS", "EKS", "Fargate", "API Gateway",
    "Cognito", "Amplify", "AppSync", "Athena", "Aurora",
    "Batch", "Bedrock", "CloudFormation", "CodeBuild", "CodePipeline",
    "Comprehend", "Connect", "DocumentDB", "Elastic Beanstalk", "ElastiCache",
    "EventBridge", "Glue", "Kinesis", "Lex", "Lightsail",
    "Macie", "MemoryDB", "Neptune", "Polly", "Rekognition",
    "SageMaker", "SecretsManager", "Step Functions", "Textract", "VPC"
]

# Load images
def load_images():
    images = {}
    for service in aws_services:
        image_path = os.path.join("images", f"{service.lower().replace(' ', '_')}.png")
        if os.path.exists(image_path):
            try:
                img = pygame.image.load(image_path)
                img = pygame.transform.scale(img, (200, 200))
                images[service] = img
            except pygame.error:
                print(f"Could not load image for {service}")
        else:
            print(f"Image not found for {service}: {image_path}")
    return images

# Get a random AWS service and remove it from the list to avoid duplicates
def get_random_service(services):
    if not services:  # If all services have been used
        return None
    service = random.choice(services)
    services.remove(service)  # Remove the service from the list
    return service

# Draw text with a background
def draw_text(text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_rect

# Get title based on correct count
def get_title(count):
    if count >= 40:
        return "AWS Hero"
    elif count >= 30:
        return "AWS Expert"
    elif count >= 20:
        return "AWS Professional"
    elif count >= 10:
        return "AWS Associate"
    else:
        return "AWS Beginner"

# Main game loop
def main():
    global game_active, game_over, current_service, current_image, user_input
    global correct_count, mistake_count, start_time, elapsed_time, typing_count
    
    clock = pygame.time.Clock()
    
    # Try to load images
    service_images = load_images()
    
    # Available services (those with images)
    available_services = aws_services.copy()
    
    # Start screen
    # Create AWS background once
    aws_background = create_aws_background(WIDTH, HEIGHT)
    
    while not game_active and not game_over:
        screen.blit(aws_background, (0, 0))
        
        # Draw AWS-style title
        draw_aws_title(screen, "AWS Service Typing Game", font_title, WIDTH//2, HEIGHT//4)
        
        # Draw instruction text box
        instruction_text = "Type the AWS service name shown (without 'AWS' or 'Amazon' prefix)"
        draw_aws_text_box(screen, instruction_text, font_medium, WIDTH//2, HEIGHT//2 - 30, 600, 80)
        
        # Draw start button
        start_button = draw_aws_button(screen, "Press SPACE to start", font_medium, WIDTH//2, HEIGHT//2 + 80, 300, 60)
        
        # Draw additional information
        info_text = "Test your AWS knowledge with this typing game!"
        draw_aws_text_box(screen, info_text, font_small, WIDTH//2, HEIGHT - 100, 500, 50)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_active = True
                    start_time = time.time()
                    current_service = get_random_service(available_services)
                    
    # Main game loop
    while game_active:
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = max(0, game_time - elapsed_time)
        
        if remaining_time <= 0:
            game_active = False
            game_over = True
        
        # Use a lighter background during gameplay
        screen.fill(AWS_LIGHT_BLUE)
        pygame.draw.rect(screen, AWS_DARK_BLUE, (0, 0, WIDTH, 80))  # Top bar
        pygame.draw.rect(screen, AWS_DARK_BLUE, (0, HEIGHT-40, WIDTH, 40))  # Bottom bar
        
        # Display service icon with a nice frame
        if current_service in service_images:
            # Draw a frame for the icon
            icon_frame = pygame.Rect(WIDTH//2 - 110, 90, 220, 220)
            pygame.draw.rect(screen, WHITE, icon_frame, border_radius=10)
            pygame.draw.rect(screen, AWS_ORANGE, icon_frame, 3, border_radius=10)
            
            # Display the icon
            screen.blit(service_images[current_service], (WIDTH//2 - 100, 100))
        else:
            # Fallback if image not found
            icon_frame = pygame.Rect(WIDTH//2 - 110, 90, 220, 220)
            pygame.draw.rect(screen, WHITE, icon_frame, border_radius=10)
            pygame.draw.rect(screen, AWS_ORANGE, icon_frame, 3, border_radius=10)
            draw_text(current_service, font_large, BLACK, WIDTH//2, 200)
        
        # Display input field with AWS styling
        input_rect = pygame.Rect(WIDTH//2 - 200, 350, 400, 50)
        pygame.draw.rect(screen, WHITE, input_rect, border_radius=5)
        pygame.draw.rect(screen, AWS_BLUE, input_rect, 2, border_radius=5)
        draw_text(user_input, font_medium, AWS_DARK_BLUE, WIDTH//2, 375)
        
        # Display stats with AWS styling
        pygame.draw.rect(screen, WHITE, (20, 15, 180, 50), border_radius=5)
        draw_text(f"Time: {int(remaining_time)}s", font_small, AWS_DARK_BLUE, 110, 40)
        
        pygame.draw.rect(screen, WHITE, (WIDTH - 220, 15, 200, 50), border_radius=5)
        draw_text(f"Correct: {correct_count}", font_small, GREEN, WIDTH - 120, 30)
        
        pygame.draw.rect(screen, WHITE, (WIDTH - 220, 70, 200, 50), border_radius=5)
        draw_text(f"Mistakes: {mistake_count}", font_small, RED, WIDTH - 120, 95)
        
        # Add instruction at the bottom
        draw_text("Type the service name and press ENTER", font_small, WHITE, WIDTH//2, HEIGHT - 20)
        
        # Display answer feedback if available
        if answer_feedback and time.time() - feedback_timer < 2:  # Show feedback for 2 seconds
            feedback_color = GREEN if "Correct" in answer_feedback else RED
            # Create a background for the feedback
            feedback_bg = pygame.Rect(WIDTH//2 - 300, HEIGHT - 70, 600, 30)
            pygame.draw.rect(screen, AWS_DARK_BLUE, feedback_bg, border_radius=5)
            draw_text(answer_feedback, font_small, feedback_color, WIDTH//2, HEIGHT - 55)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_active = False
                    game_over = True
                elif event.key == K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == K_RETURN:
                    typing_count += len(user_input)
                    if user_input.lower() == current_service.lower():
                        correct_count += 1
                        answer_feedback = "Correct!"
                    else:
                        mistake_count += 1
                        answer_feedback = f"Wrong! Correct answer: {current_service}"
                    
                    feedback_timer = time.time()
                    last_answer = user_input
                    user_input = ""
                    current_service = get_random_service(available_services)
                    # If we've used all services, end the game
                    if current_service is None:
                        game_active = False
                        game_over = True
                else:
                    user_input += event.unicode
        
        clock.tick(60)
    
    # Game over screen
    while game_over:
        # Black background for game over screen
        screen.fill(BLACK)
        
        # Calculate typing speed (characters per second)
        total_time = min(game_time, elapsed_time)
        typing_speed = typing_count / total_time if total_time > 0 else 0
        
        # Get title
        title = get_title(correct_count)
        
        # Draw AWS-style title
        draw_aws_title(screen, "Game Over!", font_title, WIDTH//2, HEIGHT//5)
        
        # Center all content vertically
        center_y = HEIGHT // 2
        
        # Draw results in an AWS-style box with adjusted width
        results_text = f"Correct: {correct_count}  |  Mistakes: {mistake_count}"
        draw_aws_text_box(screen, results_text, font_medium, WIDTH//2, center_y - 70, 400, 60)
        
        # Draw typing speed with adjusted width
        speed_text = f"Typing Speed: {typing_speed:.1f} chars/second"
        draw_aws_text_box(screen, speed_text, font_medium, WIDTH//2, center_y, 400, 50)
        
        # Draw title with AWS-style with adjusted width
        title_text = f"Your Title: {title}"
        draw_aws_text_box(screen, title_text, font_large, WIDTH//2, center_y + 70, 400, 60, 
                         bg_color=AWS_ORANGE, text_color=WHITE)
        
        # Draw restart button
        restart_button = draw_aws_button(screen, "Press SPACE to play again", font_medium, WIDTH//2, HEIGHT - 80, 350, 50)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Reset game
                    game_active = True
                    game_over = False
                    correct_count = 0
                    mistake_count = 0
                    user_input = ""
                    typing_count = 0
                    answer_feedback = ""
                    last_answer = ""
                    start_time = time.time()
                    # Reset available services
                    available_services = aws_services.copy()
                    current_service = get_random_service(available_services)
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        clock.tick(60)

if __name__ == "__main__":
    main()
