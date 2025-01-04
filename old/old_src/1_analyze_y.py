import cv2
import numpy as np
import os
import re
import matplotlib.pyplot as plt

def list_images(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.jpg'))]

def load_image_pairs(shadow_folder, no_shadow_folder):
    shadow_images = list_images(shadow_folder)
    no_shadow_images = list_images(no_shadow_folder)
    #print(len(shadow_images),len(no_shadow_images))
    assert len(shadow_images) == len(no_shadow_images), "Folders must contain the same number of images."
    return zip(shadow_images, no_shadow_images)

def convert_to_ycbcr(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

def analyze_images(image_pairs):
    diffs = []
    for shadow_image_path, no_shadow_image_path in image_pairs:
        shadow_image = cv2.imread(shadow_image_path)
        no_shadow_image = cv2.imread(no_shadow_image_path)

        shadow_ycbcr = convert_to_ycbcr(shadow_image)
        no_shadow_ycbcr = convert_to_ycbcr(no_shadow_image)

        shadow_Y = shadow_ycbcr[:, :, 0]
        no_shadow_Y = no_shadow_ycbcr[:, :, 0]

        diff_Y = cv2.absdiff(shadow_Y, no_shadow_Y)
        diffs.append(diff_Y)

        theshold = 20
        mean_diff = np.mean(shadow_Y[shadow_Y < no_shadow_Y - theshold])
        std_diff  = np.std(shadow_Y[shadow_Y < no_shadow_Y - theshold])

        mean_shadow = np.mean(shadow_Y)
        std_shadow = np.std(shadow_Y)

        y_mask = np.copy(shadow_Y)
        y_mask[shadow_Y < no_shadow_Y - theshold] = 255
        y_mask[shadow_Y >= no_shadow_Y - theshold] = 0

        img_name = shadow_image_path.split("\\")[-1]
        # Display the difference
        plt.figure(figsize=(12, 5))
        plt.subplot(241)
        plt.title(f"Shadow Image mean:{mean_shadow:.3f} std:{std_shadow:.3f}")
        plt.imshow(cv2.cvtColor(shadow_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(242)
        plt.title(f'{img_name}')
        plt.imshow(cv2.cvtColor(no_shadow_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(243)
        plt.title(f"Diff Image mean:{mean_diff:.3f} std:{std_diff:.3f}")
        plt.imshow(diff_Y, cmap='gray')
        plt.axis('off')

        plt.subplot(244)
        plt.title(f"diff hist")
        plt.hist(x=diff_Y.flatten(),bins=50)

        plt.subplot(245)
        plt.imshow(shadow_Y,cmap='gray')
        plt.axis('off')

        plt.subplot(246)
        plt.imshow(no_shadow_Y,cmap='gray')
        plt.axis('off')

        plt.subplot(247)
        plt.imshow(y_mask,cmap='gray')
        plt.axis('off')

        plt.show()

    return diffs

shadow_folder = '../dataset/shadow'
no_shadow_folder = '../dataset/shadow_free'

image_pairs = load_image_pairs(shadow_folder, no_shadow_folder)
diffs = analyze_images(image_pairs)