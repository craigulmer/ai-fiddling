# Bouncy Vector Ball

A Python application featuring a bouncing ball made of vector points that rotate as the ball moves, inspired by 1990s Amiga demos.

## Features

- **Vector Dot Ball**: The ball is composed of rotating points connected by lines
- **Physics Simulation**: Realistic bouncing with gravity and damping
- **Retro Aesthetic**: Dark background with subtle grid, reminiscent of classic demos
- **Interactive Controls**: Reset ball position and quit functionality

## Requirements

- Python 3.7+
- Pygame 2.5.2
- NumPy 1.24.3

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python bouncy_ball.py
```

## Controls

- **SPACE**: Reset ball position and give it a random velocity
- **ESC**: Quit the application
- **Close Window**: Quit the application

## How It Works

The application creates a ball made of 15 vector points arranged in a circle. As the ball bounces around the screen:

1. **Physics**: The ball follows realistic physics with gravity and bounce damping
2. **Rotation**: The vector points rotate around the ball's center as it moves
3. **Wireframe Effect**: Lines connect adjacent points to create a wireframe appearance
4. **Visual Feedback**: The screen shows ball position and velocity information

The result is a nostalgic visual effect similar to the vector graphics seen in classic Amiga demos from the 1990s. 