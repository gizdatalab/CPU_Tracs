# set path
import glob, os, sys
sys.path.append('../utils')

#import needed libraries
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from utils.adapmit_classifier import load_adapmitClassifier,adapmit_classification
# from utils.keyword_extraction import textrank
import logging
logger = logging.getLogger(__name__)
from utils.config import get_classifier_params
from utils.preprocessing import paraLengthCheck
from io import BytesIO
import xlsxwriter
import plotly.express as px

# Declare all the necessary variables
classifier_identifier = 'adapmit'
params  = get_classifier_params(classifier_identifier)


def app():
    ### Main app code ###
    with st.container():          
        if 'key1' in st.session_state:
            df = st.session_state.key1

            classifier = load_adapmitClassifier(classifier_name=params['model_name'])
            st.session_state['{}_classifier'.format(classifier_identifier)] = classifier
                    
            df = adapmit_classification(haystack_doc=df,
                                        threshold= params['threshold'])

            st.session_state.key1 = df

