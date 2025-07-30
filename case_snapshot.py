import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="CCF Update App")

st.title("📊 CCF Update App")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = [c.strip().lower() for c in df.columns]

        if "date" not in df.columns or "case id" not in df.columns:
            st.error("❌ File must contain 'case id' and 'date' columns.")
        else:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.dropna(subset=["date"])

            summary = df.groupby(df["date"].dt.date).size().reset_index(name="cases")
            now = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")

            message = f"📊 Case Snapshot – {now}\n\n"
            for _, row in summary.iterrows():
                message += f"• {row['date'].strftime('%d/%m/%Y')} – {row['cases']} cases\n"

            st.text_area("📝 Copy this message to send to Teams:", message, height=200)
            st.success("✅ Done! You can now copy and paste this message into Teams.")
    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
