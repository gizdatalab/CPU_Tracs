import streamlit as st
import json
import os
# shifted from below - this must be the first streamlit call; otherwise: problems
st.set_page_config(page_title = 'Climate Policy Intelligence', 
                   initial_sidebar_state='expanded', layout="wide") 

import appStore.target as tapp_extraction
import appStore.sector as sector
import appStore.adapmit as adapmit
import appStore.conditional as conditional
import appStore.subtarget as subtarget
import appStore.category as category
import appStore.iki_sheets as iki_sheets
import appStore.doc_processing as processing
import appStore.excel_convert as excel_convert
from utils.uploadAndExample import add_upload
from PIL import Image
import pkg_resources
installed_packages = pkg_resources.working_set

with st.sidebar:
    # upload and example doc
    
    choice = st.sidebar.radio(label = 'Select the Document',
                            help = 'You can upload the document \
                            or else you can try a example document', 
                            options = ('Upload Document', 'Try Example'), 
                            horizontal = True)
    with(open('docStore/sample/files.json','r')) as json_file:
            files = json.load(json_file)
    add_upload(choice, files) 

with st.container():
        st.markdown("<h2 style='text-align: center; color: black;'> Climate Policy Understanding: IKI Tracs </h2>", unsafe_allow_html=True)
        st.write(' ')

with st.expander("ℹ️ - About this app", expanded=False):
    st.write(
        """
        Climate Policy Understanding App is an open-source\
        digital tool which aims to assist policy analysts and \
        other users in extracting and filtering relevant \
        information from public documents.
        """)
    st.write('**Definitions**')

    st.caption("""
            - **Target**: Targets are an intention to achieve a specific result, \
            for example, to reduce GHG emissions to a specific level \
            (a GHG target) or increase energy efficiency or renewable \
            energy to a specific level (a non-GHG target), typically by \ 
            a certain date.
            - **Economy-wide Target**: Certain Target are applicable \
                not at specific Sector level but are applicable at economic \
                wide scale.
            - **Netzero**: Identifies if its Netzero Target or not.
                - 'NET-ZERO target_labels' = ['T_Netzero','T_Netzero_C']
            - **GHG Target**: GHG targets refer to contributions framed as targeted \
                              outcomes in GHG terms.
                - 'GHG': ['T_Transport_Unc','T_Transport_C','T_Economy_C','T_Economy_Unc','T_Energy_C','T_Energy_Unc']
                - 'NON GHG TARGET': ['T_Adaptation_Unc','T_Adaptation_C', 'T_Transport_O_Unc', 'T_Transport_O_C']
            - **Conditionality**: An “unconditional contribution” is what countries \
             could implement without any conditions and based on their own \
             resources and capabilities. A “conditional contribution” is one \
             that countries would undertake if international means of support \
             are provided, or other conditions are met.
            - **Action**: Actions are an intention to implement specific means of \
             achieving GHG reductions, usually in forms of concrete projects.
            - **Policies and Plans**: Policies are domestic planning documents \
              such as policies, regulations or guidlines, and Plans  are broader \
             than specific policies or actions, such as a general intention \ 
             to ‘improve efficiency’, ‘develop renewable energy’, etc. \
            The terms come from the World Bank's NDC platform and WRI's publication.
              """)
    c1, c2, c3 =  st.columns([12,1,10])
    with c1:
        image = Image.open('docStore/img/flow.jpg') 
        st.image(image)
    with c3:
        st.write("""
            What Happens in background?
            
            
    
            - Step 1: Once the document is provided to app, it undergoes *Pre-processing*.\
            In this step the document is broken into smaller paragraphs \
            (based on word/sentence count).
            - Step 2: The paragraphs are fed to **TAPP(Target/Action/Policy/Plan multilabel) Classifier** which detects if
            the paragraph contains any *TAPP* related information or not.
            - Step 3: The paragraphs which are detected containing some TAPP \
            related information are then fed to multiple classifier to enrich the 
            Information Extraction.
    
            """)
        
        list_ = ""
        for package in installed_packages:
            list_ = list_ + f"{package.key}=={package.version}\n"
        st.download_button('Download Requirements', list_, file_name='requirements.txt')
                  
    st.write("")
        
        
    
apps = [processing.app, tapp_extraction.app, sector.app, adapmit.app, 
        conditional.app, subtarget.app, category.app]

multiplier_val =1/len(apps)
if st.button("Analyze Document"):
    prg = st.progress(0.0)
    for i,func in enumerate(apps):
        func()
        prg.progress((i+1)*multiplier_val)
    prg.empty()

    
if 'key1' in st.session_state:
    iki_sheets.netzero()
    iki_sheets.targets()
    iki_sheets.mitigation()
    iki_sheets.adaptation()
    with st.sidebar:
        topic = st.radio(
                        "Which category you want to explore?",
                        ('Netzero', 'Targets', 'Mitigation','Adaptation'))
    
    if topic == 'Netzero':
        iki_sheets.netzero_display()
        excel_convert.filter_dataframe('netzero_hits',['keep','text','Parameter','page'])
        with st.sidebar:
                st.write('-------------')
                df_xlsx = excel_convert.to_excel()
                st.download_button(label='📥 Download Result',
                            data=df_xlsx ,
                            file_name= os.path.splitext(os.path.basename(st.session_state['filename']))[0]+'.xlsx')
    elif topic == 'Targets':
        iki_sheets.target_display()
        excel_convert.filter_dataframe('target_hits',['keep','text','Parameter','page'])
        with st.sidebar:
                st.write('-------------')
                df_xlsx = excel_convert.to_excel()
                st.download_button(label='📥 Download Result',
                            data=df_xlsx ,
                            file_name= os.path.splitext(os.path.basename(st.session_state['filename']))[0]+'.xlsx')
    elif topic == 'Mitigation':
        iki_sheets.mitigation_display()
        excel_convert.filter_dataframe('mitigation_hits',['keep','text','Parameter','Type','page'])
        with st.sidebar:
                st.write('-------------')
                df_xlsx = excel_convert.to_excel()
                st.download_button(label='📥 Download Result',
                            data=df_xlsx ,
                            file_name= os.path.splitext(os.path.basename(st.session_state['filename']))[0]+'.xlsx')
    else:
        iki_sheets.adaptation_display()
        excel_convert.filter_dataframe('adaptation_hits',['keep','text','Type','page'])
        with st.sidebar:
                st.write('-------------')
                df_xlsx = excel_convert.to_excel()
                st.download_button(label='📥 Download Result',
                            data=df_xlsx ,
                            file_name= os.path.splitext(os.path.basename(st.session_state['filename']))[0]+'.xlsx')
        #policyaction.policy_display()
    # st.write(st.session_state.key1)
