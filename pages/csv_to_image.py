import streamlit as st
import pandas as pd
import jieba

parse_data = ''
st.session_state.text_contents = ''

uploaded_file = st.file_uploader("Choose a csv", ['csv'])
if uploaded_file is not None:
    parse_data = pd.read_csv(uploaded_file)

yl_button = st.button('转换预览')

if  yl_button:
    # 解析json对象
    contents = parse_data['content']
    for content in contents:
        seg_list = jieba.cut_for_search(content)  # 搜索引擎模式
        print(", ".join(seg_list))
    st.dataframe(parse_data)
