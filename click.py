import cv2
import pyautogui
import numpy as np
import time

# Path of default images
botao_imagem_ = ["manual.png", "manual_download.png", "download.png", "downloadslow.png", "download75.png", "download75slow.png"]

template_ = [0] * 6
template_h = [0] * 6
template_w = [0] * 6

# Initialize default images
for i in range(6):
    template_[i] = cv2.imread(botao_imagem_[i], cv2.IMREAD_GRAYSCALE)
    template_h[i], template_w[i] = template_[i].shape[:2]

# Main function to find and click
def find_and_click():
    screenshot = pyautogui.screenshot()
    screenshot_array = np.array(screenshot)
    tela = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2GRAY)
    
    for i in range(6):
        # Find image in screen with template
        resultado = cv2.matchTemplate(tela, template_[i], cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        # Set other values to be less or more precise
        limiar = 0.7  # As closer to 1 to be precise
        if max_val >= limiar:
            if i == 0:
                print("Manual found!")
            elif i == 1:
                print("Manual download found!")
            else:
                print("Button found!")

            botao_x, botao_y = max_loc
            centro_x = botao_x + (template_w[i]) // 2
            centro_y = botao_y + (template_h[i]) // 2

            # Move and click
            pyautogui.moveTo(centro_x, centro_y, duration=0.5)
            pyautogui.click()
            return 0
        else:
            continue
    
    print("Button not found. Awaiting 7 seconds")
    return 0

# Chamar a função
print("Set Wabbajack to fullscreen mode.")
print("Press enter to begin...")
lixo = input("Press CTRL + C to close the program.")
print('')

while (1):
    find_and_click() 
    time.sleep(7)