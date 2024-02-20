# set path
import glob, os, sys; 
sys.path.append('../utils')

#import needed libraries
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import logging
logger = logging.getLogger(__name__)
from utils.config import get_classifier_params
from io import BytesIO
import xlsxwriter
import plotly.express as px
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_list_like)


def to_excel():
    if 'key1' in st.session_state:
        df = st.session_state['key1']
        len_df = len(df)
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='rawdata')
    def build_sheet(df,name):
        df = df[df.keep == True]
        df = df.reset_index(drop=True)
        df.drop(columns = ['keep'], inplace=True)
        df.to_excel(writer,index=False,sheet_name = name)
        
        
    if 'target_hits' in st.session_state:
        target_hits = st.session_state['target_hits']
        build_sheet(target_hits,'Target')
    if 'netzero_hits' in st.session_state:
        netzero_hits = st.session_state['netzero_hits']
        build_sheet(netzero_hits,'Netzero')
    if 'mitigation_hits' in st.session_state:
        mitigation_hits = st.session_state['mitigation_hits']
        build_sheet(mitigation_hits,'Mitigation')
    if 'adaptation_hits' in st.session_state:
        adaptation_hits = st.session_state['adaptation_hits']
        build_sheet(adaptation_hits,'Adaptation')
        
    workbook = writer.book                                                                                                        
    writer.save()
    processed_data = output.getvalue()
    return processed_data