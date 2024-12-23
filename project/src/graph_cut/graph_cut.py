from typing import Sequence, Callable, TypeAlias

import cv2
import numpy as np
import streamlit as st

def find_first_index(sequence: Sequence[float],
                     condition: Callable[[float], bool],
                     reverse: bool = False) -> float:
    index = 0
    reverse_flag = 1
    if reverse:
        reverse_flag = -1
    for value in sequence[::reverse_flag]:
        if condition(value):
            break
        else:
            index += 1
    if reverse:
        index = len(sequence) - 1 - index
    return index


@st.cache_data
def predict_from_bbox(origin_image: np.ndarray, image_data: np.ndarray,
                      graph_cut_iterations: int) -> np.ndarray:

    if len(image_data.shape) == 3:
        image_data = image_data.min(axis=2)

    if len(origin_image.shape) == 3 and origin_image.shape[-1] > 3:
        origin_image = origin_image[..., :3]

    bbox = [0, 0, 0, 0]
    bbox[0] = find_first_index(image_data.sum(axis=0), lambda value: value > 0)
    bbox[1] = find_first_index(image_data.sum(axis=1), lambda value: value > 0)
    bbox[2] = find_first_index(image_data.sum(axis=0),
                               lambda value: value > 0,
                               reverse=True)
    bbox[3] = find_first_index(image_data.sum(axis=1),
                               lambda value: value > 0,
                               reverse=True)

    mask = np.zeros(origin_image.shape[:2], np.uint8)

    # inplace 变量，供函数内部使用，别问我为什么要这么设计，鬼知道
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    cv2.grabCut(origin_image, mask, bbox, bgdModel, fgdModel,
                graph_cut_iterations, cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    mor_kernel = np.ones((5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=mor_kernel)
    masked_image = origin_image * mask[..., np.newaxis]
    return masked_image, mask


@st.cache_data
def predict_from_mask(origin_image: np.ndarray, image_data: np.ndarray,
                      graph_cut_iterations: int) -> np.ndarray:

    background_mask = image_data[..., 0]
    foreground_mask = image_data[..., 1]
    _, background_mask = cv2.threshold(background_mask, 100, 255, cv2.THRESH_BINARY)
    _, foreground_mask = cv2.threshold(foreground_mask, 100, 255, cv2.THRESH_BINARY)    

    if len(origin_image.shape) == 3 and origin_image.shape[-1] > 3:
        origin_image = origin_image[..., :3]

    mask = np.ones(origin_image.shape[:2], np.uint8) * cv2.GC_PR_BGD
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    mask[foreground_mask > 0] = cv2.GC_FGD
    mask[background_mask > 0] = cv2.GC_BGD

    cv2.grabCut(origin_image, mask, None, bgdModel, fgdModel,
                graph_cut_iterations, cv2.GC_INIT_WITH_MASK)
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    mor_kernel = np.ones((5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=mor_kernel)
    masked_image = origin_image * mask[..., np.newaxis]
    return masked_image, mask