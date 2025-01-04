function corrected_img = shadow_removal(img,boundary_region,smooth_region,final_mask,sigma,offset)
    shadow_region = final_mask;  % 阴影区
    lit_region = ~final_mask;    % 非阴影区

    % 初始化去阴影图像（复制原始图像用于修改阴影区域）
    corrected_img = double(img);

    % 对 R, G, B 三个通道分别处理
    for k = 1:3
        % 当前通道的阴影和亮区像素
        shadow_pixels = double(img(:, :, k)) .* shadow_region;
        lit_pixels = double(img(:, :, k)) .* lit_region;
        boundary_pixels = double(img(:, :, k)) .* boundary_region;
    
        % 计算阴影区域和亮区的均值
        shadow_mean = mean(shadow_pixels(shadow_pixels > 0));
        lit_mean = mean(lit_pixels(lit_pixels > 0));
        boundary_mean = mean(boundary_pixels(boundary_pixels > 0));
    
        % 计算阴影区域和亮区的标准差
        shadow_std = std(shadow_pixels(shadow_pixels > 0));
        lit_std = std(lit_pixels(lit_pixels > 0));
        boundary_std = std(boundary_pixels(boundary_pixels > 0));
    
        % 计算通道的 alpha_k 和 gamma_k
        gamma_k = lit_std / shadow_std;
        alpha_k = lit_mean - gamma_k * shadow_mean;
    
        gamma1_k = lit_std / boundary_std;
        alpha1_k = lit_mean - gamma1_k * boundary_mean;
        
        %阴影区域
        shadow_indices = find(shadow_region - boundary_region);
        corrected_channel = corrected_img(:, :, k); 
        corrected_channel(shadow_indices) = alpha_k + gamma_k * corrected_channel(shadow_indices)+offset;
    
        % 对边界区域
        boundary_indices = find(boundary_region);
        corrected_channel(boundary_indices) = alpha1_k + gamma1_k * corrected_channel(boundary_indices);
    
        % 对 smooth_region 应用高斯模糊
        h = fspecial('gaussian', 4 * sigma - 1, sigma);
        smoooth_indice = find(smooth_region);
        
        % 对于 smooth_region 区域应用高斯模糊
        blurred_area = imfilter(corrected_channel, h, 'replicate');
        
        % 将模糊区域更新到 corrected_channel
        corrected_channel(smoooth_indice) = blurred_area(smoooth_indice);
        
        corrected_img(:, :, k) = corrected_channel;
    end
    
    % 限制像素值范围 [0, 255]
    corrected_img = uint8(min(max(corrected_img, 0), 255));

end