import streamlit as st
import pandas as pd
from sudoku import Sudoku

# 获取当前的会话状态
st.title("# sudoku 🐱")

uploaded_file = st.file_uploader("Choose a file", ['xls', 'xlsx'])

board = []

parse_button = st.button('求解')

left_column, right_column = st.columns(2)

if uploaded_file:
    # 获取所有 sheet 页的名称列表
    major_data = pd.read_excel(uploaded_file)
    for index, row in major_data.iterrows():
        board.append(row.values)

    puzzle = Sudoku(3, 3, board=board)
    left_column.code(str(puzzle))

if parse_button and board:
    solution = puzzle.solve()
    right_column.code(str(solution))