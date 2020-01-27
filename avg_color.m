vid = VideoReader('567326203.mp4')
frame = read(vid,60*10);
imshow(frame)

mean1 = [mean(mean(frame(:,:,1))),mean(mean(frame(:,:,2))),mean(mean(frame(:,:,3)))]
%numFrames = 1000;
numFrames = vid.NumFrames;
mean2 = cell(numFrames,1)

for i = 1:numFrames
    fr = read(vid,i);
    mean2{i} = [mean(mean(fr(:,:,1))),mean(mean(fr(:,:,2))),mean(mean(fr(:,:,3)))];
end

gr = cell2mat(mean2) 
grp = zeros(300,numFrames,3);
for i = 1:numFrames
    grp(:,i,1) = gr(i,1);
    grp(:,i,2) = gr(i,2);
    grp(:,i,3) = gr(i,3);
end
imshow(grp./255)
imwrite(grp./255,'avg_color_test.png')
imshow(grp(:,:,1)./255)
imshow(grp(:,:,2)./255)
imshow(grp(:,:,3)./255)
