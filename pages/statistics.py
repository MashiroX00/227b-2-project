import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

from services.statistics_service import (
    parse_numbers,
    calculate_statistics
)


st.set_page_config(
    page_title="Statistics Calculator",
    layout="wide"
)

# หัวข้อหน้าเว็บ
st.title("Statistics Calculator")

st.write(
    "โปรแกรมคำนวณ Mean, Median, Mode, "
    "Standard Deviation และ Variance"
)

st.divider()


# ฟอร์มรับข้อมูล
with st.form("statistics_form"):

    input_text = st.text_area("กรอกชุดตัวเลข",
        value="-100, 0, 10, 20, 30, 100",
        help="แยกตัวเลขด้วยจุลภาคหรือช่องว่าง"
    )

    data_type = st.radio("เลือกประเภทข้อมูล",
        options=["population", "sample"],
        format_func=lambda value: (
            "population (ประชากร)"
            if value == "population"
            else "sample (กลุ่มตัวอย่าง)"
        )
    )

    submitted = st.form_submit_button("คำนวณสถิติ", type="primary")


# ทำงานเมื่อกดปุ่มคำนวณ
if submitted:

    try:
        # ส่งข้อความไปแปลงเป็นตัวเลข
        numbers = parse_numbers(input_text)

        # ส่งตัวเลขไปคำนวณ
        result = calculate_statistics(
            numbers,data_type
        )

    except ValueError as error:
        st.error(str(error))

    else:
        st.success(f"คำนวณด้วย Type: {data_type} สำเร็จ")

        st.subheader(f"ผลลัพธ์การคำนวณด้วย Type: {data_type}")

        # เตรียมข้อความแสดงฐานนิยม
        if result["modes"]:
            mode_text = ", ".join(
                f"{value:g}"
                for value in result["modes"]
            )
        else:
            mode_text = "ไม่มีฐานนิยม"

        # แสดงผลลัพธ์แถวแรก
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Mean (ค่าเฉลี่ย)",
            f'{result["mean"]:.4f}'
        )

        col2.metric(
            "Median (มัธยฐาน)",
            f'{result["median"]:.4f}'
        )

        col3.metric(
            "Mode (ฐานนิยม)",
            mode_text
        )

        # แสดงผลลัพธ์แถวที่สอง
        col4, col5 = st.columns(2)

        col4.metric(
            "Standard Deviation",
            f'{result["sd"]:.4f}'
        )

        col5.metric(
            "Variance",
            f'{result["variance"]:.4f}'
        )

        st.divider()

        st.write(
            "จำนวนข้อมูล:",result["count"]
        )

        sorted_text = ", ".join(
            f"{value:g}"
            for value in result["sorted_numbers"]
        )

        st.write(
            "ข้อมูลเรียงจากน้อยไปมาก:",
            sorted_text
        )
