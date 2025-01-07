import streamlit as st
from PIL import Image
import numpy as np
import cv2
from rembg import remove

st.set_page_config(page_title="Blur the background in your photos", page_icon="📷")

def blur_background(image, blur_amount, feather_amount):
    # Usuń tło
    no_bg = remove(image)
    
    # Konwertuj obrazy na tablice numpy
    original = np.array(image)
    mask = np.array(no_bg)[:,:,3]
    
    # Rozmyj oryginalny obraz
    blurred = cv2.GaussianBlur(original, (blur_amount, blur_amount), 0)
    
    # Zastosuj wtapianie do maski
    mask = cv2.GaussianBlur(mask, (feather_amount, feather_amount), 0)
    
    # Normalizuj maskę
    mask = mask / 255.0
    
    # Połącz oryginalny obraz z rozmytym tłem używając wtopionej maski
    result = (original * mask[:,:,np.newaxis] + blurred * (1 - mask[:,:,np.newaxis])).astype(np.uint8)
    
    return Image.fromarray(result)
# Konfiguracja Streamlit
html_temp = """
    <div style="display:none">
    <meta name="description" content="Blur the background in your photos. Free online tool. No registration required.">
    </div>
"""
st.markdown(html_temp, unsafe_allow_html=True)
st.markdown("[![100pa.com](https://www.100pa.com/images/logo.png)](https://100pa.com/)")
st.title("📷 Blur the background in your photos")
st.markdown(f"<h3><font face='sans serif' color='white'>blur100.streamlit.app</font></h3>", unsafe_allow_html=True)


uploaded_file = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original photo", use_container_width=True)
    
    blur_amount = st.slider("Blur size", min_value=1, max_value=151, value=21, step=2)
    feather_amount = st.slider("Feathering amount", min_value=1, max_value=51, value=5, step=2)
    
    if st.button("Blur the background"):
        result = blur_background(image, blur_amount, feather_amount)
        st.image(result, caption="Photo with blurred background", use_container_width=True)
