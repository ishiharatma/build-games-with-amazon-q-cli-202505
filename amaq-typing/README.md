# AWS Service Typing Game

** Under construction **

A typing game where AWS service icons appear and you need to type the service name correctly.

## Game Features

- Type AWS service names (without "AWS" or "Amazon" prefix)
- 100-second time limit
- Score tracking: correct entries and mistakes
- Typing speed calculation (characters per second)
- Title awarded based on performance

## Requirements

- Python 3.x
- Pygame 2.6.1

## Setup

1. Install the required packages:
   ```
   pip install pygame==2.6.1 pillow requests
   ```

2. Download AWS service icons:
   ```
   python download_icons.py
   ```

3. Run the game:
   ```
   python main.py
   ```

## How to Play

1. Press SPACE to start the game
2. Type the name of the AWS service shown (without "AWS" or "Amazon")
3. Press ENTER to submit your answer
4. Try to type as many service names correctly as possible within 100 seconds

## Game Results

At the end of the game, you'll see:
- Number of correct entries
- Number of mistakes
- Typing speed (characters per second, with 1 decimal place)
- Your title based on performance:
  - 0-9 correct: AWS Beginner
  - 10-19 correct: AWS Associate
  - 20-29 correct: AWS Professional
  - 30-39 correct: AWS Expert
  - 40+ correct: AWS Hero

## Controls

- SPACE: Start game / Play again
- ENTER: Submit answer
- BACKSPACE: Delete character
- ESC: Quit game
