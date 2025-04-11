from machine import Pin, I2C
import ssd1306
import time
import random

# I2C and display configuration
i2c = I2C(0, scl=Pin(1), sda=Pin(2))
display = ssd1306.SSD1306_I2C(64, 32, i2c)

# Button configuration
btn_left = Pin(11, Pin.IN, Pin.PULL_UP)
btn_right = Pin(13, Pin.IN, Pin.PULL_UP)
btn_exit = Pin(9, Pin.IN, Pin.PULL_UP)

# Game variables
DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32
PADDLE_WIDTH = 16
PADDLE_HEIGHT = 2
BALL_SIZE = 2
BRICK_HEIGHT = 2
BRICK_WIDTH = 5
MAX_BRICKS = 24

class BrickBreaker:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        # Game state initialization
        self.paddle_x = (DISPLAY_WIDTH - PADDLE_WIDTH) // 2
        
        # Random initial ball position
        self.ball_x = random.randint(10, DISPLAY_WIDTH - 10)  # Avoid edges
        self.ball_y = DISPLAY_HEIGHT - 5
        
        # Random initial ball direction
        self.ball_dx = random.choice([-1, 1])  # Left or right
        self.ball_dy = -1  # Always upwards at the start
        
        # Brick generation
        self.bricks = []
        for row in range(3):
            for i in range(MAX_BRICKS // 3):
                # Centered x position calculation
                total_bricks_width = (BRICK_WIDTH + 1) * (MAX_BRICKS // 3)
                start_x = (DISPLAY_WIDTH - total_bricks_width) // 2
                brick_x = start_x + i * (BRICK_WIDTH + 1)
                brick_y = 2 + row * (BRICK_HEIGHT + 1)
                self.bricks.append({'x': brick_x, 'y': brick_y, 'alive': True})
    
    def move_paddle(self):
        # Paddle movement
        if not btn_left.value() and self.paddle_x > 0:
            self.paddle_x -= 2
        if not btn_right.value() and self.paddle_x < DISPLAY_WIDTH - PADDLE_WIDTH:
            self.paddle_x += 2
    
    def move_ball(self):
        # Ball movement
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Side wall bounce
        if self.ball_x <= 0 or self.ball_x >= DISPLAY_WIDTH - BALL_SIZE:
            self.ball_dx *= -1
        
        # Top wall bounce
        if self.ball_y <= 0:
            self.ball_dy *= -1
        
        # Ball drop check (Game Over)
        if self.ball_y >= DISPLAY_HEIGHT - BALL_SIZE:
            return False  # Game Over
        
        # Paddle bounce
        if (self.ball_y >= DISPLAY_HEIGHT - PADDLE_HEIGHT - BALL_SIZE and
            self.paddle_x <= self.ball_x <= self.paddle_x + PADDLE_WIDTH):
            self.ball_dy *= -1
        
        # Brick collision check
        for brick in self.bricks:
            if brick['alive']:
                if (self.ball_x >= brick['x'] and 
                    self.ball_x <= brick['x'] + BRICK_WIDTH and
                    self.ball_y <= brick['y'] + BRICK_HEIGHT):
                    brick['alive'] = False
                    self.ball_dy *= -1
        
        return True  # Game continues
    
    def draw(self):
        # Clear display
        display.fill(0)
        
        # Draw bricks
        for brick in self.bricks:
            if brick['alive']:
                display.fill_rect(brick['x'], brick['y'], BRICK_WIDTH, BRICK_HEIGHT, 1)
        
        # Draw paddle
        display.fill_rect(self.paddle_x, DISPLAY_HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, 1)
        
        # Draw ball
        display.fill_rect(self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE, 1)
        
        display.show()
    
    def game_over(self):
        display.fill(0)
        display.text("GAME", 16, 8, 1)
        display.text("OVER", 16, 16, 1)
        display.show()
        time.sleep(3)
    
    def run(self):
        while True:
            # Exit check
            if not btn_exit.value():
                break
            
            # Movement
            self.move_paddle()
            
            # Check if ball fell
            if not self.move_ball():
                self.game_over()
                break
            
            # Drawing
            self.draw()
            
            # Victory check
            if all(not brick['alive'] for brick in self.bricks):
                display.fill(0)
                display.text("YOU WIN!", 8, 8, 1)
                display.show()
                time.sleep(3)
                break
            
            time.sleep(0.05)  # Game speed

# Start game
game = BrickBreaker()
game.run()
