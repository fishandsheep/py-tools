import streamlit as st
from PIL import Image
import time

# 获取当前的会话状态
st.title("# to do ... 🐱")

image = Image.open('images/xx.jpg')

st.image(image, caption='xiang xiang')


with st.empty():
    for seconds in range(60):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write("✔️ 1 minute over!")