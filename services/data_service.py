import csv
import io
import json
from pathlib import Path

# หาโฟลเดอร์โปรเจกต์ และโฟลเดอร์ data
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


#1) อ่านไฟล์ 
def get_file_names():
    """คืนรายชื่อไฟล์ .json ในโฟลเดอร์ data/ เช่น ['raw_data.json']"""
    names = []
    for file in DATA_DIR.glob("*.json"):
        names.append(file.name)
    return sorted(names)


def load_json(file_name):
    """อ่านไฟล์ JSON แล้วคืนข้อมูลกลับไป (ถ้าไฟล์พังจะ raise ValueError)"""
    file = DATA_DIR / file_name
    if not file.exists():
        raise ValueError(f"ไม่พบไฟล์ {file_name}")
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"ไฟล์ JSON ไม่ถูกต้อง: {e}")


def get_file_size_kb(file_name):
    """คืนขนาดไฟล์เป็น KB"""
    return (DATA_DIR / file_name).stat().st_size / 1024


# 2) จัดข้อมูลให้เป็น "แถว" (list ของ dict) สำหรับแสดงเป็นตาราง
def to_rows(data):
    """แปลงข้อมูล JSON ทุกแบบให้เป็น list ของ dict"""
    # แบบที่ 1: list ของ dict อยู่แล้ว เช่น [{"name": "A"}, {"name": "B"}]
    if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
        return data

    # แบบที่ 2: list ธรรมดา เช่น ["ข้อความ1", "ข้อความ2"]
    if isinstance(data, list):
        rows = []
        for i, item in enumerate(data, start=1):
            rows.append({"ลำดับ": i, "ข้อมูล": str(item)})
        return rows

    # แบบที่ 3: dict เช่น {"key1": "...", "key2": [...]}
    if isinstance(data, dict):
        rows = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)  # ซ้อนอยู่ -> แปลงเป็นข้อความ
            rows.append({"key": key, "value": str(value)})
        return rows

    # แบบที่ 4: ค่าเดี่ยว ๆ
    return [{"value": str(data)}]


# 3) ค้นหา / สรุป / ดาวน์โหลด 
def search_rows(rows, keyword):
    """คืนเฉพาะแถวที่มีคำค้นหาอยู่ในช่องใดช่องหนึ่ง (ไม่สนตัวพิมพ์เล็ก/ใหญ่)"""
    if not keyword:
        return rows
    keyword = keyword.lower()
    result = []
    for row in rows:
        for value in row.values():
            if keyword in str(value).lower():
                result.append(row)
                break  # เจอแล้วไม่ต้องดูช่องอื่นของแถวนี้
    return result


def summarize_columns(rows):
    """สรุปแต่ละคอลัมน์: มีกี่แถวที่ช่องนั้นมีค่า"""
    counts = {}
    for row in rows:
        for key, value in row.items():
            counts[key] = counts.get(key, 0) + (1 if value not in (None, "") else 0)
    return [{"คอลัมน์": k, "จำนวนที่มีค่า": v} for k, v in counts.items()]


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
