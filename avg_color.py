import numpy as np
import cv2

# open video file
filename = 'dwts05.mp4'
vid = cv2.VideoCapture(filename)
if (vid.isOpened()== True):
    print(filename + ' opened')
else:
    print("Error opening video stream or file")

# initialize video length
full_length = True
if full_length:
    numFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    print(numFrames)
else:
    numFrames = 1000

# calculate mean color for each frame
mean1 = np.zeros([numFrames,1])
for i in range(numFrames):
    ret, frame = vid.read()
    # frame axis 0 is row, axis 1 is col, axis 2 is rgb
    red = frame[:,:,1]
    print(np.size(red,axis=0))
    print(np.size(red,axis=1))
    #mean1[i] = [np.mean(frame[:,:,1]),np.mean(frame[:,:,2])]
    # print(mean1[i])
    break
    # cv2.imshow('frame',frame)
