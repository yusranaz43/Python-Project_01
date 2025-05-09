import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", page_icon="🧹", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("⚡Efficient Data Cleaning & Processing By Yusra Naz")
st.write("An efficient tool for data cleaning, preprocessing, and analysis.")

# Upload file
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
            st.error(f"❌ Please upload a valid file format: {file_ext}")
            continue

        # Show data preview
        st.subheader(f"📄 Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Drop Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✔️ Duplicates dropped successfully!")

            with col2:
                if st.button(f"Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✔️ Missing values filled successfully!")    

        # Select columns
        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Data Summary for {file.name}"):
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

        # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "XLSX"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "XLSX":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Click to Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")  
