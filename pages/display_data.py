import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from services.data_service import (  # noqa: E402
    get_file_names,
    get_file_size_kb,
    load_json,
    rows_to_csv,
    search_rows,
    summarize_columns,
    to_rows,
)

# ---------- หัวหน้าเพจ ----------
st.title("📂 Data Viewer")
st.caption("ดึงและแสดงข้อมูลดิบจากโฟลเดอร์ data/")

# 1) ให้ผู้ใช้เลือกไฟล์ 
file_names = get_file_names()  # ขอรายชื่อไฟล์จาก service

if not file_names:
    st.warning("ไม่พบไฟล์ .json ในโฟลเดอร์ data/")
    st.stop()  # หยุดหน้านี้ตรงนี้

selected_file = st.selectbox("เลือกไฟล์ข้อมูล", file_names)

# 2) อ่านข้อมูล 
try:
    data = load_json(selected_file)
except ValueError as e:  # ไฟล์ไม่เจอ หรือ JSON พัง
    st.error(str(e))
    st.stop()

rows = to_rows(data)  # ให้ service จัดเป็นแถว ๆ

# 3) ตัวเลขสรุป 3 ช่อง 
col1, col2, col3 = st.columns(3)
col1.metric("ชื่อไฟล์", selected_file)
col2.metric("ขนาดไฟล์", f"{get_file_size_kb(selected_file):.1f} KB")
col3.metric("จำนวนแถว", len(rows))

# 4) แบ่งเป็น 3 แท็บ 
tab_table, tab_json, tab_summary = st.tabs(["📊 ตาราง", "🧾 JSON ดิบ", "📋 สรุปคอลัมน์"])

with tab_table:
    keyword = st.text_input("🔍 ค้นหาในตาราง", placeholder="พิมพ์คำที่ต้องการค้นหา")
    rows_show = search_rows(rows, keyword)  # ถ้าไม่พิมพ์อะไร จะได้ทุกแถว

    if keyword:
        st.caption(f"พบ {len(rows_show)} แถว")

    st.dataframe(rows_show)

    st.download_button(
        "⬇️ ดาวน์โหลดเป็น CSV",
        data=rows_to_csv(rows_show),
        file_name=f"{selected_file}.csv",
        mime="text/csv",
    )

with tab_json:
    st.json(data)

with tab_summary:
    st.dataframe(summarize_columns(rows))
