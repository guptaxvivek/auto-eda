import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def get_cat_cols():
    cat_col = []
    for col in data.columns.tolist():
        if data[col].nunique() < 10:
            cat_col.append(col)
    return cat_col


with st.sidebar:
    st.title("DATA Visualizer")
    try:
        data = pd.read_csv(st.file_uploader(label="Upload CSV file", type='csv'))
    except ValueError:
        pass
    show = st.selectbox("What to Show", ['DataFrame', 'Column Analysis', "Visualization"])


try:
    cat_cols = get_cat_cols()
    numeric = data.select_dtypes(include=['int', 'float']).columns.tolist()
    num_cols = [x for x in numeric if x not in cat_cols]
except NameError:
    pass

if show == 'DataFrame':
    st.header("Your DataFrame")
    try:
        st.dataframe(data)

        null_val = data.isna().sum().sum()
        rows = data.shape[0]
        null_p = null_val/rows
        st.subheader(f"NULL Values: {null_val} ({null_p*100:.2f}%)")
        st.progress(null_p)

        dup_val = data.duplicated().sum().sum()
        dup_p = dup_val / rows
        st.subheader(f"Duplicated Rows: {dup_val} ({dup_p*100:.2f}%)")
        st.progress(dup_p)

    except NameError:
        st.write("Please Upload a csv file to proceed..")


elif show == 'Column Analysis':
    st.header("Column Analysis")
    sel_col = st.selectbox("Choose column", data.columns.tolist())

    null_val = data[sel_col].isna().sum().sum()
    null_p = null_val/data[sel_col].shape[0]
    st.subheader(f"Null Values: {null_val}  ({null_p*100:.2f}%)")
    st.progress(null_p)

    dup_val = data[sel_col].duplicated().sum()
    dup_p = dup_val/data[sel_col].shape[0]
    st.subheader(f"Duplicated Values: {dup_val} ({dup_p*100:.2f}%)")
    st.progress(dup_p)

    if sel_col in num_cols:
        st.subheader("Descriptive Stats")
        st.write(f"Average: {data[sel_col].mean()}")
        st.write(f"Min: {data[sel_col].min()}")
        st.write(f"Max: {data[sel_col].max()}")

        st.subheader("Histogram")
        fig = plt.figure(figsize=(10, 4))
        sns.histplot(data[sel_col], kde=True)
        st.pyplot(fig)

        st.subheader("BoxPlot")
        fig = plt.figure(figsize=(10, 4))
        sns.boxplot(data[sel_col])
        st.pyplot(fig)

    elif sel_col in cat_cols:
        distinct = data[sel_col].nunique()
        distinct_p = distinct/data[sel_col].shape[0]
        st.subheader(f"Distinct Values: {data[sel_col].nunique()} ({distinct_p*100:.2f}%)")
        st.progress(distinct_p)

        st.subheader("CountPlot")
        fig = plt.figure(figsize=(10, 4))
        sns.countplot(data[sel_col])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.subheader("PieChart")
        fig = plt.figure(figsize=(10, 4))
        data[sel_col].value_counts().plot(kind='pie', autopct='%.1f')
        st.pyplot(fig)


elif show == "Visualization":
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
        sns.scatterplot(x=data[col1], y=data[col2], hue=data[col3], palette='mako',alpha=0.8)
        st.pyplot(fig)