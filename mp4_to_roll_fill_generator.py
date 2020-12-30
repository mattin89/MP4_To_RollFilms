import cv2
import time
import os, os.path
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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

    path = '/Roll Film/{0}.jpg'
    pdf = PdfFileWriter()
    x = 50
    y = 800
    for num in range(1, 67):  # for each slide
        # Using ReportLab Canvas to insert image into PDF
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas('watermark.pdf', pagesize=A4)
        # Draw image on Canvas and save PDF in buffer
        imgDoc.drawImage(path.format(num), x, y, width=28.35, height=14.17)
        # x, y - start position
        # in my case -25, -45 needed
        imgDoc.save()
        y += 50
        #if num % 28 == 0:
        #    x += 50
        #    y = 800

    # Use PyPDF to merge the image-PDF into the template
    pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))

    pdf.write(open("LK601-A4film-template-5mm.pdf","wb"))

if __name__=="__main__":

    input_loc = '/Roll Film/Snapchat-1045260453.mp4'
    output_loc = '/Roll Film/'
    video_to_frames(input_loc, output_loc)
    gen_pdf()
