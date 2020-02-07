import numpy as np
import cv2
import time
from multiprocessing import Pool
from asyncio import Lock

lock = Lock()

# open video file
filename = 'sample_vid.mp4'
vid0 = cv2.VideoCapture(filename)
vid1 = cv2.VideoCapture(filename)
vid2 = cv2.VideoCapture(filename)
vid3 = cv2.VideoCapture(filename)
# if (vid.isOpened()== True): print(filename + ' opened')
# else: print("Error opening video stream or file")

# initialize video length
full_length = True
if full_length: numFrames = int(vid0.get(cv2.CAP_PROP_FRAME_COUNT))
else: numFrames = 8000
print('numFrames = ')
print(numFrames)

# calculate mean color for each frame
mean1 = np.zeros([numFrames,3])
# i_pcent = 0
# i_toc = time.time()
# duration = np.zeros([100,1])

def func_name(vid, i_parallel):
    vid.set(2,i_parallel*numFrames/4)
    for i in range(numFrames/4):
        # read next frame
        _, frame = vid.read() # frame axis=0 is row, axis=1 is col, axis=2 is rgb
        # calculate mean of each color in frame
        lock.acquire()
        mean1[i+i_parallel*numFrames/4] = np.array([np.mean(frame[:,:,0]),np.mean(frame[:,:,1]),np.mean(frame[:,:,2])])
        lock.release()

with Pool(4) as p:
    p.map(func_name,zip([vid0,vid1,vid2,vid3,0,1,2,3]))
# for i in range(numFrames):
#     # read next frame
#     _, frame = vid.read() # frame axis=0 is row, axis=1 is col, axis=2 is rgb
#     # calculate mean of each color in frame
#     mean1[i] = np.array([np.mean(frame[:,:,0]),np.mean(frame[:,:,1]),np.mean(frame[:,:,2])])
    # progress counter
    # if np.floor(i*100)/numFrames>i_pcent:
    #     duration[i_pcent] = time.time()-i_toc
    #     if i_pcent > 6: est_time_remaining = (100-i_pcent)*np.mean(duration[4:i_pcent])
    #     else: est_time_remaining = (100-i_pcent)*(time.time()-i_toc)
    #     print('Averaging Progess: '+str(i_pcent)+'%')
    #     print('Estim. seconds remaining: '+str(np.round(est_time_remaining,1)))
    #     i_toc = time.time()
    #     i_pcent += 1
print('Averaging Progress: 100%')

# generate the shape of the composite image
aspect_ratio = 21/9
min_height = 1440
width = numFrames
divs = 0
while width > aspect_ratio*min_height*2:
    width = np.floor(width/2)
    divs += 1
height = np.floor(width/aspect_ratio)

# compress the frames for long videos
mean2 = np.zeros([int(width),3])
if divs > 0:
    for i in range(int(width)-1):
        vert = np.zeros([2^divs,3])
        for j in range(2^divs-1):
            vert[j] = np.array([mean1[i*2^divs+j,0],mean1[i*2^divs+j,1],mean1[i*2^divs+j,2]])
        mean2[i] = [np.mean(vert[:,0]),np.mean(vert[:,1]),np.mean(vert[:,2])]
else:
    mean2 = mean1

# synthesize image file
grp = np.zeros([int(height),int(width),3])
for i in range(int(width)): grp[:,i] = mean2[i]
cv2.imwrite('avg_color_test_py.png',grp)

