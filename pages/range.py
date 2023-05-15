import streamlit as st
import requests
import json


st.header('浪姐4投票排行👩‍🎤')
st.caption('实时更新')

st.session_state.data = {}

url = "https://vipact.api.mgtv.com/api/v1/act/vote/charlist?act_name=20230414cf2023&count=33"
response = requests.get(url)
st.session_state.data = json.loads(response.text)   

character_list = st.session_state.data['data']['character_list']

other_vote_num = 0
mr_vote_num = 0
for item in character_list:
    if item['char_name'] != '美依礼芽':
        other_vote_num += item['vote_num']
    else:
        mr_vote_num = item['vote_num']



st.vega_lite_chart(character_list, {
    'width':700,
    'mark': {'type': 'bar', 'tooltip': True},
    'encoding': {
        "y": {"field": "char_name","sort":'-x'},
        "x": {"field": "vote_num", "type": "quantitative", "title": "投票总数"},
    }
})



# [{'char_name':'美依礼芽','vote_num':mr_vote_num},
#                     {'char_name':'others','vote_num':other_vote_num}]

st.vega_lite_chart([{'char_name':'美依礼芽','vote_num':mr_vote_num},
                     {'char_name':'others','vote_num':other_vote_num}], {
    "layer": [{'mark': "arc"}],
    'encoding': {
        "theta": {"field": "vote_num", "type": "quantitative"},
        "color": {"field": "char_name", "type": "nominal"}
    }
})

# mr_vote_num/(mr_vote_num+other_vote_num)
rounded_num = round((mr_vote_num/(mr_vote_num+other_vote_num))*100, 2)
st.markdown("### MARiA/ALL:{}%".format(rounded_num))


# st.vega_lite_chart(character_list, {
#     'mark': {'type': 'bar', 'tooltip': True},
#     'encoding': {
#         "x": {"field": "char_name","sort":'-y',"title": "粉丝数"},
#         "y": {"field": "fans_num", "type": "quantitative"},
#     },
# })

# st.vega_lite_chart(character_list, {
#     'mark': {'type': 'bar', 'tooltip': True},
#     'encoding': {
#         "x": {"field": "char_name","sort":'-y',"title": "投票总数/粉丝数"},
#         "y": {"field": "avg", "type": "quantitative"},
#     },
# })

