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
        build_sheet(target_hits[['keep','text','Parameter','page']],'Target')
    if 'netzero_hits' in st.session_state:
        netzero_hits = st.session_state['netzero_hits']
        build_sheet(netzero_hits[['keep','text','Parameter','page']],'Netzero')
    if 'mitigation_hits' in st.session_state:
        mitigation_hits = st.session_state['mitigation_hits']
        build_sheet(mitigation_hits[['keep','text','Parameter','Type','page']],'Mitigation')
    if 'adaptation_hits' in st.session_state:
        adaptation_hits = st.session_state['adaptation_hits']
        build_sheet(adaptation_hits[['keep','text','Type','page']],'Adaptation')
        
    workbook = writer.book                                                                                                        
    writer.close()
    processed_data = output.getvalue()
    return processed_data


def filter_dataframe(key, cols):
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        key: key to look for in session_state
        cols: columns to use for filter in that order
    Returns:
        None
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return 
    if key not in st.session_state:
        return
    else:
        df = st.session_state[key]
        df = df[cols + list(set(df.columns) - set(cols))]
    if len(df)==0:
        return

    modification_container = st.container()

    with modification_container:
        temp = list(set(cols) -{'page','keep'})
        to_filter_columns = st.multiselect("Filter dataframe on", temp)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]):
                # st.write(type(df[column][0]), column)
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_list_like(df[column]) & (type(df[column][0]) == list) :
                list_vals = set(x for lst in df[column].tolist() for x in lst)
                user_multi_input = right.multiselect(
                    f"Values for {column}",
                    list_vals,
                    default=list_vals,
                )   
                df['check'] = df[column].apply(lambda x: any(i in x for i in user_multi_input))
                df = df[df.check == True]
                df.drop(columns = ['check'],inplace=True)
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.lower().str.contains(user_text_input)]
            
            df = df.reset_index(drop=True)
        df = st.data_editor(
                  df,
                  column_config={
                      "keep": st.column_config.CheckboxColumn(
                          help="Select which rows to keep",
                          default=False,
                      )
                  },
                  disabled=list(set(df.columns) - {'keep'}),
                  hide_index=True,
                  key = 'editor'+key,
                    )
    

        #("updating target hits....")
        # st.write(len(df[df.keep == True]))
        st.session_state[key] = df
        
    return