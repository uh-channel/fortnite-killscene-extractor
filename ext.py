from PIL import Image

import cv2
import pytesseract
import re
import sys
import os
import subprocess

pre_margin_sec = 10
post_margin_sec = 2
fps = 30
interval = 150
out_count = 0
out_dir = ''

# Get the image for OCR.
#  in:  screen image
#  out: image for OCR
def get_count_image(image):
    topRate = 332 / 1080
    bottomRate = 365 /1080
    leftRate = 1523 / 1920
    rightRate = 1780 / 1920

    height, width, channels = image.shape[:3]

    return image[int(topRate * height) : int(bottomRate * height), int(leftRate * width) : int(rightRate * width)]

# Get kill count from screen image.
#  in:  screen image
#  out: current kill count (if failed, return -1)
def get_kill_count(image):
    img = get_count_image(image)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    text = pytesseract.image_to_string(img)
    m = re.match(r'.*(\d)\s*$', text)
    try:
        if m:
            count = int(m.groups()[0])
        else :
            count = -1
    except ValueError:
        count = -1
    # print(text +  "-> " + str(count))
    return count

# Extract and output the kill scene.
#  in:  file : sourcefile, frame: detected frame
def extract_scene(file, frame):
    print ("found at : " + str(frame))
    ss = int(frame/fps) - pre_margin_sec
    basefile = os.path.splitext(os.path.basename(file))[0] + "_" + str(ss) + ".mp4"
    outfile = os.path.join(out_dir, basefile)
    if ss < 0 :
        ss = 0
    t = pre_margin_sec + post_margin_sec
    subprocess.run(('ffmpeg', '-y', '-ss', str(ss), '-i', file, '-t', str(t), '-c', 'copy', outfile))

# Process kill scene detection and extraction from video
def proc_video(file, interval):
    cap = cv2.VideoCapture(file)

    frame = 1000
    ret = True
    killCount = 0
    while ret:
        print(str(frame))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        current = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if current != frame:
            return

        ret, image = cap.read()
        if ret:
            count = get_kill_count(image)
            if count > 0 and killCount != count:
                killCount = count
                extract_scene(file, frame)
        else:
            return

        frame += interval

argv = sys.argv

if len(argv) < 6:
    print ('Usage: python3 ext.py interval pre_margin post_margin input_file output_dir')
    print ('   interval    : detection interval seconds')
    print ('   pre_margin  : margin seconds to cut before detected point')
    print ('   post_margin : margin seconds to cut after detected point')
    
else:
    interval = int(argv[1]) * fps
    pre_margin_sec = int(argv[2])
    post_margin_sec = int(argv[3])
    file = argv[4]
    out_dir = argv[5]

    os.makedirs(out_dir, exist_ok=True)
    proc_video(file, interval)