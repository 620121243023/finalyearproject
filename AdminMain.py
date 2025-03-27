from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
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
from PIL import ImageTk, Image
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
def addProduct():
    global filename
    text.delete('1.0', END)
    pid = tf1.get()
    name = tf2.get()
    user = tf3.get()
    address = tf4.get()
    
    # First display the entered data in the text box
    text.insert(END, "Product Details to be Saved:\n")
    text.insert(END, "---------------------------\n")
    text.insert(END, f"Product ID: {pid}\n")
    text.insert(END, f"Product Name: {name}\n")
    text.insert(END, f"Company/User: {user}\n")
    text.insert(END, f"Address: {address}\n")
    text.insert(END, "\nProcessing blockchain entry...\n\n")
    
    # Generate unique digital signature for this product
    neer = hex(random.getrandbits(128))
    bytes_data = neer.encode('utf-8')
    digital_signature = sha256(bytes_data).hexdigest()
    
    # Create QR code with company logo
    global QRimg
    try:
        logo = Image.open('bg\\logo.jpg')
        basewidth = 100
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        QRcode.add_data(digital_signature)
        QRcode.make(fit=True)
        QRimg = QRcode.make_image().convert('RGB')
        pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)
        
        # Save QR code with product ID in filename
        qr_filename = f'original_barcodes\\{pid}_productQR.png'
        QRimg.save(qr_filename)
 
        if len(pid) > 0 and len(name) > 0 and len(user) > 0 and len(address) > 0:
            current_time = datetime.datetime.now() 
            # Create blockchain data string with all details
            data = f"{pid}#{name}#{user}#{address}#{str(current_time)}#{digital_signature}"
            
            # Add to blockchain
            blockchain.add_new_transaction(data)
            hash_value = blockchain.mine()
            latest_block = blockchain.chain[len(blockchain.chain)-1]
            
            # Display success message with blockchain details
            text.insert(END,"Blockchain Entry Created Successfully!\n")
            text.insert(END,"------------------------------------\n")
            text.insert(END,f"Blockchain Previous Hash: {str(latest_block.previous_hash)}\n")
            text.insert(END,f"Block No: {str(latest_block.index)}\n")
            text.insert(END,f"Product Qr-code no: {digital_signature}\n")
            
            # Save blockchain state
            blockchain.save_object(blockchain,'blockchain_contract.txt')
            
            # Display QR code
            img2 = Image.open(qr_filename)
            load = img2.resize((200,200))
            render = ImageTk.PhotoImage(load)
            img = Label(main, image=render)
            img.image = render  # Keep reference
            img.place(x=140, y=500)
            
            # Clear input fields
            tf1.delete(0, 'end')
            tf2.delete(0, 'end')
            tf3.delete(0, 'end')
            tf4.delete(0, 'end')
            messagebox.showinfo("QR Code Generator", "QR Code and blockchain entry saved successfully!")
        else:
            text.insert(END,"\nERROR: Please enter all details")
    except Exception as e:
        text.insert(END,f"\nError occurred: {str(e)}")
def searchProduct():
    text.delete('1.0', END)
    pid = tf1.get().strip()  # Remove any whitespace

    if not pid:
        text.insert(END, "Please enter a Product ID to search")
        return

    product_found = False
    for i in range(len(blockchain.chain)):
        if i > 0:  # Skip genesis block
            block = blockchain.chain[i]
            for transaction in block.transactions:
                try:
                    arr = transaction.split("#")
                    if arr[0] == pid:
                        # Generate QR code display
                        try:
                            logo = Image.open('bg\\logo.jpg')
                            basewidth = 100
                            wpercent = (basewidth/float(logo.size[0]))
                            hsize = int((float(logo.size[1])*float(wpercent)))
                            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                            
                            QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                            QRcode.add_data(arr[5])
                            QRcode.make(fit=True)
                            QRimg = QRcode.make_image().convert('RGB')
                            pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
                            QRimg.paste(logo, pos)
                            
                            qr_filename = f'original_barcodes\\{pid}_productQR.png'
                            QRimg.save(qr_filename)
                            
                            # Display product details
                            text.insert(END, f"Product Details (Block {i}):\n\n")
                            text.insert(END, f"Product ID: {arr[0]}\n")
                            text.insert(END, f"Product Name: {arr[1]}\n")
                            text.insert(END, f"Company/User: {arr[2]}\n")
                            text.insert(END, f"Address: {arr[3]}\n")
                            text.insert(END, f"Registration Date: {arr[4]}\n")
                            text.insert(END, f"QR Code Hash: {arr[5]}\n")
                            
                            # Display QR code
                            img2 = Image.open(qr_filename)
                            load = img2.resize((200,200))
                            render = ImageTk.PhotoImage(load)
                            img = Label(main, image=render)
                            img.image = render  # Keep reference
                            img.place(x=140, y=500)
                            
                            product_found = True
                            break
                        except Exception as e:
                            text.insert(END, f"\nError generating QR code: {str(e)}")
                            product_found = True
                            break
                except Exception as e:
                    text.insert(END, f"\nError processing block {i}: {str(e)}")
                    continue
            
            if product_found:
                break

    if not product_found:
        text.insert(END, f"No product found with ID: {pid}")
        
    
    









    

main.wm_attributes('-transparentcolor', '#ab23ff')
font = ('times', 30, 'bold')
title = Label(main, text='Blockchain-Powered Product Authentication and Registration')
title.config(bg="#1ebbb0",fg='black')  
title.config(font=font)           
title.config(height=2, width=47)       
title.place(x=10,y=45)

font1 = ('times', 13, 'bold')

# Labels and Entries with black background and #1ebbb0 text color
l1 = Label(main, text='Product ID :', bg='black', fg='#1ebbb0')  # Set background and foreground colors
l1.config(font=font1)
l1.place(x=280, y=200)

tf1 = Entry(main, width=80, bg='black', fg='#1ebbb0')  # Set background and foreground colors
tf1.config(font=font1)
tf1.place(x=470, y=200)

l2 = Label(main, text='Product Name :', bg='black', fg='#1ebbb0')  # Set background and foreground colors
l2.config(font=font1)
l2.place(x=280, y=250)

tf2 = Entry(main, width=80, bg='black', fg='#1ebbb0')  # Set background and foreground colors
tf2.config(font=font1)
tf2.place(x=470, y=250)

l3 = Label(main, text='Company/User Details :', bg='black', fg='#1ebbb0')  # Set background and foreground colors
l3.config(font=font1)
l3.place(x=280, y=300)

tf3 = Entry(main, width=80, bg='black', fg='#1ebbb0')  # Set background and foreground colors
tf3.config(font=font1)
tf3.place(x=470, y=300)

l4 = Label(main, text='Address Details :', bg='black', fg='#1ebbb0')  # Set background and foreground colors
l4.config(font=font1)
l4.place(x=280, y=350)

tf4 = Entry(main, width=80, bg='black', fg='#1ebbb0')  # Set background and foreground colors
tf4.config(font=font1)
tf4.place(x=470, y=350)

font2 = ('times', 22, 'bold')

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

saveButton = Button(main, text="Save Product with Blockchain Entry",bg="black", fg="#1ebbb0", command=addProduct)
saveButton.place(x=420,y=400)
saveButton.config(font=font1)

searchButton = Button(main, text="Retrieve Product Data", bg="black", fg="#1ebbb0",command=searchProduct)
searchButton.place(x=850,y=400)
searchButton.config(font=font1)

font1 = ('times', 13, 'bold')
# Text widget with black background and #1ebbb0 text color
text = Text(main, height=15, width=100, bg='black', fg='#1ebbb0')  # Set background and foreground colors
scroll = Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=300, y=450)
text.config(font=font1)

main.config(bg='cornflower blue')
main.mainloop()