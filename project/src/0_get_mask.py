import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

def list_images(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.jpg'))]

shadow_folder = '../dataset/shadow'
binary_folder = '../dataset/shadow_binary_mask/'
shadow_images = list_images(shadow_folder)

for img_path in shadow_images:
    or_img = cv2.imread(img_path)
    y_cb_cr_img = cv2.cvtColor(or_img, cv2.COLOR_BGR2YCrCb)
    binary_mask = np.copy(y_cb_cr_img)

    y_mean = np.mean(cv2.split(y_cb_cr_img)[0])
    y_std = np.std(cv2.split(y_cb_cr_img)[0])

    # classify pixels as shadow and non-shadow pixels
    for i in range(y_cb_cr_img.shape[0]):
        for j in range(y_cb_cr_img.shape[1]):
            if y_cb_cr_img[i, j, 0] < y_mean - (y_std / 3):
                # paint it white (shadow)
                binary_mask[i, j] = [255, 255, 255]
            else:
                # paint it black (non-shadow)
                binary_mask[i, j] = [0, 0, 0]
    print(img_path.split('\\')[-1])
    plt.imsave(binary_folder+img_path.split('\\')[-1],binary_mask[:,:,0],cmap='gray')