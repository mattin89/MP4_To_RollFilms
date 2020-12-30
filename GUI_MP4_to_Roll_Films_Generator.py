import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
import cv2
import time
import os, os.path
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


def video_to_frames(input_loc, output_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.mkdir(output_loc)
    except OSError:
        pass
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        # Write the results back to output location.
        cv2.imwrite(output_loc + "/%#d.jpg" % (count+1), frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds for conversion." % (time_end-time_start))
            break

def gen_pdf():
    """Function to insert frames in the output pdf file
        and save it in an output directory.
        Args:
            None
        Returns:
            None
        """
    # Create the watermark from an image
    c = canvas.Canvas('watermark.pdf')

    # Draw the image at x, y. I positioned the x,y to be where i like here
    path = 'C:/Users/delor/Downloads/Roll Film/Frames/{0}.jpg'
    x = 45.67
    y = 794.85
    num_frames = len([name for name in os.listdir('C:/Users/delor/Downloads/Roll Film/Frames/')])

    if num_frames > 224:
        num_frames = 224

    for num in range(1, num_frames):

        try:
            c.drawImage(path.format(num), x, y, width=27.71, height=17.5)

            y -= 28.345
            if num % 28 == 0:
                x += 68.033
                y = 794.85

        except IOError:
            print("Couldn't use frame number " + str(num))

    c.save()

    # Get the watermark file you just created
    watermark = PdfFileReader(open("watermark.pdf", "rb"))

    # Get our files ready
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open("LK601-A4film-template-5mm.pdf", "rb"))

    # Number of pages in input document
    page_count = input_file.getNumPages()

    # Go through all the input file pages to add a watermark to them
    for page_number in range(page_count):
        print("Watermarking page {} of {}".format(page_number, page_count))
        # merge the watermark with the page
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        # add page from input file to output document
        output_file.addPage(input_page)

    # finally, write "output" to document-output.pdf
    with open("document-output.pdf", "wb") as outputStream:
        output_file.write(outputStream)

def UploadAction():
    filename = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    print('Selected:', filename)
    output_loc = 'C:/Users/delor/Downloads/Roll Film/Frames/'
    video_to_frames(filename, output_loc)
    gen_pdf()

root = tk.Tk()

root.geometry("1000x600")
root.title("MP4 to Roll Films converter")
root.configure(bg = 'grey')

c = Canvas(root, width=1000, height=400)
c.pack()

img1 = Image.open("mp4-pngrepo-com.png")
img1 = img1.resize((200, 200))
img1 = ImageTk.PhotoImage(img1)
c.create_image(100, 100, image=img1, anchor=NW)

img2 = Image.open("photographic-film-photography-roll-film-viewfinder-clipart-removebg-preview.png")
img2 = img2.resize((300, 300))
img2 = ImageTk.PhotoImage(img2)
c.create_image(650, 50, image=img2, anchor=NW)

img3 = Image.open("1_xDGtplbrOnaKC1ov7t23kA.png")
img3 = img3.resize((200, 200))
img3 = ImageTk.PhotoImage(img3)
c.create_image(400, 100, image=img3, anchor=NW)

button = tk.Button(root, text='Upload MP4 file', height=5, width=20, command=UploadAction)
button.place(x=500,y =500)

button.pack()

root.mainloop()