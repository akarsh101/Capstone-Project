import subprocess
import sys
import pyautogui
import time
import os
import cv2
import pandas as pd


# Function to install required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Install required packages


install('opencv-python')
install('pandas')
install('pyautogui')


# Directories to store images and metadata
image_folder = 'E:\\Downloads\\captured_images'
metadata_folder = 'E:\\Downloads\\image_metadata'


# create directories
os.makedirs(image_folder, exist_ok=True)
os.makedirs(metadata_folder, exist_ok=True)


def capture_frame(cap, frame_index):
    try:
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("Error: Could not read frame.")
        
        # Save the image
        image_filename = os.path.join(images_folder, f'image_{frame_index}.png')
        cv2.imwrite(image_filename, frame)
        
        # Convert the frame to a DataFrame for metadata
        df = pd.DataFrame(frame.reshape(-1, 3), columns=['B', 'G', 'R'])
        
        # Save the metadata to a CSV file
        metadata_filename = os.path.join(metadata_folder, f'metadata_{frame_index}.csv')
        df.to_csv(metadata_filename, index=False)
    
    except RuntimeError as e:
        print(e)
        return False  # Indicate failure


    return True  # Indicate success


def capture_images():
    # Total images to capture
    total_captures = 100
    # Number of images to capture in each batch
    num_frames_to_capture = 10
    # Interval between batches in seconds
    wait = 10


    while True:  # Keep retrying until successful
        # Initialize the camera capture
        cap = cv2.VideoCapture(0)  # Use 0 for default camera


        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        # Loop to capture 100 images in batches of 10
        for b in range(total_captures // num_frames_to_capture):
            for i in range(num_frames_to_capture):
                if not capture_frame(cap, b * num_frames_to_capture + i):
                    cap.release()
                    print("Restarting due to error...")
                    break  # Exit inner loop to restart
            else:
                continue  # Continue outer loop if inner loop was not broken
            break  # Exit outer loop if inner loop was broken


        print(f"Captured a total of {total_images_to_capture} images.")
        cap.release()
        break  # Exit the while loop if successful


def find_and_click_buttons(button_image, scroll_attempts=5, scroll_amount=-500):
    for attempt in range(scroll_attempts):
        print(f"Attempt {attempt + 1}: Trying to locate buttons on screen...")
        
        try:
            # Find all instances of the button on the screen
            buttons = list(pyautogui.locateAllOnScreen(button_image, confidence=0.8))
            
            if not buttons:
                print("No buttons found. Scrolling...")
            else:
                print(f"Found {len(buttons)} button(s). Clicking them...")
                # Click each button found
                for button in buttons:
                    x, y = pyautogui.center(button)
                    pyautogui.click(x, y)
                    time.sleep(0.5)  # Short delay between clicks
                
                print("Scrolling down to find more buttons...")
                # Scroll down to find more buttons
                pyautogui.scroll(scroll_amount)
                time.sleep(1)  # Wait for the page to scroll
        
        except Exception as e:
            print(f"Error during button detection or clicking: {e}")


def main():
    while True:
        # Step 1: Open the Camera Privacy settings page
        subprocess.run(['start', 'ms-settings:privacy-webcam'], shell=True)


        # Wait for the settings page to load
        time.sleep(10)  # Increased wait time to ensure the page is fully loaded


        # Step 2: Find and click buttons
        button_image = 'C:\\Users\\akars\\Pictures\\toggle_button_image.png'
        if not os.path.exists(button_image):
            print(f"Button image file not found at: {button_image}")
            return
        
        find_and_click_buttons(button_image)


        print("Finished clicking on all buttons.")


        # Step 3: Capture images
        capture_images()
        
        # Wait for a key press to restart
        print("Press any key to restart the entire process...")
        key = cv2.waitKey(0)  # Wait indefinitely for a key press
        
        if key != -1:  # If any key is pressed
            print("Key pressed. Restarting...")
            continue  # Restart the loop


if __name__ == "__main__":
    main()




