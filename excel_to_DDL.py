import streamlit as st
import time
import pandas as pd

st.title("excel to DDL :sunglasses:")

ddl_sql = ''
# excel_path = st.text_input(
#    '请输入excel路径:', key='excel_path', value='D:\\风险模型表单设计.xlsx')
st.session_state.text_contents = ''
uploaded_file = st.file_uploader("Choose a file", ['xls', 'xlsx'])
# ddl_path = st.text_input('请输入ddl文件生成路径:', key='ddl_path', value='D:\\数据文档\\') + \
#     '土增风险加工表结构'+str(time.strftime("%Y%m%d", time.localtime()))+'.sql'
sheet_name = st.text_input('请输入读取的起始sheet名:', key='sheet_name', value='收入明细表')
sheet_startnumber = st.number_input(
    '请输入读取的起始sheet序号:', key='sheet_startnumber', value=1)
sheet_number = st.number_input('请输入读取的sheet个数:', key='sheet_number', value=2)

yl_button = st.button('预览')
ddl_button = st.button('批量生成DDL')

if yl_button:
    yl_bjg = pd.read_excel(uploaded_file, sheet_name=sheet_name, dtype=object)
    # yl_bjg.columns
    st.dataframe(yl_bjg)
    #print(excel_path)
# st.write(excel_path)

if ddl_button:
    bjg_list = pd.read_excel(uploaded_file, sheet_name=None, dtype=object)
    for i, (name, bjg) in enumerate(bjg_list.items()):
        tab_ddl = ''
        if (i >= sheet_startnumber and i < sheet_startnumber+sheet_number):
            drop_table = 'DROP TABLE IF EXISTS '
            tab_ddl = ''
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
                isNull = 'NOT NULL' if str(
                    bjg['是否可为空'][j]).strip() == 'N' else ' '
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
                '(\n' + cols_ddl + 'PRIMARY KEY (' + \
                primaryKey + ')\n' + ') ' + tab_comment + ';'
        ddl_sql = ddl_sql + tab_ddl + '\n\n' if len(tab_ddl) > 0 else ddl_sql
    st.code(ddl_sql, language='sql')
    st.session_state.text_contents = ddl_sql
    # f = open(ddl_path, 'w')
    # f.truncate(0)
    # f.write(ddl_sql)
    # f.close()

st.download_button(
    '下载DDL', st.session_state.text_contents, 'demo' + '_ddl.sql')