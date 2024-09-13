from PIL import Image
import numpy as np
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def cloud(image, parse_data, max_word, max_font, random):
    stopwords = set(STOPWORDS)
    stopwords.update([])
    
    # create coloring from image
    image_colors = ImageColorGenerator(image)

    wc = WordCloud(font_path='/root/py-tools/images/SIMSUN.TTC',background_color="white", max_words=max_word, mask=image,
    stopwords=stopwords, max_font_size=max_font, random_state=random)

    # generate word cloud
    contents = parse_data['content']
    word_str = ''
    for content in contents:
        seg_list = jieba.cut_for_search(content) # 搜索引擎模式
        word_str += " ".join(seg_list)  
    wc.generate(word_str)

   

    # show the figure
    plt.figure(figsize=(100,100))
    fig, axes = plt.subplots(1,2, gridspec_kw={'width_ratios': [3, 2]})
    axes[0].imshow(wc, interpolation="bilinear")
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    axes[1].imshow(image, cmap=plt.cm.gray, interpolation="bilinear")

    for ax in axes:
        ax.set_axis_off()
    st.pyplot(fig)

def main():
    st.write("# CSV file to WordCloud Image")
    max_word = st.sidebar.slider("Max words", 200, 3000, 200)
    max_font = st.sidebar.slider("Max Font Size", 50, 350, 60)
    random = st.sidebar.slider("Random State", 30, 100, 42 )

    uploaded_file = st.file_uploader("Choose a csv file", ['csv'])
    image = st.file_uploader("Choose a image file", ['png','jpg','svg'])
   
       
    if image and uploaded_file is not None:
        if st.button("Plot"):
            st.write("### Original image")
            image = np.array(Image.open(image))
            parse_data = pd.read_csv(uploaded_file)
            # st.image(image, width=100, use_column_width=True)
            st.write("### Word cloud")
            st.write(cloud(image, parse_data, max_word, max_font, random), use_column_width=True)

if __name__=="__main__":
  main()