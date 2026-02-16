# Treasure Hunt AI Game

**Treasure Hunt AI Game** is a 2D Python game built using **Pygame**, where the player automatically moves using the **A\*** algorithm to find treasures while avoiding obstacles, collecting gold, and managing health points (HP) before time runs out.

---

## 🕹️ How to Play

- The player starts at a random position on a 20×20 grid.
- The goal is to collect 3 treasures placed randomly on the grid.
- Collect **gold** (+10) by moving over gold cells.
- Moving over **damage cells** reduces HP by 10.
- Running out of time or HP ends the game (**Game Over**).
- Collecting all treasures means you **Win**.

---

## 🎮 Game Elements

| Element | Color | Effect |
|---------|-------|--------|
| Walkable cell | Gray | Can move over |
| Obstacle | Black | Cannot move through |
| Gold cell | Gold | +10 Gold when visited |
| Damage cell | Red | -10 HP when visited |
| Treasure | Blue | Main goal |
| Player | Green | Moves automatically using A* |

---


## ⚙️ Features

- **A\* Algorithm**: Finds the shortest path from the player to the next treasure.
- **Visited Cells**: Cells the player passed turn green.
- **Timer**: 30 seconds limit per game.
- **Sounds**:
  - `win.wav` plays when winning.
  - `game_over.wav` plays when losing.

---

## 🛠️ Requirements

- Python 3.x
- Pygame library

Install Pygame with:

```bash
pip install pygame
