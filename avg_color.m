close all
tic

% open video file
vid = VideoReader('sample_vid.mp4');

% initialize video length
full_length = 0;
test_length = 1000;
if full_length
    numFrames = vid.NumFrames;
else
    numFrames = test_length;
end

% initialize and calculate mean color for each frame
mean1 = cell(numFrames,1);
i_pcent = 0;
i_toc = toc;
duration = zeros(1,100);
for i = 1:numFrames
    fr = read(vid,i); % read next frame
    % calculate mean of each color in frame
    mean1{i} = [mean(mean(fr(:,:,1))),mean(mean(fr(:,:,2))),...
                mean(mean(fr(:,:,3)))]./255;
    % progress counter
    if floor(i*100)/numFrames>i_pcent
        i_pcent = i_pcent+1;
        duration(i_pcent) = toc-i_toc;
        if i_pcent > 6
            est_time_remaining = (100-i_pcent)*mean(duration(5:i_pcent))+1;
        else
            est_time_remaining = (100-i_pcent)*(toc-i_toc)+1;
        end
        disp(strcat('Averaging Progress:',{' '},string(i_pcent),'%'));
        disp(strcat('Estim. seconds remaining:',{' '},...
            string(round(est_time_remaining))));
        i_toc = toc;
    end
end

% generate the shape of the composite image
shape_toc = toc;
aspect_ratio = 21/9;
width = numFrames;
divs = 0;
while width > aspect_ratio*1440*2
    width = floor(width/2);
    divs = divs+1;
end
height = floor(width/aspect_ratio);
dims = [width,height];
shape_duration = toc-shape_toc;
disp(strcat('Shape duration',{' '},string(shape_duration),{' '},'s'))

% compress the frames for long videos
compression_toc = toc;
mean2 = cell(width,1);
if divs > 0
    for i = 0:width-1
        red = zeros(1,2^divs);
        blue = zeros(1,2^divs);
        green = zeros(1,2^divs);
        for j = 1:2^divs
            red(j) = mean1{i*2^divs+j}(1);
            blue(j) = mean1{i*2^divs+j}(2);
            green(j) = mean1{i*2^divs+j}(3);
        end
        mean2{i+1,1} = [mean(red),mean(blue),mean(green)];
    end
else
    mean2 = mean1;
end
compression_duration = toc - compression_toc;
disp(strcat('Compression duration',{' '},...
    string(compression_duration),{' '},'s'))

% synthesize image file
gr = cell2mat(mean2);
grp = zeros(height,width,3);
for i = 1:width
    grp(:,i,1) = gr(i,1);
    grp(:,i,2) = gr(i,2);
    grp(:,i,3) = gr(i,3);
end
figure();
imshow(grp);
imwrite(grp,'avg_color_test.png');
disp(toc-i_toc);
