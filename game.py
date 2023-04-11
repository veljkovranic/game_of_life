import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 50
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Pygame initialization
pygame.init()

# Functions
def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_cells(screen, grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] == 1:
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, cell_rect)

def get_cell_coordinates(mouse_pos):
    x, y = mouse_pos
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    return grid_x, grid_y


def count_neighbors(grid, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            xi, yj = (x + i) % GRID_SIZE, (y + j) % GRID_SIZE
            count += grid[xi, yj]
    return count


def update_cells(grid):
    new_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1:
                if neighbors == 2 or neighbors == 3:
                    new_grid[x, y] = 1
            else:
                if neighbors == 3:
                    new_grid[x, y] = 1

    return new_grid

def play_pause(playing):
    return not playing

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    run = True
    playing = False
    print("dsada")
    # Initialize grid
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    while run:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = get_cell_coordinates(mouse_pos)
                    grid[x, y] = 1 - grid[x, y]  # Toggle cell state
                elif event.button == 3:  # Right click
                    playing = play_pause(playing)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = play_pause(playing)

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # Left mouse button is held down
            x, y = get_cell_coordinates(mouse_pos)
            grid[x, y] = 1  # Set the cell to live
        screen.fill(WHITE)

        if playing:
            grid = update_cells(grid)

        draw_grid(screen)
        draw_cells(screen, grid)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
