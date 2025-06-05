# app/job_browser.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
import psycopg2
from config.config_loader import load_config

# Load cấu hình database từ file config
DB_CONFIG = load_config()["database"]

def get_data(limit=100):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT s.*, r.description AS raw_description
            FROM structured_jobs s
            LEFT JOIN raw_jobs r ON s.id = r.id
            ORDER BY s.date_posted DESC
            LIMIT %s
        """
        df = pd.read_sql(query, conn, params=(limit,))
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Lỗi kết nối cơ sở dữ liệu: {e}")
        return pd.DataFrame()

def render_sidebar(df):
    st.sidebar.header("🔎 Bộ lọc")
    
    locations = ["Tất cả"] + sorted(df['location'].dropna().unique().tolist())
    selected_location = st.sidebar.selectbox("Địa điểm", locations)

    seniorities = ["Tất cả"] + sorted(df['seniority'].dropna().unique().tolist())
    selected_seniority = st.sidebar.selectbox("Cấp bậc", seniorities)

    filtered_df = df.copy()

    if selected_location != "Tất cả":
        filtered_df = filtered_df[filtered_df["location"] == selected_location]
    if selected_seniority != "Tất cả":
        filtered_df = filtered_df[filtered_df["seniority"] == selected_seniority]

    return filtered_df

def render_job_list(df):
    st.title("💼 Việc làm AI Engineer")

    if 'selected_index' not in st.session_state:
        st.session_state.selected_index = 0

    left_col, right_col = st.columns([2, 3])
    with left_col:
        for i, row in df.iterrows():
            with st.container(border=True):
                if st.button(row['job_title'], key=f"title_{i}"):
                    st.session_state.selected_index = i
                st.markdown(f"**{row['company']}** – {row['location']}")
                st.caption(f"📅 {row['date_posted']}  •  🧰 {row['seniority'] or 'Không rõ'}")

    with right_col:
        if df.empty:
            st.info("Không có dữ liệu để hiển thị.")
            return

        job = df.iloc[st.session_state.selected_index]
        st.subheader(job['job_title'])
        st.markdown(f"**{job['company']}** – {job['location']}")
        st.markdown(f"**💰 Lương:** {job['salary'] or 'Không rõ'}")
        st.markdown(f"**📊 Cấp bậc:** {job['seniority'] or 'Không rõ'}")
        st.markdown(f"**📅 Ngày đăng:** {job['date_posted']}")

        st.divider()
        st.markdown("### 📝 Mô tả công việc")
        st.markdown(job['job_description'])

        st.markdown("### ✅ Yêu cầu công việc")
        st.markdown(job['job_requirements'])

        st.markdown("### 🎁 Phúc lợi")
        st.markdown(job['benefits'])

        if st.button("📄 Xem mô tả gốc"):
            st.markdown("### 📄 Mô tả gốc từ trang tuyển dụng")
            st.info(job.get("raw_description", "Không có mô tả gốc."))

def main():
    st.set_page_config(page_title="Job Explorer", layout="wide")
    df = get_data()

    if df.empty:
        st.warning("Không có dữ liệu để hiển thị.")
        return

    filtered_df = render_sidebar(df)
    render_job_list(filtered_df)

if __name__ == "__main__":
    main()
