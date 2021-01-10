import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
import ttk
from PIL import Image, ImageTk
import cv2
import time
import os, os.path
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger


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
        k = int((count/video_length)*30)
        progressbar['value'] = k
        root.update_idletasks()
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
    path_watermark = 'watermark{0}.pdf'
    #c = canvas.Canvas('watermark.pdf')

    # Draw the image at x, y. I positioned the x,y to be where i like here
    path = 'Frames/{0}.jpg'
    x = 45.67
    y = 794.85
    num_frames = len([name for name in os.listdir('Frames/')])

    #if num_frames > 224:
    #    num_frames = 224
    pages = 1
    columns = 1
    new_page = 1
    never_saved = 1
    list_canvas = []
    for num in range(1, num_frames):

        if new_page:
            c = canvas.Canvas(path_watermark.format(pages))
            new_page = 0

        try:
            c.drawImage(path.format(num), x, y, width=27.71, height=17.5)

            y -= 28.345
            if num % 28 == 0:
                x += 68.033
                y = 794.85
                columns += 1

            if columns == 9:
                x = 45.67
                pages += 1
                new_page = 1
                columns = 1
                c.save()
                list_canvas.append(c)
                never_saved = 0

        except IOError:
            print("Couldn't use frame number " + str(num))

        k = 40 + int((num / num_frames) * 30)
        progressbar['value'] = k
        root.update_idletasks()

    if never_saved:
        c.save()
        list_canvas.append(c)

    # Get the watermark file you just created
    #watermark = PdfFileReader(open("watermark.pdf", "rb"))

    # Get our files ready
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open("LK601-A4film-template-5mm.pdf", "rb"))

    # Number of pages in input document
    page_count = input_file.getNumPages()

    # Go through all the input file pages to add a watermark to them
    for n in range(len(list_canvas)):

        # Get the watermark file you just created
        #with open(path_watermark.format(n+1), "rb") as file:
        file = open(path_watermark.format(n+1), "rb")
        #file = open(path_watermark.format(n+1), "rb")
        watermark = PdfFileReader(file)
        print("Watermarking page {} of {}".format(n+1, len(list_canvas)))

        # merge the watermark with the page
        input_page = input_file.getPage(0)
        input_page.mergePage(watermark.getPage(0))

        # add page from input file to output document
        output_file.addPage(input_page)
        path_merged = 'merged_document{0}.pdf'
        f = open(path_merged.format(n+1), "wb")
        output_file.write(f)
        f.close()
        file.close()

        k = 80 + int((n / len(list_canvas)) * 30)
        progressbar['value'] = k

    merger = PdfFileMerger()

    for i in range(len(list_canvas)):
        with open(path_merged.format(i + 1), "rb") as file2:
            merger.append(PdfFileReader(file2), pages=(0, 1))
    # finally, write "output" to document-output.pdf
    #file3 = open("document-output.pdf","w")
    saveHere = asksaveasfilename(filetypes = [("PDF files", "*.pdf")], defaultextension = [("PDF files", "*.pdf")])
    merger.write(os.path.join(saveHere))
    #with open("document-output.pdf", "wb") as outputStream:
    #    output_file.write(outputStream)

    #Deleting all files created for the conversion
    dir_name = "Frames/"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".jpg"):
            os.remove(os.path.join(dir_name, item))

    dir_name = "."
    test = os.listdir(dir_name)
    for item in test:
        if item.startswith("merged_document") or item.startswith("watermark"):
            os.remove(os.path.join(dir_name, item))

    print("Done")
    progressbar['value'] = 100

def UploadAction():
    filename = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    print('Selected:', filename)
    output_loc = 'Frames/'
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

button = tk.Button(root, text='Upload MP4 file', height=10, width=40, command=UploadAction)
button.place(x=500,y =400)
button.pack()

progressbar = ttk.Progressbar(root, length=300, orient=HORIZONTAL, mode="determinate")
progressbar.pack()

root.mainloop()
