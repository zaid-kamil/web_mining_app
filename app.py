import streamlit as st
import pandas as pd
from miner import data_miner_1, data_miner_2, save_data
import os

st.set_page_config(page_title='Data Mining and Web Scraping App', page_icon='📊', layout='wide',)

st.title('Data Mining and Web Scraping App')

st.sidebar.title('Navigation')

nav = st.sidebar.radio('Go to', ('Home', 'Collected Datasets', 'Data Mining', 'About'))

if nav == 'Home':
    # what is data mining
    st.header('What is Data Mining?')
    st.markdown('''
        data mining is the process of discovering patterns in large data sets involving methods at the 
        intersection of machine learning, statistics, and database systems. Data mining is an 
        interdisciplinary subfield of computer science and statistics with an overall goal 
        to extract information (with intelligent methods) from a data set and transform the 
        information into a comprehensible structure for further use. Data mining is the analysis 
        step of the "knowledge discovery in databases" process, or KDD. Aside from the raw analysis 
        step, it also involves database and data management aspects, data pre-processing, model and 
        inference considerations, interestingness metrics, complexity considerations, post-processing 
        of discovered structures, visualization, and online updating. The difference between data 
        analysis and data mining is that data analysis is used to test models and hypotheses 
        on the dataset, e.g., analyzing the effectiveness of a marketing campaign, regardless of 
        the amount of data; in contrast, data mining uses machine-learning and statistical models 
        to uncover clandestine or hidden patterns in a large volume of data.
    ''')

    # what is web scraping
    st.header('What is Web Scraping?')
    st.markdown('''
        Web scraping, web harvesting, or web data extraction is data scraping used for extracting
        data from websites. Web scraping software may access the World Wide Web directly using the
        Hypertext Transfer Protocol, or through a web browser. While web scraping can be done manually
        by a software user, the term typically refers to automated processes implemented using a bot
        or web crawler. It is a form of copying, in which specific data is gathered and copied from
        the web, typically into a central local database or spreadsheet, for later retrieval or analysis.
    ''')

    # about dputils library
    st.header('About dputils library')
    st.markdown('''
        dputils is a python library for data mining and web scraping. It is built on top of
        [requests](https://docs.python-requests.org/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
        It is a simple library that makes web scraping and data mining easy for everyone.
        The library is open source and can be found on [github](https://github.com/digipodium/dputils) and [pypi](https://pypi.org/project/dputils/).
    ''')

elif nav == 'Collected Datasets':
    st.header('Collected Datasets')
    st.markdown('''
        Here are some datasets collected using this app. You can also download the datasets
        and use them for your own projects.
    ''')
    path = 'datasets'
    files = os.listdir(path)
    files = [file for file in files if file.endswith('.csv')]
    if len(files) == 0:
        st.markdown('''
            No datasets found. Please run the data mining app to collect some data.
        ''')
    else:
        st.markdown('''
            ## Download datasets
        ''')
        selected_file = st.selectbox('Select dataset', files)
        df = pd.read_csv(f'datasets/{selected_file}')
        try:df['rating'] = df['rating'].astype(float)
        except:pass
        st.sidebar.subheader('Dataset info')
        st.sidebar.write(df.dtypes)
        st.dataframe(df, column_config={
            'image_url': st.column_config.ImageColumn("Product Image", width="large"),
        },use_container_width=True)
        st.sidebar.subheader('Download datasets')
        for file in files:
            with open(f'datasets/{file}', 'rb') as f:
                data = f.read()
            st.sidebar.download_button(file, data, file)
elif nav == 'Data Mining':
    data_path = None
    st.header('Data Mining')
    st.markdown('''
        Here you can collect data from flipkart.com. You can collect data from any category
        and any page. The data will be saved in a csv file in the datasets folder.
    ''')
    st.sidebar.markdown('''
        ## Miner 1
        This miner collects data from the rows wise results of the search page for phones, laptops, etc. 
                
        ## Miner 2
        This miner collects data from the grid wise results of the search page for bags, shoes, etc.
    ''')
    col1, col2 = st.columns([5,2])
    query = col1.text_input('Enter search query', 'phone')
    page = col2.number_input('Starting page number', 1, 100, 1)

    col1, col2 = st.columns(2)
    if col1.button('Try Miner 1 (rows)', type='primary',use_container_width=True):
        with st.spinner('Mining data...'):
            collection = []
            while True:
                page_data = data_miner_1(query, page)
                if len(page_data) == 0:
                    break
                st.sidebar.write(f'Page {page} data collected')
                collection.extend(page_data)    
                page += 1
            data_path = save_data(collection, query)
            st.sidebar.success('Data saved successfully')

    
    if col2.button('Try Miner 2 (grid)', type='secondary',use_container_width=True ):
        with st.spinner('Mining data...'):
            data = data_miner_2(query, page)
            data_path = save_data(data, query)
            st.sidebar.success('Data saved successfully')

    if data_path:
        st.markdown('''
            ## Data
        ''')
        
        st.dataframe(pd.read_csv(data_path), column_config={
            'image_url': st.column_config.ImageColumn("Product Image", width="large"),
        }, use_container_width=True)

elif nav == 'About':
    st.header('About')
    st.markdown('''

''')