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

# Parameters for Matrix effect
NUM_STREAMS = 8  # Number of falling character streams
CHAR_HEIGHT = 8  # Height of each character
SPEED = 50       # Scroll speed (higher is slower)

# Characters used for Matrix effect (uppercase, lowercase, numbers and symbols)
MATRIX_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~"

def matrix_effect():
    # Initialize character streams
    streams = []
    for _ in range(NUM_STREAMS):
        streams.append({
            'x': random.randint(0, WIDTH - 1),  # Random X position
            'y': random.randint(-HEIGHT, 0),    # Random Y position (off-screen)
            'speed': random.randint(1, 3),      # Scroll speed
            'chars': [],                        # List of characters in the stream
            'brightness': random.choice([1, 1, 1, 2, 2, 3])  # Random brightness
        })
    
    while True:
        # Check if exit button is pressed
        if not btn_exit.value():
            break
        
        # Clear display
        display.fill(0)
        
        # Update and draw each stream
        for stream in streams:
            # Add new random character at top of stream
            if random.randint(0, 10) < 3:  # Probability to add new character
                char = random.choice(MATRIX_CHARS)
                stream['chars'].insert(0, (char, stream['brightness']))
            
            # Remove characters that go off-screen
            if len(stream['chars']) > HEIGHT // CHAR_HEIGHT:
                stream['chars'].pop()
            
            # Move stream downward
            stream['y'] += stream['speed']
            if stream['y'] > HEIGHT:
                stream['y'] = random.randint(-HEIGHT, 0)  # Reposition stream at top
                stream['chars'] = []  # Reset characters
            
            # Draw characters in the stream
            for i, (char, brightness) in enumerate(stream['chars']):
                y_pos = stream['y'] + i * CHAR_HEIGHT
                if 0 <= y_pos < HEIGHT:  # Only draw if character is visible
                    # Simulate brightness with thicker pixels
                    if brightness == 1:
                        display.text(char, stream['x'], y_pos, 1)
                    elif brightness == 2:
                        display.text(char, stream['x'], y_pos, 1)
                        display.text(char, stream['x'] + 1, y_pos, 1)
                    elif brightness == 3:
                        display.text(char, stream['x'], y_pos, 1)
                        display.text(char, stream['x'] + 1, y_pos, 1)
                        display.text(char, stream['x'], y_pos + 1, 1)
        
        # Update display
        display.show()
        
        # Wait for next frame
        time.sleep_ms(SPEED)

# Start Matrix effect
matrix_effect()

# Clear display before exiting
display.fill(0)
display.show()
