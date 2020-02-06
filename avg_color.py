import numpy as np
import cv2
import time
start_time = time.time()

# open video file
filename = 'dwts05.mp4'
vid = cv2.VideoCapture(filename)
if (vid.isOpened()== True):
    print(filename + ' opened')
else:
    print("Error opening video stream or file")

# initialize video length
full_length = False
if full_length:
    numFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    print('numFrames = ')
    print(numFrames)
else:
    numFrames = 100

# calculate mean color for each frame
mean1 = np.zeros([numFrames,3])
i_pcent = 0
i_toc = time.time()
duration = zeros(1,100)
for i in range(numFrames):
    ret, frame = vid.read()
    # frame axis 0 is row, axis 1 is col, axis 2 is rgb
    mean1[i] = [np.mean(frame[:,:,0]),np.mean(frame[:,:,1]),np.mean(frame[:,:,2])]
