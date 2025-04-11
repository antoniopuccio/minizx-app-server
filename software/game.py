from machine import Pin, I2C
import ssd1306
import time
import random

# I2C and display configuration
i2c = I2C(0, scl=Pin(1), sda=Pin(2))
display = ssd1306.SSD1306_I2C(64, 32, i2c)

# Exit button configuration
btn_exit = Pin(9, Pin.IN, Pin.PULL_UP)

# Display dimensions
WIDTH = 64
HEIGHT = 32

# Game of Life grid dimensions
CELL_SIZE = 2  # Size of each cell (2x2 pixels)
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Random initial grid state
grid = [[random.randint(0, 1) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Button debounce variable
last_button_state = btn_exit.value()

# Counter for adding randomness
randomness_counter = 0

# Function to count live neighbors of a cell
def count_neighbors(x, y):
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Ignore the cell itself
            nx, ny = x + i, y + j
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                neighbors += grid[ny][nx]
    return neighbors

# Function to update the grid
def update_grid():
    global grid
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(x, y)
            if grid[y][x] == 1:  # Live cell
                if neighbors < 2 or neighbors > 3:
                    new_grid[y][x] = 0  # Dies from overpopulation or isolation
                else:
                    new_grid[y][x] = 1  # Survives
            else:  # Dead cell
                if neighbors == 3:
                    new_grid[y][x] = 1  # New cell is born
    return new_grid

# Function to add randomness to the grid
def add_randomness():
    for _ in range(5):  # Add 5 random live cells
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        grid[y][x] = 1

# Function to draw the grid on the display
def draw_grid():
    display.fill(0)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                # Draw a 2x2 square for each live cell
                display.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, 1)
    display.show()

# Main Game of Life function
def game_of_life():
    global grid, last_button_state, randomness_counter
    while True:
        # Check if exit button is pressed (with debounce)
        current_button_state = btn_exit.value()
        if current_button_state != last_button_state:
            time.sleep_ms(20)  # Debounce
            if not btn_exit.value():
                break
        last_button_state = current_button_state
        
        # Draw the grid
        draw_grid()
        
        # Update the grid
        grid = update_grid()
        
        # Add randomness every 10 steps
        randomness_counter += 1
        if randomness_counter >= 10:
            add_randomness()
            randomness_counter = 0
        
        # Wait a bit for the next frame
        time.sleep(0.1)

# Start the Game of Life
game_of_life()

# Clear the display before exiting
display.fill(0)
display.show()
