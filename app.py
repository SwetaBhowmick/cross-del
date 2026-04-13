import streamlit as st
import pandas as pd

st.set_page_config(page_title="Column Cleaner Tool", layout="wide")

st.title("🧹 Column A Cleaner (Remove values found in Column B)")

# -------------------------------
# Helper Function (Clean Text)
# -------------------------------
def clean_text(text):
    if pd.isna(text):
        return None
    return " ".join(str(text).strip().split()).lower()

# -------------------------------
# Upload File
# -------------------------------
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Preview Data")
    st.dataframe(df.head())

    columns = df.columns.tolist()

    col_a = st.selectbox("Select Column A (Main Data)", columns)
    col_b = st.selectbox("Select Column B (Reference - values to remove)", columns)

    if st.button("🚀 Clean Column A"):

        # -------------------------------
        # Clean both columns
        # -------------------------------
        df["A_clean"] = df[col_a].apply(clean_text)
        df["B_clean"] = df[col_b].apply(clean_text)

        # -------------------------------
        # Create reference set
        # -------------------------------
        reference_values = set(df["B_clean"].dropna())

        # -------------------------------
        # Mark rows
        # -------------------------------
        df["Action"] = df["A_clean"].apply(
            lambda x: "DELETE" if x in reference_values else "KEEP"
        )

        # -------------------------------
        # Filter cleaned data
        # -------------------------------
        cleaned_df = df[df["Action"] == "KEEP"].copy()

        st.success("✅ Cleaning Completed!")

        st.subheader("Cleaned Data (Column A without matches)")
        st.dataframe(cleaned_df)

        # -------------------------------
        # Download
        # -------------------------------
        output_file = "cleaned_output.xlsx"
        cleaned_df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Download Cleaned Excel",
                data=f,
                file_name="cleaned_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
