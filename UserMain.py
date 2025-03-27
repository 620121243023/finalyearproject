from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog  # get the val of user
import tkinter
from tkinter import filedialog  # help in dil handling...
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
import PIL.Image
from PIL import ImageTk, Image
import PIL.Image
import imageio
import threading
import qrtools  # generate qr
from PIL import Image
from pyzbar.pyzbar import decode
import pyzbar.pyzbar as pyzbar  # decode qr
# from pyzbar.pyzbar import ZBarSymbol

# Initialize the main window
main = Tk()
main.attributes('-fullscreen', True)
main.title("Authentication of products-Counterfeit Elimination Using BlockChain")

# Get screen dimensions
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

# Video file path
video_name = "bg\\p1.jpg"  # Ensure this path is correct
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



global filename
blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def authenticateProduct():
    text.delete('1.0', END)
    filename_ = askopenfilename(initialdir="original_barcodes")

    image = cv2.imread(filename_)
    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        digital_signature_ = obj.data
        digital_signature = digital_signature_.decode("utf-8")

    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[5] == digital_signature:
                output = ''
                text.insert(END, "Uploaded Product Barcode Authentication Successfull\n")
                text.insert(END, "Details extracted from Blockchain after Validation\n\n")
                text.insert(END, "Product ID                                 : " + arr[0] + "\n")
                text.insert(END, "Product Name                               : " + arr[1] + "\n")
                text.insert(END, "Company/User Details                       : " + arr[2] + "\n")
                text.insert(END, "Address Details                            : " + arr[3] + "\n")
                text.insert(END, "Product registered Date & Time             : " + arr[4] + "\n")
                text.insert(END, "Product QR-Code                            : " + str(digital_signature) + "\n")

                output = '''<html>
<head>
    <style>
        body {
            background-image: url('bg\\\\blk2.jpg');
            background-size: cover;
            background-attachment: fixed;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            color: #ebbb0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: auto;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #444;
            color: #1ebbb0;
            
        }
        th {
            background-color: rgba(0, 0, 0, 0.5);
            color: #1ebbb0;
        }
        tr:hover {
            background-color: rgba(50, 50, 50, 0.5);
        }
        h1 {
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Product Authentication Details</h1>
        <table border="0">
            <tr>
                <th>Field</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Block No</td>
                <td>''' + str(i) + '''</td>
            </tr>
            <tr>
                <td>Product ID</td>
                <td>''' + arr[0] + '''</td>
            </tr>
            <tr>
                <td>Product Name</td>
                <td>''' + arr[1] + '''</td>
            </tr>
            <tr>
                <td>Company/User Details</td>
                <td>''' + arr[2] + '''</td>
            </tr>
            <tr>
                <td>Address Details</td>
                <td>''' + arr[3] + '''</td>
            </tr>
            <tr>
                <td>Scan Date & Time</td>
                <td>''' + arr[4] + '''</td>
            </tr>
            <tr>
                <td>Product QR-Code No</td>
                <td>''' + str(digital_signature) + '''</td>
            </tr>
        </table>
    </div>
</body>
</html>'''
                f = open("output.html", "w")
                f.write(output)
                f.close()
                webbrowser.open("output.html", new=1)
                flag = False
                break
    if flag:
        o1 = ''
        text.insert(END, str(digital_signature) + ",  this hash is not present in the blockchain \n")
        text.insert(END, "Uploaded Product Barcode Authentication Failed: FAKE")
        o1 = '''<html>
        <head>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
            <div class="zoom-container">
                <img src="bg/f2.jpg" alt="Fake Product" class="zoom-image">
            </div>
        </body>
        </html>'''
        f = open("o1.html", "w")
        f.write(o1)
        f.close()
        webbrowser.open("o1.html", new=1)  # Open o1.html for fake products

def authenticateProductWeb():
    text.delete('1.0', END)
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, frame = cap.read()
        data, bbox, _ = detector.detectAndDecode(frame)
        digital_signature = data
        if digital_signature:
            break
        cv2.imshow("QR-Code scanner", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if key == ord("k"):  # New condition to check if 'k' is pressed
            cap.release()
            cv2.destroyAllWindows()
            return  # Exit the function to stop further execution

    cap.release()
    cv2.destroyAllWindows()
    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[5] == digital_signature:
                output = ''
                text.insert(END, "Uploaded Product Barcode Authentication Successfull\n")
                text.insert(END, "Details extracted from Blockchain after Validation\n\n")
                text.insert(END, "Product ID                   : " + arr[0] + "\n")
                text.insert(END, "Product Name                 : " + arr[1] + "\n")
                text.insert(END, "Company/User Details         : " + arr[2] + "\n")
                text.insert(END, "Address Details              : " + arr[3] + "\n")
                text.insert(END, "Scan Date & Time             : " + arr[4] + "\n")
                text.insert(END, "Product QR-Code              : " + str(digital_signature) + "\n")

                output = '<html><body><table border=1>'
                output += '<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th><th>Product digital Signature</th></tr>'
                output += '<tr><td>' + str(i) + '</td><td>' + arr[0] + '</td><td>' + arr[1] + '</td><td>' + arr[2] + '</td><td>' + arr[3] + '</td><td>' + arr[4] + '</td><td>' + str(digital_signature) + '</td></tr>'
                f = open("output.html", "w")
                f.write(output)
                f.close()
                webbrowser.open("output.html", new=1)
                flag = False
                break
    if flag:
        o1 = ''
        text.insert(END, str(digital_signature) + ",  this hash is not present in the blockchain \n")
        text.insert(END, "Uploaded Product Barcode Authentication Failed fake product")
        text.insert(END, "Uploaded Product Barcode Authentication Failed: FAKE")
        o1 = '<html><body><link rel="stylesheet" href="styles.css">'
        o1 += '<h1>FAKE PRODUCT!!</h1>'
        o1 += '</body></html>'
        f = open("o1.html", "w")
        f.write(o1)
        f.close()
        webbrowser.open("o1.html", new=1)

main.wm_attributes('-transparentcolor', '#ab23ff')
font = ('times', 30, 'bold')
title = Label(main, text='Instant Product Verification : Scan to detect Counterfeits')
title.config(bg='#1ebbb0', fg='black')
title.config(font=font)
title.config(height=2, width=47)
title.place(x=10, y=45)

font1 = ('times', 22, 'bold')

def run13():
    main.destroy()
    import Main

    #os.system('AdmMain.py',)
    

# Load the image using Pillow
home_image_pil = Image.open("bg\\h2.png")

# Resize the image to 10x10 with high-quality resampling
home_image_pil = home_image_pil.resize((100, 100), Image.Resampling.LANCZOS)

# Ensure the image has transparency (if it doesn't, this step will add it)
home_image_pil = home_image_pil.convert("RGBA")

# Convert the Pillow image to a Tkinter-compatible format
home_image = ImageTk.PhotoImage(home_image_pil)

# Home Button with the processed image
homeButton = Button(main, image=home_image, bg="black", command=run13, borderwidth=0)
homeButton.config(highlightthickness=0)  # Remove the highlight border

# Calculate position for top-right corner with 10px margin
margin_top = 40  # 10px margin from the top
margin_right = 110  # 10px margin from the right
homeButton_width = 10  # Width of the resized image
homeButton_height = 10  # Height of the resized image
homeButton_x = screen_width - homeButton_width - margin_right  # X position (right margin)
homeButton_y = margin_top  # Y position (top margin)

# Place the button at the calculated position
homeButton.place(x=homeButton_x, y=homeButton_y)

# Keep a reference to the image to prevent garbage collection
homeButton.image = home_image
scanButton = Button(main, text="Authenticate Scan",  bg="black", fg="#1ebbb0", command=authenticateProduct)
scanButton.place(x=420, y=300)
scanButton.config(font=font1)

scanButton = Button(main, text="Authenticate web Scan", bg="black", fg="#1ebbb0", command=authenticateProductWeb)
scanButton.place(x=850, y=300)
scanButton.config(font=font1)

font1 = ('times', 13, 'bold')
# Text widget with black background and #1ebbb0 text color
text = Text(main, height=15, width=100, bg='black', fg='#1ebbb0')  # Set background and foreground colors
scroll = Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=300, y=450)
text.config(font=font1)

main.config(bg='cornflower blue')
main.mainloop()