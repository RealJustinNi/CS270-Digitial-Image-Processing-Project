function final_mask = region_growing(open_mask,radius_dilate,x,y)
    final_mask = false(size(open_mask));
    
    % 区域增长
    se = strel('disk', radius_dilate);
    for i = 1:length(x)
        seed = false(size(open_mask)); 
        seed(y(i), x(i)) = true;          % 设置基础点为种子
        region = seed;
        % 扩张，直到区域稳定
        while true
            dilated = imdilate(region, se);    
            new_region = dilated & open_mask; 
            if isequal(new_region, region)     % 如果区域没有变化，则退出
                break;
            end
            region = new_region;               % 更新区域
        end
        final_mask = final_mask | region;
    end
    %figure;
    %imshow(final_mask, []);
    %title('Final Shadow Mask');
end