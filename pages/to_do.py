import streamlit as st
import pandas as pd

# 获取当前的会话状态
st.title("# to do ... 🐱")

uploaded_file = st.file_uploader("Choose a file", ['xls', 'xlsx'])
ddl_sql = ''
st.session_state.text_contents = ddl_sql
# 创建一个空白区域
selectbox_container = st.empty()
st.session_state.sheet_names = ['请选择sheet页']
st.session_state.sheet_name = selectbox_container.selectbox(
    '', st.session_state.sheet_names)
st.session_state.yl_bjg = ''

if uploaded_file is not None:
    # 读取 Excel 文件并打开为 ExcelFile 对象
    excel_file = pd.ExcelFile(uploaded_file)
    # 获取所有 sheet 页的名称列表
    st.session_state.sheet_names.extend(excel_file.sheet_names)
    selectbox_container.empty()
    st.session_state.sheet_name = selectbox_container.selectbox(
        '', st.session_state.sheet_names)
    if st.session_state.sheet_name != '请选择sheet页':
        st.session_state.yl_bjg = pd.read_excel(
            uploaded_file, st.session_state.sheet_name)
        st.write(st.session_state.yl_bjg)


left_column, right_column = st.columns(2)
ddl_button = left_column.button('生成DDL')
if ddl_button:
    bjg = st.session_state.yl_bjg
    tab_ddl = ''
    drop_table = 'DROP TABLE IF EXISTS '
    tab_name = ''
    cols_ddl = ''
    tab_comment = ''
    primaryKey = ''
    for j in range(0, len(bjg)):  # 逐行读取excel
        if (j == 0):
            tab_name = '`' + str(bjg['表名'][j]).strip() + '`'
            tab_comment = "COMMENT='" + bjg['表注释'][j] + "'"
        colName = '`' + str(bjg['字段名'][j]).strip() + '`'
        colType = bjg['字段类型'][j]
        isNull = 'NOT NULL' if str(bjg['是否可为空'][j]).strip() == 'N' else ' '
        defaultValue = 'DEFAULT ' + \
            bjg['默认值'][j] if str(bjg['默认值'][j]) != 'nan' else ''
        comment = "COMMENT '" + bjg['字段注释'][j] + "'"
        primaryKey1 = '`' + str(bjg['字段名'][j]).strip() + '`' if str(
            bjg['是否主键'][j]).strip() == 'Y' else ''
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
    st.session_state.text_contents = ddl_sql
    st.code(ddl_sql, language='sql')

right_column.download_button(
    '下载DDL', st.session_state.text_contents, st.session_state.sheet_name + '_ddl.sql')
