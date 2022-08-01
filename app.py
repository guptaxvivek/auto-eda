import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def get_cat_cols():
    cat_col = []
    for col in data.columns.tolist():
        if data[col].nunique() < 15:
            cat_col.append(col)
    return cat_col


with st.sidebar:
    st.title("DATA Visualizer")
    data = pd.read_csv(st.file_uploader(label="Upload CSV file", type='csv'))
    show = st.selectbox("What to Show", ['DataFrame', "Single column plot", "Multiple column plot"])
    cat_cols = get_cat_cols()
    numeric = data.select_dtypes(include=['int', 'float']).columns.tolist()
    num_cols = [x for x in numeric if x not in cat_cols]

if show == 'DataFrame':
    st.header("Your DataFrame")
    st.dataframe(data)

elif show == "Single column plot":
    st.header("Single column plot")
    plot = st.selectbox("Plot Type", ['Countplot', 'PieChart', 'Histogram', 'Boxplot'])
    if plot == 'Countplot':
        col = st.selectbox('Select Column', cat_cols)
        fig = plt.figure(figsize=(10, 4))
        sns.countplot(data[col])
        plt.xticks(rotation=90)
        st.pyplot(fig)

    elif plot == 'PieChart':
        col = st.selectbox('Select Column', cat_cols)
        fig = plt.figure(figsize=(10, 4))
        data[col].value_counts().plot(kind='pie', autopct='%.1f')
        st.pyplot(fig)

    elif plot == 'Histogram':
        num_col = st.selectbox('Select Column', num_cols)
        fig = plt.figure(figsize=(10, 4))
        sns.histplot(data[num_col], kde=True)
        st.pyplot(fig)

    elif plot == 'Boxplot':
        num_col = st.selectbox('Select Column', num_cols)
        fig = plt.figure(figsize=(10, 4))
        sns.boxplot(data[num_col])
        st.pyplot(fig)



elif show == "Multiple column plot":
    st.header("Multiple column plot")

    type = st.selectbox("Chart Type", ['bar', 'scatter', 'line', 'boxplot', 'regressionplot', 'heatmap', 'pairplot',
                                       'scatterplot with hue'])
    c1, c2 = st.columns(2)
    if type == 'bar':
        with c1:
            col1 = st.selectbox('Select Column X', cat_cols)
        with c2:
            col2 = st.selectbox('Select Column Y', num_cols)
        fig = plt.figure(figsize=(10, 4))
        plt.xticks(rotation=90)
        sns.barplot(x=data[col1], y=data[col2])
        st.pyplot(fig)

    elif type == 'scatter':
        with c1:
            col1 = st.selectbox('Select Column X', num_cols)
        with c2:
            col2 = st.selectbox('Select Column Y', num_cols)
        fig = plt.figure(figsize=(10, 4))
        sns.scatterplot(x=data[col1], y=data[col2])
        st.pyplot(fig)

    elif type == 'line':
        with c1:
            col1 = st.selectbox('Select Column X', num_cols)
        with c2:
            col2 = st.selectbox('Select Column Y', num_cols)
        fig = plt.figure(figsize=(10, 4))
        sns.lineplot(x=data[col1], y=data[col2])
        st.pyplot(fig)

    elif type == 'boxplot':
        with c1:
            col1 = st.selectbox('Select Column X', cat_cols)
        with c2:
            col2 = st.selectbox('Select Column Y', num_cols)
        fig = plt.figure(figsize=(10, 4))
        plt.xticks(rotation=90)
        sns.boxplot(x=data[col1], y=data[col2])
        st.pyplot(fig)

    elif type == 'regressionplot':
        with c1:
            col1 = st.selectbox('Select Column X', num_cols)
        with c2:
            col2 = st.selectbox('Select Column Y', num_cols)
        fig = plt.figure(figsize=(10, 4))
        sns.regplot(x=data[col1], y=data[col2])
        st.pyplot(fig)

    elif type == 'heatmap':
        corr_df = data.corr()
        fig = plt.figure(figsize=(10, 4))
        sns.heatmap(corr_df)
        st.pyplot(fig)

    elif type == 'pairplot':
        fig = sns.pairplot(data)
        st.pyplot(fig)

    elif type == 'scatterplot with hue':
        s1, s2, s3 = st.columns(3)
        with s1:
            col1 = st.selectbox('Select Column X', num_cols)
        with s2:
            col2 = st.selectbox('Select Column Y', num_cols)
        with s3:
            col3 = st.selectbox('Hue Column', cat_cols)
        fig = plt.figure(figsize=(10, 4))
        sns.scatterplot(x=data[col1], y=data[col2], hue=data[col3], palette='mako', alpha=0.5)
        st.pyplot(fig)
