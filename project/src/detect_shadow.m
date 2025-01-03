function shadow_mask = detect_shadow(img,ratio)
    y_cb_cr_img = rgb2ycbcr(img);
    y_channel = y_cb_cr_img(:, :, 1); 
    y_mean = mean(y_channel(:));
    y_std = std(double(y_channel(:)));
    threshold = y_mean - (y_std / ratio);
    shadow_mask = y_channel < threshold;
    % 显示初始mask
    %figure;
    %imshow(shadow_mask, []);
    %title("Shadow Mask After Threshholding");
end