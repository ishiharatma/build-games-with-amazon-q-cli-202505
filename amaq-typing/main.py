import pygame
import sys
import random
import os
import time
from pygame.locals import *

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

# Fonts - Using Windows system fonts
try:
    # Try to use Windows system fonts
    font_large = pygame.font.SysFont('meiryo', 36)  # Japanese Windows system font
    font_medium = pygame.font.SysFont('meiryo', 28)
    font_small = pygame.font.SysFont('meiryo', 24)
except:
    # Fallback to default fonts if not available
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

# Get a random AWS service
def get_random_service(services):
    return random.choice(services)

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
    while not game_active and not game_over:
        screen.fill(WHITE)
        draw_text("AWS Service Typing Game", font_large, BLUE, WIDTH//2, HEIGHT//3)
        draw_text("Type the AWS service name shown (without 'AWS' or 'Amazon')", font_medium, BLACK, WIDTH//2, HEIGHT//2)
        draw_text("Press SPACE to start", font_medium, BLACK, WIDTH//2, HEIGHT//2 + 50)
        
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
        
        screen.fill(WHITE)
        
        # Display service icon
        if current_service in service_images:
            screen.blit(service_images[current_service], (WIDTH//2 - 100, 100))
        else:
            # Fallback if image not found
            pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, 100, 200, 200))
            draw_text(current_service, font_large, BLACK, WIDTH//2, 200)
        
        # Display input field
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 200, 350, 400, 50))
        draw_text(user_input, font_medium, BLACK, WIDTH//2, 375)
        
        # Display stats
        draw_text(f"Time: {int(remaining_time)}s", font_small, BLACK, 100, 30, False)
        draw_text(f"Correct: {correct_count}", font_small, GREEN, WIDTH - 200, 30, False)
        draw_text(f"Mistakes: {mistake_count}", font_small, RED, WIDTH - 200, 60, False)
        
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
                    else:
                        mistake_count += 1
                    user_input = ""
                    current_service = get_random_service(available_services)
                else:
                    user_input += event.unicode
        
        clock.tick(60)
    
    # Game over screen
    while game_over:
        screen.fill(WHITE)
        
        # Calculate typing speed (characters per second)
        total_time = min(game_time, elapsed_time)
        typing_speed = typing_count / total_time if total_time > 0 else 0
        
        # Get title
        title = get_title(correct_count)
        
        draw_text("Game Over!", font_large, BLUE, WIDTH//2, HEIGHT//4)
        draw_text(f"Correct: {correct_count}", font_medium, GREEN, WIDTH//2, HEIGHT//2 - 60)
        draw_text(f"Mistakes: {mistake_count}", font_medium, RED, WIDTH//2, HEIGHT//2)
        draw_text(f"Typing Speed: {typing_speed:.1f} chars/second", font_medium, BLACK, WIDTH//2, HEIGHT//2 + 60)
        draw_text(f"Your Title: {title}", font_large, BLUE, WIDTH//2, HEIGHT//2 + 120)
        draw_text("Press SPACE to play again or ESC to quit", font_small, BLACK, WIDTH//2, HEIGHT - 100)
        
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
                    start_time = time.time()
                    current_service = get_random_service(available_services)
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        clock.tick(60)

if __name__ == "__main__":
    main()
