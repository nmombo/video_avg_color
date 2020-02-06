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
full_length = False
if full_length:
    numFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
else:
    numFrames = 1500
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
mean2 = np.zeros([width,3])
if divs > 0:
    for i in range(width-1):
        red = np.zeros(1,2^divs)
        gre = np.zeros(1,2^divs)
        blu = np.zeros(1,2^divs)
        for j in range(2^divs-1):
            red[j] = mean1[i*2^divs+j,1]
            gre[j] = mean1[i*2^divs+j,2]
            blu[j] = mean1[i*2^divs+j,2]
        mean2[i] = [np.mean(red),np.mean(gre),np.mean(blu)]
else:
    mean2 = mean1

# synthesize image file
grp = np.zeros([int(height),int(width),3])
for i in range(width):
    grp[:,i] = mean2[i]
cv2.imwrite('avg_color_test_py.png',grp)
