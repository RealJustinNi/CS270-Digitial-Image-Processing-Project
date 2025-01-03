function [boundary_region,smooth_region] = extract_boundary(final_mask,radius_erode,radius_dilate2)

% 进行掩膜腐蚀操作以提取边界
    se_erode = strel('disk', radius_erode);
    eroded_mask = imerode(final_mask, se_erode); % 腐蚀操作
    boundary_region = final_mask & ~eroded_mask;    % 获取阴影边界
    se_dialate =  strel('disk', radius_dilate2);
    smooth_region = imdilate(boundary_region,se_dialate);
    
    % figure;
    % subplot(1,2,1);
    % imshow(boundary_region,[]);
    % title("Boundary Region");
    % subplot(1,2,2);
    % imshow(smooth_region,[]);
    % title("Smooth Region");
end