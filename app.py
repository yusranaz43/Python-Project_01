import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", page_icon="🧹", layout="wide")

#custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: "black";
        color: "white";
        }
        </style>
        """,
        unsafe_allow_html=True
)

#title and descrition
st.title("⚡Efficient Data Cleaning & Processing By Yusra Naz")
st.write("An efficient tool for data cleaning, preprocessing, and analysis.")

#upload file
st.sidebar.title("Upload File")
uploaded_files = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)

        elif file_ext == ".xlsx":
            df = pd.read_excel(file)

        else:
            st.error(f"Please upload a valid file format: {file_ext}")
            continue


            #show data
            st.write("Preview the head of the data")
            st.dataframe(df.head())


            #data cleaning options
            st.subheader("🛠️Data Cleaning OPtions")
            if st.checkbox(f"Clean data for {file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Drop Duplicates from the file{file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("✔️Duplicated dropped successfully!")

                with col2:
                    if st.button(f"Fill missing values in {file.name}"):
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✔️Missing values filled successfully!")    

            st.subheader("🎯Select Columns to Keep")
            columns = st.multiselect("Select Columns {file.name}", df.columns, default=df.columns)
            df = df[columns]


            #data visulaization
            st.subheader("📊Data Visualization")
            if st.checkbox(f"Show Data Summary for {file.name}"):
                st.bar_chart(df.select_dtypes(include=["number"]).iloc[: , :2])

            #conversion options
            st.subheader("🔄Conversion OPtions")
            conversion_type = st.radio(f"Convert {file.name} to", ["csv", "xlsx"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to.csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "XLSX":
                    df.to.excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label= f"Click here to download {file_name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime = mime_type
                ) 

st.success("🎉 All files processed successfully!")                   
