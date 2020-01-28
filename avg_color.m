close all
% open video file
vid = VideoReader('HWAC 2019 Final Vimeo.mp4');
% test read a frame
frame = read(vid,60*10);
imshow(frame)

% initialize video length
numFrames = 1000; % comment this out to run full length
% numFrames = vid.NumFrames; % comment this out to run first 1000 frames

% initialize and calculate mean frame color
mean1 = cell(numFrames,1);
for i = 1:numFrames
    fr = read(vid,i);
    mean1{i} = [mean(mean(fr(:,:,1))),mean(mean(fr(:,:,2))),...
                mean(mean(fr(:,:,3)))]./255;
end

gr = cell2mat(mean1);
grp = zeros(300,numFrames,3);
for i = 1:numFrames
    grp(:,i,1) = gr(i,1);
    grp(:,i,2) = gr(i,2);
    grp(:,i,3) = gr(i,3);
end
figure();
imshow(grp)
imwrite(grp,'avg_color_test.png')