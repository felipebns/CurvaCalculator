# # main.py
import math
import numpy as np
import streamlit as st
import os
import atexit
from Curva import Curva

st.title('CurvaCalculator')
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    x = st.text_input(
    "x(t)",
    label_visibility='visible',
    value=None,
    disabled=False,
    key=1
    )


with col2:
    y = st.text_input(
        "y(t)",
        label_visibility='visible',
        value=None,
        disabled=False,
        key=2
    )

with col3:
    start = float(st.text_input(
        "start",
        label_visibility='visible',
        value=1,
        disabled=False,
        key=3
    ))

with col4:
    end = float(st.text_input(
        "end",
        label_visibility='visible',
        value=1,
        disabled=False,
        key=4
    ))

with col5:
    interval = float(st.text_input(
        "interval",
        label_visibility='visible',
        value=1, 
        disabled=False,
        key=5
    ))

def main(curva):
    curva.run()

#Definindo parametrização em X
def funcX(t: float) -> float:
    return eval(x)

#Definindo parametrização em Y
def funcY(t: float) -> float:
    return eval(y)

def delete_image():
    if os.path.exists('static\curva_plot.png'):
        os.remove('static\curva_plot.png')

atexit.register(delete_image)

if __name__ == '__main__':
    if x != None and y != None and start != 1 and end != 1 and interval != 1:
        curva = Curva(list_t=np.arange(start, end, interval), funcX=funcX, funcY=funcY)
        main(curva=curva)
        st.image('static\curva_plot.png', caption='Curva')
