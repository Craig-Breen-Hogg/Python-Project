
import pyautogui
from PIL import ImageGrab
import time

# Define the region where obstacles appear (adjust based on your screen)
# You can use pyautogui.position() to find coordinates
x_start, y_start, width, height = 600, 400, 150, 50  # Example values

def detect_obstacle():
    """Check if there is an obstacle in the defined region."""
    screen = ImageGrab.grab(bbox=(x_start, y_start, x_start + width, y_start + height))
    pixels = screen.getdata()
    for pixel in pixels:
        # Obstacles are usually dark (near black)
        if pixel[0] < 100 and pixel[1] < 100 and pixel[2] < 100:
            return True
    return False

def play_game():
    print("Starting bot in 3 seconds...")
    time.sleep(3)
    pyautogui.press('space')  # Start the game
    time.sleep(1)

    while True:
        if detect_obstacle():
            pyautogui.press('space')  # Jump
            time.sleep(0.1)  # Small delay to avoid double jumps

if __name__ == "__main__":
    play_game()

# Install dependencies:
# Shellpip install pyautogui pillowShow more lines

# Open the T-Rex game in Chrome and make sure it’s visible.
# Adjust the x_start, y_start, width, and height values to match the obstacle detection area on your screen.
# Run the script:
# Shellpython trex_bot.pyShow more lines

# The bot will start playing automatically.