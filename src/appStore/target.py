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
from utils.tapp_classifier import load_tappClassifier,load_targetClassifier, tapp_classification 
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

# Declare all the necessary variables
tapp_classifier_identifier = 'tapp'
target_setfit = 'target'
param1  = get_classifier_params(tapp_classifier_identifier)
param2  = get_classifier_params(target_setfit)

def app():
    ### Main app code ###
    with st.container():
        if 'key0' in st.session_state:
            df = st.session_state.key0

            #load Classifiers
            classifier = load_tappClassifier(classifier_name=param1['model_name'])
            st.session_state['{}_classifier'.format(tapp_classifier_identifier)] = classifier
            classifier = load_targetClassifier(classifier_name=param2['model_name'])
            st.session_state['{}_classifier'.format(target_setfit)] = classifier
            
            if len(df) > 100:
                warning_msg = ": This might take sometime, please sit back and relax."
            else:
                warning_msg = ""
                
            df  = tapp_classification(haystack_doc=df,
                                    threshold= param1['threshold'])

            st.session_state.key1 = df

