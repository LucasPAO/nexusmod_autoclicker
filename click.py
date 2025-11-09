import cv2
import pyautogui
import numpy as np
import time
import os
from sys import exit

# Path of default images, only custom_download can be changed to another image
# Won't work if images are not in the same folder as the script
# Names must be the same as below
button_ = ["custom_download.png", "download.png", "lr_download.png", "hr_download.png"]
buttons = len(button_)

# Error
for name in button_:
    if not os.path.isfile(name):
        print(f"Error: {name} not found in the script folder.")
        trash = input("Press enter to exit.")
        exit(1)

template_ = [0] * buttons
template_h = [0] * buttons
template_w = [0] * buttons

# Initialize default images
for i in range(buttons):
    template_[i] = cv2.imread(button_[i], cv2.IMREAD_GRAYSCALE)
    # Error
    if template_[i] is None:
        print(f"Error: Could not load image {button_[i]}")
        trash = input("Press enter to exit.")
        exit(1)
    template_h[i], template_w[i] = template_[i].shape[:2]



# Main function to find and click
def find_and_click():
    match = None

    for _ in range(4): # Scroll 4 times to find the button    
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot_array = np.array(screenshot)
        screen = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2GRAY)
        
        # Compare screen with all the buttons
        for i in range(buttons):
            result = cv2.matchTemplate(screen, template_[i], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            limiar = 0.7  # As closer to 1 to be more precise
            if max_val >= limiar:
                match = button_[i]
                print(f"\n{match} found!\n")
                break
        
        # If no button found, scroll down and try again
        if match is None:
            print("Button not found. Scrolling down\n")
            pyautogui.scroll(-700) # Scroll down if no button found
            time.sleep(1) # Wait for screen to update
            continue
        else: # If a match is found, exit the scroll loop
            break

    # If no button found after 4 scrolls
    # Exit function
    if match is None:
        pyautogui.hotkey('ctrl', 'home') # Go back to top
        print("Button not found. Awaiting 8 seconds\n")
        return 0

    # If button is found, calculate center position
    button_x, button_y = max_loc
    center_x = button_x + (template_w[i]) // 2
    center_y = button_y + (template_h[i]) // 2

    # Move and click
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    pyautogui.click()
    return 0


# Init
print("Resize Wabbajack to fullscreen mode.")
print("Press enter to begin...")
trash = input("Press CTRL + C to stop the program.")
print('')
print("Starting in 3 seconds...")

time.sleep(3)

# Main
try:
    while (1):
        find_and_click()
        time.sleep(8)
except KeyboardInterrupt:
    print("\nProgram stopped (CTRL + C).")
    time.sleep(2)
    exit(1)
except pyautogui.FailSafeException:
    print("\nProgram stopped by fail-safe (mouse to top-left corner).")
    time.sleep(3)
    exit(1)
