import setuptools


install_requires=[
        "streamlit==1.21.0",
        "plotly==5.19.0",
        "xlsxwriter==3.2.0",
        "streamlit-aggrid==0.3.4",
]


setuptools.setup(
        name='appstore',
        version='1.0.2',
        description='Climate Policy Understanding - IKITracs',
        author='Data Service Center GIZ',
        author_email='prashant.singh@giz.de',
        package_dir={"": "src"},
        packages=setuptools.find_packages(where='src'),  
        install_requires=install_requires, #external packages as dependencies
        )