import streamlit as st
import cv2
import numpy as np
import io

def resize_image(image, size_kb):
    # Start with a high quality factor
    quality = 90

    while True:
        # Encode image to jpg format
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', image, encode_param)

        # Check size
        if result and encimg.nbytes <= size_kb * 1024:
            break

        # If the image is still too large, decrease the quality factor
        quality -= 10
        if quality < 0:
            st.warning("Cannot compress image enough to get under the desired size. The output image may be larger than expected.")
            break

    return encimg

st.title('Image Resizer')

uploaded_files = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
size_kb = st.number_input('Enter the desired size (KB)', min_value=1)

if uploaded_files and size_kb:
    for i, uploaded_file in enumerate(uploaded_files):
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        resized_img = resize_image(img, size_kb)

        # Convert byte array back to image for displaying
        resized_img_display = cv2.imdecode(resized_img, cv2.IMREAD_COLOR)

        # Display the compressed image and its size
        st.image(resized_img_display, caption=f'Resized Image {i+1} (Size: {resized_img.nbytes / 1024:.2f} KB)')

        # Create download link
        st.download_button(
            label=f"Download resized image {i+1}",
            data=resized_img.tobytes(),
            file_name=f'resized_image_{i+1}.jpg',
            mime='image/jpeg',
            key=f'download_{i}'  # Unique key for each button
        )
