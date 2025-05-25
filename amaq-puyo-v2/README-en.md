# AWS Puyo Puyo Game

[![🇯🇵 日本語](https://img.shields.io/badge/%F0%9F%87%AF%F0%9F%87%B5-日本語-white)](./README.md)
[![🇺🇸 English](https://img.shields.io/badge/%F0%9F%87%BA%F0%9F%87%B8-English-white)](./README-en.md)

This game is a falling block puzzle game similar to Puyo Puyo, using AWS service icons.

## Game Features

- AWS service icons fall like Puyo Puyo blocks
- When 4 or more icons of the same service connect, they disappear and points are added
- Icons wobble when they land
- Landing prediction spots are displayed faintly
- Chain reactions occur in sequence
- Icons flash and then pop with an animation when disappearing
- Bonus points are added based on the number of chains
- Falling speed increases as levels progress
- When game over occurs, the "Game Over" text sways from side to side

## AWS Service Icons Used

- Red: CloudTrail
- Blue: Aurora
- Yellow: EC2
- Green: S3
- Purple: Amazon VPC

## Controls

- Left/Right Arrow Keys (←→): Move pieces left and right
- Up Arrow Key (↑) or Space Key: Rotate pieces
- Down Arrow Key (↓): Fast drop (while pressed)
- Space Key: Hard drop (instantly drop to bottom)
- When Game Over: Press R to restart

## Required Libraries

- Python 3.x
- Pygame

## Installation

```bash
pip install pygame
```

## How to Run

```bash
python main.py
```

## Game Objective

Try to clear as many AWS service icons as possible to achieve a high score! Aim for chain reactions to earn even higher points!
