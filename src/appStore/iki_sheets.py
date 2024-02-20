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
from io import BytesIO
import xlsxwriter
import plotly.express as px
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_list_like)


def netzero():
    if 'key1' in st.session_state:
        df = st.session_state['key1'].copy()
        df = df[(df.TargetLabel==True) & (df.NetzeroLabel==True)].reset_index(drop=True)
        df['Parameter'] = df.apply(lambda x: 'T_Netzero_C' if ((x['NetzeroLabel'] == True) & 
                                  (x['ConditionalLabel'] == True))
                                  else 'T_Netzero', axis=1)
        #df = df[['text','page','Parameter']]
        df['keep'] = True
        st.session_state['netzero_hits'] = df

def netzero_display():
    if 'key1' in st.session_state:
        st.caption(""" **{}** is splitted into **{}** paragraphs/text chunks."""\
                          .format(os.path.basename(st.session_state['filename']),
                                 len(st.session_state['key0'])))   
        
        hits  = st.session_state['netzero_hits']
        if len(hits) !=0:
            # collecting some statistics
            count_target = sum(hits['TargetLabel'] == True)
            count_netzero = sum(hits['NetzeroLabel'] == True)

            c1, c2 = st.columns([1,1])
            with c1:
                st.write('**NetZero Related Paragraphs**: `{}`'.format(count_netzero))
                
            st.write('----------------')
            #st.dataframe(hits[['keep','text','Parameter','page']])
        else:
            st.info("🤔 No Netzero paragraph found")
            
            
def targets():
    def check_param(x):
        temp = []
        # GHG Target
        if  all([x['Transport'],x['ConditionalLabel'],x['GHGLabel']]):
                temp.append('T_Transport_C')
        if all([x['Transport'],not x['ConditionalLabel'],x['GHGLabel']]):
                temp.append('T_Transport_Unc')
        if all([x['Economy-wide'],x['ConditionalLabel'],x['GHGLabel']]):
                temp.append('T_Economy_C')
        if all([x['Economy-wide'],not x['ConditionalLabel'],x['GHGLabel']]):
                temp.append('T_Economy_Unc')
        if all([x['Energy'],x['ConditionalLabel'],x['GHGLabel']]):
                temp.append('T_Energy_C')
        if all([x['Energy'],not x['ConditionalLabel'],x['GHGLabel']]):
                temp.append('T_Energy_Unc')
            
        # NonGHG Target    
        if all([x['Transport'],x['ConditionalLabel'],x['NonGHGLabel'],x['MitigationLabel']]):
                temp.append('T_Transport_O_C')
        if all([x['Transport'],not x['ConditionalLabel'],x['NonGHGLabel'],x['MitigationLabel']]):
                temp.append('T_Transport_O_Unc')
        if all([x['Economy-wide'],x['ConditionalLabel'],x['NonGHGLabel'],x['MitigationLabel']]):
                temp.append('T_Economy_O_C')
        if all([x['Economy-wide'],not x['ConditionalLabel'],x['NonGHGLabel'],x['MitigationLabel']]):
                temp.append('T_Economy_O_Unc')
        if all([x['Energy'],x['ConditionalLabel'],x['NonGHGLabel'],x['MitigationLabel']]):
                temp.append('T_Energy_O_C')
        if all([x['Energy'],not x['ConditionalLabel'],x['NonGHGLabel'],x['MitigationLabel']]):
                temp.append('T_Energy_O_Unc')

        # Adaptation Target    
        if all([x['ConditionalLabel'],x['NonGHGLabel'],x['AdaptationLabel']]):
                temp.append('T_Adaptation_C')
        if all([not x['ConditionalLabel'],x['NonGHGLabel'],x['AdaptationLabel']]):
                temp.append('T_Adaptation_Unc')

        return temp
    
    if 'key1' in st.session_state:
        df = st.session_state['key1'].copy()
        df = df[df.TargetLabel==True].reset_index(drop=True)
        df['Parameter'] = df.apply(lambda x: check_param(x), axis=1)
        #df = df[['text','page','Parameter']]
        df['keep'] = True
        st.session_state['target_hits'] = df
    
def target_display():
    if 'key1' in st.session_state:
        st.caption(""" **{}** is splitted into **{}** paragraphs/text chunks."""\
                          .format(os.path.basename(st.session_state['filename']),
                                 len(st.session_state['key0'])))   
        
        hits  = st.session_state['target_hits']
        if len(hits) !=0:
            # collecting some statistics
            count_target = sum(hits['TargetLabel'] == True)
            count_ghg = sum(hits['GHGLabel'] == True)
            count_transport = sum(hits['Transport'] == True)
            count_nonghg = sum(hits['NonGHGLabel'] == True)

            c1, c2 = st.columns([1,1])
            with c1:
                st.write('**Target Related Paragraphs**: `{}`'.format(count_target))
                st.write('**Transport Target Related Paragraphs**: `{}`'.format(count_transport))
            with c2:
                st.write('**GHG Target Related Paragraphs**: `{}`'.format(count_ghg))
                st.write('**NonGHG Target Related Paragraphs**: `{}`'.format(count_nonghg))
            st.write('----------------')
            #st.dataframe(hits[['keep','text','Parameter','page']])
        else:
            st.info("🤔 No Targets Found")

def mitigation():
    if 'key1' in st.session_state:
        df = st.session_state['key1'].copy()
        temp = np.where((df.ActionLabel==True) | (df.PolicyLabel==True) | (df.PlansLabel==True))
        df = df.loc[temp]
        df = df.reset_index(drop=True)
        df = df[(df.MitigationLabel == True)&(df.Transport == True)].reset_index(drop=True)
        categories = ['Active mobility','Alternative fuels','Aviation improvements',
              'Comprehensive transport planning','Digital solutions','Economic instruments',
              'Education and behavioral change','Electric mobility',
              'Freight efficiency improvements','Improve infrastructure','Land use',
              'Other Transport Category','Public transport improvement',
              'Shipping improvements','Transport demand management','Vehicle improvements']
        df['Parameter'] = df.apply(lambda x: [i for i in categories if x[i]==True],axis=1)
        non_target = ['Action','Policy','Plans'] 
        df['Type'] = df.apply(lambda x: [i for i in non_target if x[i+'Label']==True],axis=1)
        df['keep'] = True
        st.session_state['mitigation_hits'] = df

def mitigation_display():
    if 'key1' in st.session_state:
        st.caption(""" **{}** is splitted into **{}** paragraphs/text chunks."""\
                          .format(os.path.basename(st.session_state['filename']),
                                 len(st.session_state['key0'])))   
        
        hits  = st.session_state['mitigation_hits']
        if len(hits) !=0:
            # collecting some statistics
            count_mitigation = sum(hits['MitigationLabel'] == True)
            count_action = sum(hits['ActionLabel'] == True)
            count_policy = sum(hits['PolicyLabel'] == True)
            count_plans = sum(hits['PlansLabel'] == True)

            c1, c2 = st.columns([1,1])
            with c1:
                st.write('**Transport Mitgation Related Paragraphs**: `{}`'.format(count_mitigation))
                st.write('**Transport Action Related Paragraphs**: `{}`'.format(count_action))
            with c2:
                st.write('**Transport Policy Related Paragraphs**: `{}`'.format(count_policy))
                st.write('**Transport Plans Related Paragraphs**: `{}`'.format(count_plans))
            st.write('----------------')
            #st.dataframe(hits[['keep','text','Parameter','Type','page']])
        else:
            st.info("🤔 No Tranport  Mitigation paragraph found")


def adaptation():
    if 'key1' in st.session_state:
        df = st.session_state['key1'].copy()
        temp = np.where((df.ActionLabel==True) | (df.PolicyLabel==True) | (df.PlansLabel==True))
        df = df.loc[temp]
        df = df.reset_index(drop=True)
        df = df[(df.AdaptationLabel == True)&(df.Transport == True)].reset_index(drop=True)
        non_target = ['Action','Policy','Plans'] 
        df['Type'] = df.apply(lambda x: [i for i in non_target if x[i+'Label']==True],axis=1)
        df['keep'] = True
        st.session_state['adaptation_hits'] = df

def adaptation_display():
    if 'key1' in st.session_state:
        st.caption(""" **{}** is splitted into **{}** paragraphs/text chunks."""\
                          .format(os.path.basename(st.session_state['filename']),
                                 len(st.session_state['key0'])))   
        
        hits  = st.session_state['adaptation_hits']
        if len(hits) !=0:
            # collecting some statistics
            count_adaptation = sum(hits['AdaptationLabel'] == True)
            count_action = sum(hits['ActionLabel'] == True)
            count_policy = sum(hits['PolicyLabel'] == True)
            count_plans = sum(hits['PlansLabel'] == True)

            c1, c2 = st.columns([1,1])
            with c1:
                st.write('**Transport Adaptation Related Paragraphs**: `{}`'.format(count_adaptation))
                st.write('**Transport Action Related Paragraphs**: `{}`'.format(count_action))
            with c2:
                st.write('**Transport Policy Related Paragraphs**: `{}`'.format(count_policy))
                st.write('**Transport Plans Related Paragraphs**: `{}`'.format(count_plans))
            st.write('----------------')
            #st.dataframe(hits[['keep','text','Type','page']])
        else:
            st.info("🤔 No Tranport  Adaptation paragraph found")
    