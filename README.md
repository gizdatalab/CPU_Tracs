# Climate Policy Understanding: IKI Tracs 
This is repo belongs to category of "Climate Policy Understanding", but focuses on specific use case of IKI Tracs.
It contains the front end operations of the Streamlit app deployed at [CPU IKI Tracs](https://huggingface.co/spaces/GIZ/cpu_tracs).The repo has 4 parts:
The backend operations including the pre-processing o

The tasks performed include:
1. datasets: Contains the data files of annotated data. The annotation was performed using [Argilla](https://docs.argilla.io/en/latest/)
2. notebooks: Contains the jupyter notebooks for doing the Fine-tuning of classification models. There are two kind of notebooks 1. [Setfit](https://github.com/huggingface/setfit) , which uses the Efficient Few-shot Framework from HF team.
3. root_files: [CPU IKI Tracs](https://huggingface.co/spaces/GIZ/cpu_tracs) app contains some files which are in main root directory as reuqired by Spaces on HF. These are files which provide infra related information to spaces build up.
4. appStore: This is the main code which in appStore of [CPU IKI Tracs](https://huggingface.co/spaces/GIZ/cpu_tracs), these scripts pertains each to classiifcation/processing
    tasks and perform the operations in streamlit by leveraging backend package [utils](https://github.com/gizdatalab/haystack_utils/tree/cputrac), (branch cputrac). You can use this repo in app directly also by performing pip install and importing it as package. The setup file
   includes the package information.

To install as package for streamlit app:
```
pip install -e "git+https://github.com/gizdatalab/CPU_Tracs.git@main#egg=appStore"
```
