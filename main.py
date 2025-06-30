import pygame  # 2D game library
import random  # Random placement
import heapq  # For A* algorithm
import time  # Timer management
import os  # File path checking

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 223, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)  # Walkable cells

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt AI Game")
font = pygame.font.SysFont(None, 36)

# Load sound effects
if not os.path.exists('sounds/win.wav') or not os.path.exists('sounds/game_over.wav'):
    print("Sound files are missing! Ensure 'sounds/win.wav' and 'sounds/game_over.wav' exist.")
    exit()

win_sound = pygame.mixer.Sound('sounds/win.wav')
game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')

# Grid setup
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Cell types
WALKABLE = 0
OBSTACLE = 1
GOLD_CELL = 2
DAMAGE_CELL = 3
TREASURE = 4

# Player setup
player_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
player_hp = 100
player_gold = 0

treasure_positions = []
visited_cells = set()

def reset_game():
    """Reset the game state."""
    global player_pos, player_hp, player_gold, treasure_positions, visited_cells, grid
    player_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    player_hp = 100
    player_gold = 0
    treasure_positions = []

    while len(treasure_positions) < 3:
        treasure_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
        if treasure_pos not in treasure_positions and treasure_pos != player_pos:
            treasure_positions.append(treasure_pos)

    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for _ in range(GRID_SIZE * 9):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if [x, y] not in [player_pos] and [x, y] not in treasure_positions:
            grid[x][y] = random.choice([OBSTACLE, GOLD_CELL, DAMAGE_CELL])
    for treasure_pos in treasure_positions:
        grid[treasure_pos[0]][treasure_pos[1]] = TREASURE

    visited_cells = set()

def draw_grid():
    """Draw the grid and its contents."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) in visited_cells:
                pygame.draw.rect(screen, GREEN, rect)  # Visited cells
            elif grid[x][y] == OBSTACLE:
                pygame.draw.rect(screen, BLACK, rect)
            elif grid[x][y] == GOLD_CELL:
                pygame.draw.rect(screen, GOLD, rect)
            elif grid[x][y] == DAMAGE_CELL:
                pygame.draw.rect(screen, RED, rect)
            elif grid[x][y] == TREASURE:
                pygame.draw.rect(screen, BLUE, rect)
            elif grid[x][y] == WALKABLE:
                pygame.draw.rect(screen, GRAY, rect)  # Walkable cells
            pygame.draw.rect(screen, WHITE, rect, 1)  # Borders

    # Draw the player on top
    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, GREEN, player_rect)

def heuristic(a, b):
    """Manhattan distance heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal):
    """A* algorithm for pathfinding."""
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {tuple(start): 0}
    f_score = {tuple(start): heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while tuple(current) in came_from:
                path.append(current)
                current = came_from[tuple(current)]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = [current[0] + dx, current[1] + dy]
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[0]][neighbor[1]] != OBSTACLE:
                tentative_g_score = g_score[tuple(current)] + 1
                if tuple(neighbor) not in g_score or tentative_g_score < g_score[tuple(neighbor)]:
                    came_from[tuple(neighbor)] = current
                    g_score[tuple(neighbor)] = tentative_g_score
                    f_score[tuple(neighbor)] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[tuple(neighbor)], neighbor))
    return []

def update_player_stats(cell_type):
    """Update player stats based on cell type."""
    global player_hp, player_gold
    if cell_type == GOLD_CELL:
        player_gold += 10
    elif cell_type == DAMAGE_CELL:
        player_hp -= 10

def game_over_screen():
    """Display the Game Over screen."""
    screen.fill(WHITE)
    game_over_text = font.render("GAME OVER", True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 3 - 40, HEIGHT // 2))
    game_over_sound.play()
    pygame.display.flip()

def win_screen():
    """Display the You Win screen."""
    screen.fill(WHITE)
    win_text = font.render("YOU WIN", True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)

    screen.blit(win_text, (WIDTH // 3, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 3 - 40, HEIGHT // 2))
    win_sound.play()
    pygame.display.flip()

def main():
    """Main game loop."""
    global player_gold  # Ensure the global variable is used
    running = True
    path = []
    current_goal_index = 0  # Start with the first goal
    start_time = time.time()
    game_time_limit = 30

    while running:
        elapsed_time = int(time.time() - start_time)
        remaining_time = game_time_limit - elapsed_time

        if remaining_time <= 0 or player_hp <= 0:
            game_over_screen()
            pygame.time.wait(3000)
            reset_game()  # Reset the game state after game over
            break

        if player_pos == treasure_positions[current_goal_index]:
            player_gold += 100
            current_goal_index += 1
            if current_goal_index >= len(treasure_positions):
                win_screen()
                pygame.time.wait(3000)
                reset_game()  # Reset the game after winning
                break

        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player_hp > 0 and current_goal_index < len(treasure_positions):
            path = a_star_search(player_pos, treasure_positions[current_goal_index])

        if path:
            next_move = path.pop(0)
            player_pos[0], player_pos[1] = next_move
            visited_cells.add(tuple(player_pos))
            update_player_stats(grid[player_pos[0]][player_pos[1]])
            grid[player_pos[0]][player_pos[1]] = WALKABLE

        draw_grid()

        hp_text = font.render(f"HP: {player_hp}", True, BLACK)
        gold_text = font.render(f"Gold: {player_gold}", True, BLACK)
        timer_text = font.render(f"Time: {remaining_time}s", True, BLACK)

        screen.blit(hp_text, (10, HEIGHT - 50))
        screen.blit(gold_text, (WIDTH - 150, HEIGHT - 50))
        screen.blit(timer_text, (WIDTH // 2 - 50, HEIGHT - 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Frame rate (60 FPS)

        # Handle input for restarting or quitting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
        elif keys[pygame.K_r]:
            reset_game()
            main()

    pygame.quit()

# Start the game
reset_game()
main()

