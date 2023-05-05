import streamlit as st
import pandas as pd

# 获取当前的会话状态
st.title("# to do ... 🐱")

uploaded_file = st.file_uploader("Choose a file", ['xls', 'xlsx'])
st.session_state.text_contents = ''
# 创建一个空白区域
selectbox_container = st.empty()

with selectbox_container.container():
    st.session_state.sheet_names = ['请选择主sheet']
    st.session_state.sheet_name = st.selectbox(
    '', st.session_state.sheet_names)


st.session_state.yl_bjgs = []
st.session_state.major_data= pd.DataFrame()

st.session_state.file_map = {}

if uploaded_file is not None:
    # 读取 Excel 文件并打开为 ExcelFile 对象
    excel_file = pd.ExcelFile(uploaded_file)
    # 获取所有 sheet 页的名称列表
    st.session_state.sheet_names.extend(excel_file.sheet_names)
    selectbox_container.empty()
    st.session_state.sheet_name = selectbox_container.selectbox(
        '', st.session_state.sheet_names)
    if st.session_state.sheet_name != '请选择主sheet':
        major_data = pd.read_excel(
            uploaded_file, st.session_state.sheet_name)
        # 获取主sheet页中的清单信息
        st.session_state.major_data = major_data.query('本次是否建表 =="Y"')
        st.session_state.major_data
        # 获取其他表中的全部数据
        ddl_sheet_list = list(filter(lambda x: x != st.session_state.sheet_name, excel_file.sheet_names))
        for ddl_sheet_name in ddl_sheet_list:
            st.session_state.file_map[ddl_sheet_name] = pd.read_excel(uploaded_file, ddl_sheet_name)

# 遍历可生成 DDL的 sheet
for index, row in st.session_state.major_data.iterrows():
    current_sheet = st.session_state.file_map[row['所属层级']]
    current_table = current_sheet.query('表名 == "{}"'.format(row['表名']))
    st.session_state.yl_bjgs.append(current_table)

left_column, right_column = st.columns(2)
ddl_button = left_column.button('生成DDL')
if ddl_button:
    ddl_all_sql = ''
    for table in st.session_state.yl_bjgs:
        ddl_sql = ''
        tab_ddl = ''
        drop_table = 'DROP TABLE IF EXISTS '
        tab_name = ''
        cols_ddl = ''
        tab_comment = ''
        primaryKey = ''
        for index, bjg in table.iterrows():
            tab_name = '`' + str(bjg['表名']).strip() + '`'
            tab_comment = "COMMENT='" + bjg['表注释'] + "'"
            colName = '`' + str(bjg['字段名']).strip() + '`'
            colType = bjg['字段类型']
            isNull = 'NOT NULL' if str(bjg['是否可为空']).strip() == 'N' else ' '
            defaultValue = 'DEFAULT ' + \
                bjg['默认值'] if str(bjg['默认值']) != 'nan' else ''
            comment = "COMMENT '" + str(bjg['字段注释']) + "'"
            primaryKey1 = '`' + str(bjg['字段名']).strip() + '`' if str(
                bjg['是否主键']).strip() == 'Y' else ''
            if len(primaryKey1) > 0:
                primaryKey = primaryKey + ',' + \
                    primaryKey1 if len(primaryKey) > 0 else primaryKey1
            col_ddl = colName + ' ' + colType + ' ' + isNull + \
                ' ' + defaultValue + ' ' + comment + ',\n'
            cols_ddl += col_ddl
        tab_ddl += drop_table + tab_name + ';\n' + 'CREATE TABLE ' + tab_name + \
            '(\n' + cols_ddl + 'PRIMARY KEY (' + primaryKey + ')\n' + ') ' + \
            tab_comment + ';'
        ddl_sql = ddl_sql + tab_ddl + '\n\n' if len(tab_ddl) > 0 else ddl_sql
        ddl_all_sql += ddl_sql
    st.code(ddl_all_sql, language='sql')
    st.session_state.text_contents = ddl_all_sql

right_column.download_button(
    '下载DDL', st.session_state.text_contents, st.session_state.sheet_name + '_ddl.sql')
