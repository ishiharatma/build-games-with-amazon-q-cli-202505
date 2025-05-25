# build-games-with-amazon-q-cli-202505

Build Games with Amazon Q CLI and score a T shirt 🏆

https://community.aws/content/2xIoduO0xhkhUApQpVUIqBFGmAc/build-games-with-amazon-q-cli-and-score-a-t-shirt

![overview](./images/game-v2.2-x4.gif)

## Project Overview

This project was created as part of the "Build Games with Amazon Q CLI and score a T shirt" event. It's a Puyo Puyo-style puzzle game called "AmaQ Puyo" built using Python and Pygame, with development assistance from Amazon Q CLI.

## Game Features

### Basic Gameplay
- Puyo Puyo-style falling puzzle game
- Match 4 or more of the same color to clear them
- Chain reactions for higher scores
- Level progression based on score

### Visual Elements
- Falling prediction display with semi-transparent circles
- Pop animations when pieces are cleared
- AWS-themed background with floating clouds
- Stylized title screen with "あまぷよ！！" (AmaQ Puyo)

### Game Mechanics
- Chain system with sequential clearing animations
- Wall kick feature for rotation near edges
- Combo system with score multipliers
- Statistics tracking (cleared pieces, max chain, play time)

### UI Features
- Japanese language support
- Control instructions display
- Title screen with start prompt
- Game over animation with "Amazon Q～" text falling from top
- Continue screen with countdown timer
- Fade transitions between screens

## Development Process

This game was developed entirely with the assistance of Amazon Q CLI, demonstrating how AI can help in game development. The development process included:

1. Implementing basic game mechanics
2. Adding visual enhancements and animations
3. Implementing chain reaction systems
4. Creating UI elements and screens
5. Bug fixing and optimization
6. Adding polish and final touches

## Development Environment

- Windows with WSL (Windows Subsystem for Linux)
- VSCode with devcontainer
- Python 3 with Pygame
- Amazon Q CLI for development assistance

## Controls

- **Left/Right Arrow Keys**: Move pieces horizontally
- **Up Arrow Key or Space**: Rotate piece
- **Down Arrow Key**: Fast drop

## Technical Highlights

- State management system for different game screens
- Optimized falling logic for smooth piece movement
- Wall kick implementation for better rotation mechanics
- Japanese font support with fallback options
- Animation system for chains and piece clearing

---

*This project was created using Amazon Q CLI as part of the AWS community event.*
