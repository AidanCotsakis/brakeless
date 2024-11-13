# Breakless

A grid-based 2D puzzle game built with Python and Pygame. Breakless features customizable levels, particle effects, and responsive keyboard controls, creating a simple yet engaging gameplay experience.

## **Features**

- **Grid-Based Levels**: Level layout is read from a file, with customizable start and finish positions.
- **Responsive Keyboard Controls**: Supports arrow keys and `W`, `A`, `S`, `D` for smooth navigation.
- **Particle Effects**: Dynamic particle effects for player movements, level transitions, and specific actions.
- **Custom Wall Sprites**: Automatically adjusts wall sprite visuals based on neighboring walls for seamless continuity.
- **Level Transition System**: Smooth transitions between levels with adjustable animations.

## **Setup and Installation**

1. **Install Dependencies**:
   - Ensure Python 3 and Pygame are installed.
   ```bash
   pip install pygame
   ```
2. **Run the Game**:

    ```bash
    python breakless.py
    ```
## **Usage**
- Keyboard Controls:

    - **Move Up**: `W` or `↑`
    - **Move Down**: `S` or `↓`
    - **Move Left**: `A` or `←`
    - **Move Right**: `D` or `→`
    - **Restart Level**: `Space`

- **Objective**: Navigate the player from the start to the finish.

## **Code Highlights**
- **Particle System**: Configurable particle effects for movement, transitions, and more, implemented within `particleObj`.
- **Dynamic Wall Sprites**: A self-adapting wall sprite system that modifies wall images based on neighboring tiles.
- **Modular Level Loading**: Levels loaded from external files allow easy customization and expansion.
- **Efficient Screen Updates**: Double-buffered drawing and Pygame's `Surface` scaling for smooth performance across resolutions.