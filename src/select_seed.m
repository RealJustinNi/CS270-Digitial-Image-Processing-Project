function [open_mask,x,y] = select_seed(shadow_mask,radius)
    se1 = strel('disk', radius); 
    open_mask = imopen(shadow_mask, se1); 
    
    % 显示初始掩码并提示用户选择点
    %figure;
    %imshow(open_mask, []);
    %title('Click on the mask to select seed points. Press Enter when done.');
    %hold on;
    
    % 交互式获取用户点击的基础点
    [x, y] = ginput(); 
    x = round(x);      
    y = round(y);
    
    % 验证用户选择的点是否在图像范围内
    [h, w] = size(open_mask);
    valid_points = (x > 0 & x <= w) & (y > 0 & y <= h);
    x = x(valid_points);
    y = y(valid_points);
    
    % 在图像上标记用户选择的基础点
    %plot(x, y, 'r*', 'MarkerSize', 10);
end