import streamlit as st
import json

def flatten_objects_recursive(data):
    flattened_objects = []

    # 遍历每个对象
    for obj in data:
        # 将当前对象添加到平铺列表中
        flattened_objects.append(obj)

        # 如果当前对象的 items 属性不为空，则递归平铺 items 中的对象
        if obj["items"]:
            flattened_objects.extend(flatten_objects_recursive(obj["items"]))

        # 清空当前对象的 items 属性，以防止重复添加
        obj["items"] = []

    return flattened_objects

# st.title("json to excel :sunglasses:")

parse_data = ''
st.session_state.text_contents = ''

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    parse_data = flatten_objects_recursive(json.load(uploaded_file))

yl_button = st.button('转换预览')

if  yl_button:
    # 解析json对象
    st.dataframe(parse_data)