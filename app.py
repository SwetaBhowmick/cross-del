import streamlit as st
import pandas as pd

st.set_page_config(page_title="Column Cleaner Tool", layout="wide")

st.title("🧹 Column A Cleaner (Keep blanks instead of deleting rows)")

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
    col_b = st.selectbox("Select Column B (Reference)", columns)

    if st.button("🚀 Clean Column A (Keep Blanks)"):

        # -------------------------------
        # Clean columns for matching
        # -------------------------------
        df["A_clean"] = df[col_a].apply(clean_text)
        df["B_clean"] = df[col_b].apply(clean_text)

        # -------------------------------
        # Create reference set
        # -------------------------------
        reference_values = set(df["B_clean"].dropna())

        # -------------------------------
        # Replace matches with BLANK
        # -------------------------------
        def remove_if_match(original, cleaned):
            if cleaned in reference_values:
                return ""   # keep blank
            return original

        df["Updated_A"] = df.apply(
            lambda row: remove_if_match(row[col_a], row["A_clean"]),
            axis=1
        )

        st.success("✅ Cleaning Completed (Blanks kept)!")

        st.subheader("Updated Data")
        st.dataframe(df)

        # -------------------------------
        # Download
        # -------------------------------
        output_file = "cleaned_with_blanks.xlsx"
        df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Download Excel",
                data=f,
                file_name="cleaned_with_blanks.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
