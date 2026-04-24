import pandas as pd
import streamlit as st
from datetime import datetime

st.title("Excel Merge Tool")

file1 = st.file_uploader("Upload File 1", type=["xlsx"])
file2 = st.file_uploader("Upload File 2", type=["xlsx"])

if file1 and file2:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    df1['date'] = pd.to_datetime(df1['date'])
    df2['appointmentDate'] = pd.to_datetime(df2['appointmentDate'])

    merged_df = pd.merge(df1, df2, on='userMobile', how='left')

    merged_df['diff_days'] = (merged_df['appointmentDate'] - merged_df['date']).dt.days

    result_df = merged_df[
        (merged_df['diff_days'] >= 0) &
        (merged_df['diff_days'] <= 3)
    ]

    columns_order = [
        'userMobile',
        'date',
        'appointmentDate',
        'diff_days',
        'Colicose',
        'Livshain',
        'Other Brand'
    ]

    columns_order = [col for col in columns_order if col in result_df.columns]
    result_df = result_df[columns_order]

    st.success("Processing complete!")

    output_file = f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    result_df.to_excel(output_file, index=False)

    with open(output_file, "rb") as f:
        st.download_button("Download Result", f, file_name=output_file)