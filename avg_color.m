close all
tic
% open video file
vid = VideoReader('HWAC 2019 Final Vimeo.mp4');
% test read a frame
frame = read(vid,60*10);
imshow(frame)

% initialize video length
% numFrames = 1000; % comment this out to run full length
numFrames = vid.NumFrames; % comment this out to run first 1000 frames

% initialize and calculate mean color for each frame
mean1 = cell(numFrames,1);
i_pcent = 0;
i_toc = toc;
for i = 1:numFrames
    fr = read(vid,i); % read next frame
    % calculate mean of each color in frame
    mean1{i} = [mean(mean(fr(:,:,1))),mean(mean(fr(:,:,2))),...
                mean(mean(fr(:,:,3)))]./255;
    % progress counter
    if floor(i*100)/numFrames>i_pcent
        i_pcent = i_pcent+1;
        est_time_remaining = (100-i_pcent)*(toc-i_toc);
        disp(strcat({' '},'Averaging Progress:',{' '},string(i_pcent),...
            '% Est. duration remaining:',{' '},...
            string(est_time_remaining)));
        i_toc = toc;
    end
end

% generate the composite image
aspect_ratio = 21/9;
if numFrames > 2^11
    
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