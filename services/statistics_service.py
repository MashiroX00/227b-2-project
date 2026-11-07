
import math
import re
from collections import Counter


# แปลงข้อความที่ผู้ใช้กรอกให้เป็นตัวเลข
def parse_numbers(raw_text):
    if not raw_text.strip():
        raise ValueError("กรุณากรอกตัวเลขอย่างน้อย 1 ค่าขึ้นไปเพื่อให้โปรแกรมคำนวน")

    # แยกตัวเลขด้วยจุลภาค ช่องว่าง หรือขึ้นบรรทัดใหม่
    items = re.split(r"[,;\s]+", raw_text.strip())

    numbers = []

    for item in items:
        try:
            number = float(item)
        except ValueError:
            raise ValueError(
                f"'{item}' ไม่ใช่ค่าตัวเลขที่ถูกต้อง กรุณากรอกตัวเลข 0 - 9 เท่านั้น"
            ) from None

        if not math.isfinite(number):
            raise ValueError("ระบบไม่รองรับค่า NaN หรือ Infinity")

        numbers.append(number)

    return numbers


# คำนวณค่าสถิติทั้งหมด
def calculate_statistics(numbers, data_type="population"):

    n = len(numbers)

    if n == 0:
        raise ValueError("ข้อมูลตัวอย่างต้องมีอย่างน้อย 1 ค่าขึ้นไปเพื่อให้โปรแกรมคำนวณ")

    if data_type not in ("population", "sample"):
        raise ValueError("ประเภทข้อมูลไม่ถูกต้อง กรุณากรอกค่าใหม่")

    if data_type == "sample" and n < 2:
        raise ValueError("ข้อมูลตัวอย่างต้องมีอย่างน้อย 2 ค่าขึ้นไปเพื่อให้โปรแกรมคำนวณ")

    # 1. Mean (ค่าเฉลี่ย)
    mean = sum(numbers) / n

    # 2. Median (มัธยฐาน)
    sorted_numbers = sorted(numbers)

    if n % 2 == 1:
        median = sorted_numbers[n // 2]
    else:
        middle1 = sorted_numbers[n // 2 - 1]
        middle2 = sorted_numbers[n // 2]
        median = (middle1 + middle2) / 2

    # 3. Mode (ฐานนิยม)
    frequency = Counter(numbers)
    highest_frequency = max(frequency.values())

    if highest_frequency == 1:
        modes = []
    else:
        modes = sorted([
            number
            for number, count in frequency.items()
            if count == highest_frequency
        ])

    # 4. Variance (ความแปรปรวน)
    squared_diff_sum = sum(
        (number - mean) ** 2
        for number in numbers
    )

    if data_type == "population":
        denominator = n
    else:
        denominator = n - 1

    variance = squared_diff_sum / denominator

    # 5. Standard Deviation (ส่วนเบี่ยงเบนมาตรฐาน)
    sd = math.sqrt(variance)

    return {
        "count": n,
        "sorted_numbers": sorted_numbers,
        "mean": mean,
        "median": median,
        "modes": modes,
        "variance": variance,
        "sd": sd
    }
