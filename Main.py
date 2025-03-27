from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk 
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
import datetime
import webbrowser
import qrcode
import random
import cv2
import sys
from PIL import Image, ImageTk
import PIL.Image
import imageio
import threading

# Initialize the main window
main = Tk()
main.attributes('-fullscreen', True)
main.title("Authentication of products-Counterfeit Elimination Using BlockChain")

# Get screen dimensions
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

# Video file path
video_name = "bg\\o4.webp"  # Ensure this path is correct
video = imageio.get_reader(video_name) 

# Create a label to display the video
my_label = tkinter.Label(main)
my_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

# Persistent reference to the current frame image
current_frame_image = None

def stream(label):
    global current_frame_image  # Use a global variable to keep the reference
    for image in video.iter_data():
        # Resize the frame to match the screen resolution
        frame = Image.fromarray(image).resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        frame_image = ImageTk.PhotoImage(frame)
        label.config(image=frame_image)
        label.image = frame_image  # Keep a reference to avoid garbage collection
        current_frame_image = frame_image  # Update the persistent reference

# Start the video stream in a separate thread
thread = threading.Thread(target=stream, args=(my_label,))
thread.daemon = 1  # Daemonize thread to exit when the main program exits
thread.start()

def run1():
    main.destroy()
    import AdminMain

def run2():
    main.destroy()
    import UserMain

def run3():
    main.destroy()
    import distributed

def run13():
    main.destroy()
    import login


def quiti():
    main.destroy()

# Set transparent color (if needed)
main.wm_attributes('-transparentcolor', '#ab23ff')

# Title label

font = ('times', 28, 'bold')
title = Label(main, text='Authentication of products-Counterfeit Elimination Using BlockChain')
title.config(bg='black', fg='#1ebbb0')
title.config(font=font)
title.config(height=2, width=50)
title.place(x=10, y=45)


# Buttons
font1 = ('times', 22, 'bold')

try:
    user_image = Image.open("bg\\m6.png")  # Load the image
    user_image = user_image.resize((150, 150), Image.Resampling.LANCZOS)  # Resize the image
    user_photo = ImageTk.PhotoImage(user_image)  # Convert to PhotoImage
    user_image_label = Label(main, image=user_photo, bg='black')  # Create a label for the image
    user_image_label.image = user_photo  # Keep a reference to avoid garbage collection
    user_image_label.place(x=480, y=330)  # Position the image above the User Page button
except Exception as e:
    print(f"Error loading image: {e}")

saveButton = tkinter.Button(main, text="Industrial login", bg="black", fg="#1ebbb0", command=run1)
saveButton.place(x=450, y=500)
saveButton.config(font=font1)

try:
    user_image = Image.open("bg\\u5.png")  # Load the image
    user_image = user_image.resize((150, 150), Image.Resampling.LANCZOS)  # Resize the image
    user_photo = ImageTk.PhotoImage(user_image)  # Convert to PhotoImage
    user_image_label = Label(main, image=user_photo, bg='black')  # Create a label for the image
    user_image_label.image = user_photo  # Keep a reference to avoid garbage collection
    user_image_label.place(x=150, y=330)  # Position the image above the User Page button
except Exception as e:
    print(f"Error loading image: {e}")

searchButton = tkinter.Button(main, text="User Page", bg="black", fg="#1ebbb0", command=run2)
searchButton.place(x=150, y=500)
searchButton.config(font=font1)


# Load the image using Pillow
home_image_pil = Image.open("bg\\n1.png")

# Resize the image to 10x10 with high-quality resampling
home_image_pil = home_image_pil.resize((90, 90), Image.Resampling.LANCZOS)

# Ensure the image has transparency (if it doesn't, this step will add it)
home_image_pil = home_image_pil.convert("RGBA")

# Convert the Pillow image to a Tkinter-compatible format
home_image = ImageTk.PhotoImage(home_image_pil)

# Home Button with the processed image
homeButton = Button(main, image=home_image, bg="black", command=run13, borderwidth=0)
homeButton.config(highlightthickness=0)  # Remove the highlight border

# Calculate position for top-right corner with 10px margin
margin_top = 45  # 10px margin from the top
margin_right = 210  # 10px margin from the right
homeButton_width = 10  # Width of the resized image
homeButton_height = 10  # Height of the resized image
homeButton_x = screen_width - homeButton_width - margin_right  # X position (right margin)
homeButton_y = margin_top  # Y position (top margin)

# Place the button at the calculated position
homeButton.place(x=homeButton_x, y=homeButton_y)

# Close Button
font3 = ('times', 25, 'bold')
# Close Button
closeButton = tkinter.Button(main, text="Exit", bg="black" , fg="#1ebbb0", command=quiti)
closeButton.config(font=font3)

# Calculate position for top-right corner with 20px margin at the top
margin_top = 60  # 20px margin at the top
margin_right = 20  # 20px margin at the right (optional, if you want margin on the right as well)
closeButton_width = closeButton.winfo_reqwidth()  # Get the width of the button
closeButton_height = closeButton.winfo_reqheight()  # Get the height of the button
closeButton_x = screen_width - closeButton_width - margin_right  # X position (right margin)
closeButton_y = margin_top  # Y position (top margin)

# Place the button at the calculated position
closeButton.place(x=closeButton_x, y=closeButton_y)

# Set background color (fallback if video fails)
main.config(bg='cornflower blue')

# Run the application
main.mainloop()