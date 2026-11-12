import calendar
import csv
import io
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ---------- อ่านไฟล์ ----------
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


# ---------- จัดข้อมูลให้เป็น "แถว" (list ของ dict) ----------
def to_rows(data):
    """แปลงข้อมูล JSON ทุกแบบให้เป็น list ของ dict"""
    # list ของ dict อยู่แล้ว
    if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
        return data

    # list ธรรมดา
    if isinstance(data, list):
        return [{"ลำดับ": i, "ข้อมูล": str(item)} for i, item in enumerate(data, start=1)]

    # dict
    if isinstance(data, dict):
        rows = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            rows.append({"key": key, "value": str(value)})
        return rows

    # ค่าเดี่ยว ๆ
    return [{"value": str(data)}]


# ---------- ค้นหา / ดาวน์โหลด ----------
def search_rows(rows, keyword):
    """คืนเฉพาะแถวที่มีคำค้นหาอยู่ในช่องใดช่องหนึ่ง (ไม่สนตัวพิมพ์เล็ก/ใหญ่)"""
    if not keyword:
        return rows
    keyword = keyword.lower()
    return [
        row for row in rows
        if any(keyword in str(value).lower() for value in row.values())
    ]


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


# ---------- แดชบอร์ด: คำนวณทั้งหมดอยู่ที่นี่ ไม่ใช่ใน UI ----------
def build_dashboard(rows):
    """ดูคอลัมน์ของไฟล์ แล้วคำนวณข้อมูลแดชบอร์ดให้พร้อมวาด
    คืน dict ที่มี "type" = calendar / coverage / variance (ไม่รองรับ -> None)"""
    cols = set(rows[0]) if rows else set()

    # ปฏิทิน: weeks = สัปดาห์ละ 7 ช่อง {"day": วันที่ (0 = ว่าง), "items": [รายการ]}
    if {"date", "zone", "warehouse"} <= cols:
        year, month = int(rows[0]["date"][:4]), int(rows[0]["date"][5:7])
        by_day = {}
        for r in rows:
            by_day.setdefault(int(r["date"][8:10]), []).append(r)
        weeks = [
            [{"day": d, "items": by_day.get(d, [])} for d in week]
            for week in calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)
        ]
        return {"type": "calendar", "title": f"{calendar.month_name[month]} {year}", "weeks": weeks}

    # Coverage: เพิ่ม pct (เปอร์เซ็นต์ที่นับแล้ว)
    if {"warehouse", "counted", "total"} <= cols:
        bars = [{**r, "pct": r["counted"] / r["total"] * 100 if r["total"] else 0} for r in rows]
        return {"type": "coverage", "bars": bars}

    # Variance: เพิ่ม width (เทียบค่าสูงสุด) และ level (high/mid/low)
    if {"zone", "variance_pct"} <= cols:
        top = max(r["variance_pct"] for r in rows) or 1
        bars = []
        for r in rows:
            v = r["variance_pct"]
            level = "high" if v > 3 else "mid" if v > 1.5 else "low"
            bars.append({**r, "width": v / top * 100, "level": level})
        return {"type": "variance", "bars": bars}

    return None
