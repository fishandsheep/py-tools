import streamlit as st
from PIL import Image
import time

# 获取当前的会话状态
st.title("# to do ... 🐱")

image = Image.open('images/xx.jpg')

st.image(image, caption='xiang xiang')


with st.empty():
    while True:
        for seconds in range(10):
            st.write(f"⏳ {10-seconds} seconds have passed")
            time.sleep(1)
            if seconds == 9:
                seconds = 0