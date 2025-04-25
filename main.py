import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Exploratory Data Analysis App")
file = st.file_uploader("upload yor csv file for analysis", type=['csv'])

if file is not None:
    data = pd.read_csv(file)

    st.subheader("Data is successfully uploaded")
    st.dataframe(data.head())

    st.subheader("Dataset Information")
    st.text(f"Shape of the dataset: {data.shape[0]} rows, {data.shape[1]} columns")

    st.markdown("***Column names and data types:***")
    st.write(data.dtypes)

    st.text("Missing values in each columns")
    st.write(data.isnull().sum())

    if st.checkbox("Show statistical summary"):

        st.subheader("Statistical Summary")

        selected_columns = st.multiselect("Select columns to display summary",
                                          data.columns.tolist(),
                                          default=data.select_dtypes(include='number').columns.tolist())
        if selected_columns:
            st.write(data[selected_columns].describe())
        else:
            st.write("No columns selected")

    if st.checkbox("Show Visualizations"):
        st.subheader("Data Visualization")

        st.markdown("### Univariate Analysis")
        column = st.selectbox("Select a column for univariate analysis:", data.columns.tolist())
        plot_type = st.radio("Select plot type:", ["Histogram", "Box Plot", "Count Plot"])

        if plot_type == "Histogram":
            st.bar_chart(data[column])
        elif plot_type == "Box Plot":
            fig, ax = plt.subplots()
            st.write(sns.boxplot(data=data, x=column, ax=ax))
            st.pyplot(fig)
        elif plot_type == "Count Plot":
            fig, ax = plt.subplots()
            st.write(sns.countplot(data=data, x=column, ax=ax))
            st.pyplot(fig)

        st.markdown("### Bivariate Analysis")
        cols = st.multiselect("Select columns for scatter plot (choose 2):",
                              data.columns.tolist())

        if len(cols) == 2:
            fig, ax = plt.subplots()
            st.write(sns.scatterplot(data=data, x=cols[0], y=cols[1], ax=ax))
            st.pyplot(fig)
    if st.checkbox("Show Relationships Between Columns"):
        st.subheader("Column Relationships")

        numeric_data = data.select_dtypes(include='number')
        corr = numeric_data.corr()

        st.markdown("Here are some patterns we noticed between your columns:")

        seen = set()
        found = 0

        for col1 in corr.columns:
            for col2 in corr.columns:
                if col1 != col2 and (col2, col1) not in seen:
                    value = corr[col1][col2]

                    if abs(value) > 0.5:
                        direction = "increase together" if value > 0 else "move in opposite directions"
                        st.write(f"🔎 When **{col1}** increases, **{col2}** tends to {direction}.")
                        seen.add((col1, col2))
                        found += 1

        if found == 0:
            st.write("We didn't find any strong patterns between your numeric columns.")

