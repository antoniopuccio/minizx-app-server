from machine import Pin, I2C
import ssd1306
import time

# Configure I2C connection
i2c = I2C(0, scl=Pin(1), sda=Pin(2))

# Initialize the display
display = ssd1306.SSD1306_I2C(64, 32, i2c)

# Configure button on pin 9
btn_home = Pin(9, Pin.IN, Pin.PULL_UP)

# Clear the display
display.fill(0)

# Center the text "Hello" on the first line
# Each character is about 8 pixels wide
hello_width = len("Hello") * 8
x_hello = (64 - hello_width) // 2
display.text("Hello", x_hello, 0, 1)

# Center the text "World" on the second line
world_width = len("World") * 8
x_world = (64 - world_width) // 2
display.text("World", x_world, 12, 1)

# Update the display
display.show()

# Wait for 5 seconds or until the button is pressed
start_time = time.time()
while time.time() - start_time < 5:
    if not btn_home.value():  # If button is pressed
        break
    time.sleep(0.1)  # Reduce CPU usage

# Clear the display before exiting
display.fill(0)
display.show()
