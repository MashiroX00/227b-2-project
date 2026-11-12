import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from services.data_service import (  # noqa: E402
    build_dashboard,
    get_file_names,
    load_json,
    rows_to_csv,
    search_rows,
    to_rows,
)

# ต้องเป็นคำสั่ง st ตัวแรก
st.set_page_config(page_title="Data Viewer", page_icon="📂", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp {background: linear-gradient(180deg, #ffffff 0%, #e8f0fe 100%);}
.stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp p, [data-testid="stMetric"] * {color:#0f172a;}
[data-testid="stMetricValue"] {color:#1d4ed8;}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {display:none;}
[data-testid="stMetric"], div[data-baseweb="tab-panel"], .card {
    background: #ffffff; border-radius: 16px; padding: 16px 20px;
    border: 1px solid #dbeafe; box-shadow: 0 2px 10px rgba(37,99,235,.08);
}
.cal {width:100%; border-collapse:collapse; table-layout:fixed;}
.cal th {font-size:12px; color:#9ca3af; text-align:left; padding:6px;}
.cal td {height:84px; vertical-align:top; border:1px solid #dbeafe; padding:4px; font-size:12px; color:#6b7280;}
.chip {display:block; border-radius:6px; padding:2px 6px; margin-top:3px; font-size:11px; color:#fff;
       white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.bar-row {display:flex; justify-content:space-between; font-size:13px; margin-top:10px;}
.bar-bg {background:#dbeafe; border-radius:99px; height:8px;}
.bar-fg {height:8px; border-radius:99px;}
</style>
""", unsafe_allow_html=True)

# สีประจำคลังสินค้า (ใช้ทั้งปฏิทินและแถบความคืบหน้า)
COLORS = {"Dallas": "#1e3a8a", "Columbus": "#2563eb", "Reno": "#60a5fa", "Savannah": "#93c5fd"}

# แปลง "ระดับ" ที่ services ส่งมา -> สี
LEVEL_COLORS = {"high": "#1e3a8a", "mid": "#2563eb", "low": "#60a5fa"}


def draw_bar(label, text, width, color):
    """วาดแถบความคืบหน้า 1 แถว (ประกอบ HTML เท่านั้น ไม่คำนวณ)"""
    st.markdown(
        f"<div class='bar-row'><span>{label}</span><span>{text}</span></div>"
        f"<div class='bar-bg'><div class='bar-fg' style='width:{width}%;background:{color}'></div></div>",
        unsafe_allow_html=True,
    )


# ---------- หัวหน้าเพจ ----------
file_names = get_file_names()

if not file_names:
    st.warning("ไม่พบไฟล์ .json ในโฟลเดอร์ data/")
    st.stop()

head_left, head_right = st.columns([3, 1])
head_left.title("Data Viewer")
head_left.caption("Fetch and display raw data from the data/ folder/")
selected_file = head_right.selectbox("Select Data File", file_names)

try:
    data = load_json(selected_file)
except ValueError as e:
    st.error(str(e))
    st.stop()

rows = to_rows(data)

col1, col2 = st.columns(2)
col1.metric("ชื่อไฟล์", selected_file)
col2.metric("จำนวนแถว", len(rows))

tab_table, tab_json, tab_dash = st.tabs(["📊 ตาราง", "🧾 JSON ดิบ", "🗓️ แดชบอร์ด"])

with tab_table:
    keyword = st.text_input("🔍 ค้นหาในตาราง", placeholder="พิมพ์คำที่ต้องการค้นหา")
    rows_show = search_rows(rows, keyword)

    if keyword:
        st.caption(f"พบ {len(rows_show)} แถว")

    st.dataframe(rows_show, use_container_width=True)

    st.download_button(
        "⬇️ ดาวน์โหลดเป็น CSV",
        data=rows_to_csv(rows_show),
        file_name=f"{selected_file}.csv",
        mime="text/csv",
    )

with tab_json:
    st.json(data)

# ---------- แท็บแดชบอร์ด: ขอข้อมูลจาก services แล้ววาดตามที่ได้ ----------
with tab_dash:
    dash = build_dashboard(rows)

    if dash is None:
        st.info("ไฟล์นี้ไม่มีคอลัมน์สำหรับแดชบอร์ด (ลองเลือก count_schedule / coverage / variance)")

    elif dash["type"] == "calendar":
        html = "<table class='cal'><tr>" + "".join(f"<th>{d}</th>" for d in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]) + "</tr>"
        for week in dash["weeks"]:
            html += "<tr>"
            for slot in week:  # day = 0 คือช่องว่างนอกเดือน
                cell = f"<b>{slot['day']}</b>" if slot["day"] else ""
                for r in slot["items"]:
                    cell += f"<span class='chip' style='background:{COLORS.get(r['warehouse'], '#999')}'>{r['zone']}</span>"
                html += f"<td>{cell}</td>"
            html += "</tr>"
        st.subheader(dash["title"])
        st.markdown(html + "</table>", unsafe_allow_html=True)

    elif dash["type"] == "coverage":
        st.subheader("Coverage this quarter")
        for r in dash["bars"]:
            draw_bar(r["warehouse"], f"{r['pct']:.0f}% · {r['counted']} of {r['total']}", r["pct"], COLORS.get(r["warehouse"], "#2563eb"))

    else:
        st.subheader("Variance by zone")
        for r in dash["bars"]:
            draw_bar(r["zone"], f"{r['variance_pct']}%", r["width"], LEVEL_COLORS[r["level"]])
