# set path
import glob, os, sys; 
sys.path.append('../utils')

#import needed libraries
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from utils.conditional_classifier import load_conditionalClassifier, conditional_classification
import logging
logger = logging.getLogger(__name__)
from utils.config import get_classifier_params
from io import BytesIO
import xlsxwriter
import plotly.express as px


# Declare all the necessary variables
classifier_identifier = 'conditional'
params  = get_classifier_params(classifier_identifier)


def app():
    ### Main app code ###
    with st.container():
        if 'key1' in st.session_state:
            df = st.session_state.key1

            # Load the classifier model
            classifier = load_conditionalClassifier(classifier_name=params['model_name'])
            st.session_state['{}_classifier'.format(classifier_identifier)] = classifier
            
            df = conditional_classification(haystack_doc=df,
                                        threshold= params['threshold'])
            st.session_state.key1 = df

