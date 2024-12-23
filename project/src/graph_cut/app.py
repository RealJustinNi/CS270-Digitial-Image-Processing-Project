from streamlit_drawable_canvas import st_canvas
from PIL import Image
import streamlit as st
import numpy as np

from graph_cut import predict_from_bbox, predict_from_mask

st.set_page_config(
    page_title='交互式图像分割程序',
    page_icon=' ',
    layout='wide'
)

st.sidebar.title("Graph Cut 交互式前景分割程序")

drawing_region, display_region = st.columns(spec=2)

# 感谢 andfanilo 贡献的绘画组件 streamlit_drawable_canvas
# 论坛链接： https://discuss.streamlit.io/t/drawable-canvas/3671
tagging_mode = st.sidebar.selectbox(
    "标记模式:",
    ("bbox 先验", "mask 先验"),
)

drawing_mode_mapping = {
    'bbox 先验': 'rect',
    'mask 先验': 'freedraw'
}

drawing_mode = drawing_mode_mapping[tagging_mode]

stroke_width = st.sidebar.slider("画笔宽度: ", 1, 100, 15)
if drawing_mode == "point":
    point_display_radius = st.sidebar.slider("点半径: ", 1, 25, 3)

graph_cut_iterations = st.sidebar.slider('网络流迭代次数: ', 2, 30, 5)
if drawing_mode == 'rect':
    stroke_color = '#4dc114'
else:
    stroke_color = st.sidebar.selectbox(
        "标记区域",
        ('前景', '背景')
    )
    stroke_color_mapping = {
        '前景': '#4dc114',
        '背景': '#ff4b4b'
    }
    stroke_color = stroke_color_mapping[stroke_color]

bg_image = st.sidebar.file_uploader("上传需要标记的图像: ", type=["png", "jpg"])
realtime_update = st.sidebar.checkbox("实时更新", False)

if bg_image:
    img = Image.open(bg_image)
    img_array = np.array(img)
    canvas_height, canvas_width = img_array.shape[:2]
    with drawing_region:
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color='#eee',
            background_image=img,
            update_streamlit=realtime_update,
            height=canvas_height,
            width=canvas_width,
            drawing_mode=drawing_mode,
            point_display_radius=point_display_radius
            if drawing_mode == "point" else 0,
            display_toolbar=True,
            key="full_app",
        )
    if canvas_result.image_data is not None and canvas_result.image_data.sum() > 0:
        if drawing_mode == 'rect':
            masked_image, mask = predict_from_bbox(img_array, canvas_result.image_data, graph_cut_iterations)
            display_region.image(masked_image)

        if drawing_mode == 'freedraw':
            masked_image, mask = predict_from_mask(img_array, canvas_result.image_data, graph_cut_iterations)
            display_region.image(masked_image)