import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def list_images(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

def load_image_pairs(shadow_folder, no_shadow_folder):
    shadow_images = list_images(shadow_folder)
    no_shadow_images = list_images(no_shadow_folder)
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

        # Display the difference
        plt.figure(figsize=(12, 5))
        plt.subplot(131)
        plt.title('Shadow Image')
        plt.imshow(cv2.cvtColor(shadow_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(132)
        plt.title('No Shadow Image')
        plt.imshow(cv2.cvtColor(no_shadow_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(133)
        plt.title('Difference in Y Channel')
        plt.imshow(diff_Y, cmap='gray')
        plt.axis('off')

        plt.show()

    return np.array(diffs)

# Main execution
shadow_folder = 'path_to_shadow_images'
no_shadow_folder = 'path_to_no_shadow_images'

image_pairs = load_image_pairs(shadow_folder, no_shadow_folder)
diffs = analyze_images(image_pairs)

# Further statistical analysis on `diffs` array can be added here
average_diff = np.mean(diffs, axis=0)
plt.imshow(average_diff, cmap='gray')
plt.title('Average Y Channel Difference')
plt.axis('off')
plt.show()
