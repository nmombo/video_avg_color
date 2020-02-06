import numpy as np
import cv2
import time
start_time = time.time()

# open video file
filename = 'sample_vid.mp4'
vid = cv2.VideoCapture(filename)
if (vid.isOpened()== True):
    print(filename + ' opened')
else:
    print("Error opening video stream or file")

# initialize video length
full_length = True
if full_length:
    numFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
else:
    numFrames = 1000
print('numFrames = ')
print(numFrames)

# calculate mean color for each frame
mean1 = np.zeros([numFrames,3])
i_pcent = 0
i_toc = time.time()
duration = np.zeros([100,1])
for i in range(numFrames):
    # read next frame
    ret, frame = vid.read() # frame axis=0 is row, axis=1 is col, axis=2 is rgb
    # calculate mean of each color in frame
    mean_red = np.mean(frame[:,:,0])
    mean_gre = np.mean(frame[:,:,1])
    mean_blu = np.mean(frame[:,:,2])
    mean1[i] = [mean_red,mean_gre,mean_blu]
    # progress counter
    if np.floor(i*100)/numFrames>i_pcent:
        duration[i_pcent] = time.time()-i_toc
        if i_pcent > 6:
            est_time_remaining = (100-i_pcent)*np.mean(duration[4:i_pcent])
        else:
            est_time_remaining = (100-i_pcent)*(time.time()-i_toc)
        print('Averaging Progess: '+str(i_pcent)+'%')
        print('Estim. seconds remaining: '+str(np.round(est_time_remaining,1)))
        i_toc = time.time()
        i_pcent += 1
print('Averaging Progress: 100%')