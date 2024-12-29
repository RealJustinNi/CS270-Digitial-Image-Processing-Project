function shadow_mask = detect_shadow(img)
gray_img = rgb2gray(img);
% show hist
%imhist(gray_img);
[nums,grayLevels] = imhist(gray_img);
[peaks, locs] = findpeaks(nums);

% most left peak in hist
[~, idx] = max(peaks);
leftmostPeakLevel = grayLevels(locs(idx));

thresholdLow = leftmostPeakLevel - 2; % 下界灰度值
thresholdHigh = leftmostPeakLevel + 2; % 上界灰度值

% 只选择在这个范围内的像素
mask = gray_img >= thresholdLow & gray_img <= thresholdHigh;

% 创建一个标记图像来显示原图中的对应区域
markedImage = img;
markedImage(repmat(~mask, [1, 1, size(img, 3)])) = 0; % 将范围外的像素设置为黑色

%imshow(markedImage);

shadow_mask = gray_img;
% should be MxNx3
shadow_mask = cat(3,shadow_mask,shadow_mask,shadow_mask);
end