import numpy as np
from scipy.ndimage import gaussian_filter
def generate_terrain_trace(N, H, T, sigma, seed):
    rng = np.random.default_rng(int(seed))
 
    # logits สุ่ม N(0,1): หนึ่งเวคเตอร์ยาว H ต่อหนึ่งคอลัมน์ (x, z)
    raw = rng.normal(size=(N, N, H))
 
    # เบลอตามแกน x, z แล้วปรับ std กลับเป็น 1
    if sigma > 0:
        blurred = gaussian_filter(raw, sigma=(sigma, sigma, 0), mode="wrap")
        normalized = blurred / blurred.std()
    else:
        blurred = raw
        normalized = raw
 
    # softmax
    scaled = normalized / T  # z / T
    shifted = scaled - scaled.max(axis=-1, keepdims=True) # ลบ max ของคอลัมน์
    exp = np.exp(shifted) # e^z
    denom = exp.sum(axis=-1, keepdims=True) # ผลรวมต่อคอลัมน์
    p = exp / denom # ความน่าจะเป็น
 
    # ค่าความน่าจะเป็นของแต่ละระดับ k และความสูงสุดท้าย
    weighted = p * np.arange(H) # k * p_k
    height = weighted.sum(axis=-1) # sum_k k * p_k
 
    return {
        "raw": raw,
        "blurred": blurred,
        "normalized": normalized,
        "scaled": scaled,
        "shifted": shifted,
        "exp": exp,
        "denom": denom[..., 0],
        "p": p,
        "weighted": weighted,
        "height": height,
    }
 
 
def generate_terrain(N, H, T, sigma, seed):
    return generate_terrain_trace(N, H, T, sigma, seed)["height"]