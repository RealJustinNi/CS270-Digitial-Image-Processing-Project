ratio = 3; % 阈值检测的参数，可正可负
radius = 3; % 做开运算去除噪声的半径
radius_dilate = 1; % 用于区域增长的半径（一般不改）
radius_erode = 6;  % 用于提取边界做腐蚀的半径
radius_dilate2 = 1; % 用于模糊边界做膨胀的半径
sigma = 2; % 生成高斯核

img         = imread('CS270-Digitial-Image-Processing\project\dataset\shadow/_MG_2923.jpg');
shadow_mask = detect_shadow(img,ratio);
[open_mask,x,y] = select_seed(shadow_mask,radius);
final_mask  = region_growing(open_mask,radius_dilate,x,y);
[boundary_region,smooth_region] = extract_boundary(final_mask,radius_erode,radius_dilate2);
corrected_img = shadow_removal(img,boundary_region,smooth_region,final_mask,sigma);
figure;
imshow(corrected_img);
title('Shadow Removed Image');