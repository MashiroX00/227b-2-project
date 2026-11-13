import calendar
import csv
import io
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def get_file_names():
    """คืนรายชื่อไฟล์ .json ในโฟลเดอร์ data/ เช่น ['raw_data.json']"""
    return sorted(file.name for file in DATA_DIR.glob("*.json"))


def load_json(file_name):
    """อ่านไฟล์ JSON แล้วคืนข้อมูลกลับไป (ถ้าไฟล์พังจะ raise ValueError)"""
    file = DATA_DIR / file_name
    if not file.exists():
        raise ValueError(f"ไม่พบไฟล์ {file_name}")
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"ไฟล์ JSON ไม่ถูกต้อง: {e}")


def to_rows(data):
    """แปลงข้อมูล JSON ทุกแบบให้เป็น list ของ dict"""
    if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
        return data

    if isinstance(data, list):
        return [{"ลำดับ": i, "ข้อมูล": str(item)} for i, item in enumerate(data, start=1)]

    if isinstance(data, dict):
        rows = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            rows.append({"key": key, "value": str(value)})
        return rows

    return [{"value": str(data)}]


def search_rows(rows, keyword):
    """คืนเฉพาะแถวที่มีคำค้นหาอยู่ในช่องใดช่องหนึ่ง (ไม่สนตัวพิมพ์เล็ก/ใหญ่)"""
    if not keyword:
        return rows
    keyword = keyword.lower()
    return [
        row for row in rows
        if any(keyword in str(value).lower() for value in row.values())
    ]


def count_rows(rows):
    """คืนจำนวนแถว"""
    return len(rows)


def rows_to_csv(rows):
    """แปลงแถวเป็น CSV (utf-8-sig เพื่อให้ Excel เปิดภาษาไทยได้)"""
    columns = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8-sig")


def build_dashboard(rows):
    """ดูคอลัมน์ของไฟล์ แล้วคำนวณข้อมูลปฏิทินให้พร้อมวาด
    คืน dict ที่มี title และ weeks (ไม่รองรับ -> None)"""
    cols = set(rows[0]) if rows else set()

    if {"date", "zone", "warehouse"} <= cols:
        year, month = int(rows[0]["date"][:4]), int(rows[0]["date"][5:7])
        by_day = {}
        for r in rows:
            by_day.setdefault(int(r["date"][8:10]), []).append(r)
        weeks = [
            [{"day": d, "items": by_day.get(d, [])} for d in week]
            for week in calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)
        ]
        return {"title": f"{calendar.month_name[month]} {year}", "weeks": weeks}

    return None
