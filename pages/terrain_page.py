import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from services.terrain_generator_service import generate_terrain_trace

MAX_SPAN = 12 

st.title("Terrain Generator")

N = st.sidebar.slider("Size (N x N)", 16, 64, 16)
H = st.sidebar.slider("Height levels", 8, 64, 16)
T = st.sidebar.slider("Softmax temperature", 0.05, 3.0, 0.3)
sigma = st.sidebar.slider("Smooth (sigma)", 0.0, 8.0, 3.0)
seed = st.sidebar.number_input("Seed", value=0, step=1)
voxel = st.sidebar.checkbox("Blocky (voxel) look", True)
decimals = st.sidebar.slider("ทศนิยมในตาราง", 1, 8, 4)


@st.cache_data(show_spinner=False)
def get_trace(N, H, T, sigma, seed):
    return generate_terrain_trace(N, H, T, sigma, seed)


tr = get_trace(N, H, T, sigma, int(seed))
h_soft = tr["height"]
h = np.floor(h_soft) if voxel else h_soft

fig = go.Figure(go.Surface(z=h, colorscale="Earth", showscale=False))
fig.update_layout(height=700, scene=dict(aspectmode="data"),
                  margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)

def range_picker(label, n, key, default_span=8):
    lo, hi = st.slider(label, 0, n - 1, (0, min(default_span, n) - 1),
                       key=f"{key}_{n}")
    if hi - lo + 1 > MAX_SPAN:
        hi = lo + MAX_SPAN - 1
        st.warning(f"{label}: แสดงสูงสุด {MAX_SPAN} ช่อง ตัดเหลือ {lo} ถึง {hi}")
    return lo, hi


def show(df):
    st.dataframe(df.style.format(f"{{:.{decimals}f}}"))

st.header("ดูตัวเลขในแต่ละขั้น")
tab_col, tab_layer, tab_map = st.tabs([
    "1) คอลัมน์เดียว: ตามดูทีละฟังก์ชัน",
    "2) ตารางของระดับ k เดียว",
    "3) ความสูงทั้งแผนที่ (ช่วงที่เลือก)",
])
with tab_col:
    c1, c2 = st.columns(2)
    x = c1.number_input("x", 0, N - 1, 0, key=f"col_x_{N}")
    z = c2.number_input("z", 0, N - 1, 0, key=f"col_z_{N}")
    k0, k1 = range_picker("ช่วงระดับ k ที่จะดู", H, "col_k")

    ks = np.arange(k0, k1 + 1)
    table = pd.DataFrame({
        "raw": tr["raw"][x, z, ks],
        "blurred": tr["blurred"][x, z, ks],
        "normalized": tr["normalized"][x, z, ks],
        "scaled (z/T)": tr["scaled"][x, z, ks],
        "shifted (z/T - max)": tr["shifted"][x, z, ks],
        "exp": tr["exp"][x, z, ks],
        "p (exp/sum)": tr["p"][x, z, ks],
        "k*p": tr["weighted"][x, z, ks],
    }, index=pd.Index(ks, name="k"))
    show(table)

    full_p = tr["p"][x, z]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("sum(exp) ทั้งคอลัมน์", f"{tr['denom'][x, z]:.{decimals}f}")
    m2.metric("sum(p) ทั้งคอลัมน์", f"{full_p.sum():.{decimals}f}")
    m3.metric("h = sum(k*p)", f"{h_soft[x, z]:.{decimals}f}")
    m4.metric("k ที่ p สูงสุด", f"{int(full_p.argmax())}")
    st.caption(
        "ตารางแสดงเฉพาะช่วง k ที่เลือก แต่ sum และ h ด้านล่างคิดจาก k ทั้ง "
        f"0 ถึง {H - 1} ของคอลัมน์ ({x}, {z}) "
        "| raw = rng.normal | blurred = gaussian_filter | normalized = /std "
        "| scaled = /T | shifted = ลบ max | exp = np.exp | p = exp/sum "
        "| k*p = p*np.arange(H)"
    )

with tab_layer:
    stage = st.selectbox(
        "ขั้นตอน",
        ["raw", "blurred", "normalized", "scaled", "shifted",
         "exp", "p", "weighted"],
        index=2, key="layer_stage")
    k = st.number_input("ระดับ k", 0, H - 1, 0, key=f"layer_k_{H}")
    xa, xb = range_picker("ช่วง x (แถว)", N, "layer_x")
    za, zb = range_picker("ช่วง z (คอลัมน์)", N, "layer_z")
    grid = tr[stage][xa:xb + 1, za:zb + 1, k]
    show(pd.DataFrame(grid, index=pd.Index(range(xa, xb + 1), name="x"),
                      columns=pd.Index(range(za, zb + 1), name="z")))
    st.caption("แถว = x, คอลัมน์ = z. เทียบ raw กับ blurred จะเห็นว่าช่องข้างเคียงใกล้กันขึ้น")

with tab_map:
    xa, xb = range_picker("ช่วง x (แถว)", N, "map_x")
    za, zb = range_picker("ช่วง z (คอลัมน์)", N, "map_z")
    idx = pd.Index(range(xa, xb + 1), name="x")
    cols = pd.Index(range(za, zb + 1), name="z")
    cl, cr = st.columns(2)
    cl.write("h = sum(k*p)")
    with cl:
        show(pd.DataFrame(h_soft[xa:xb + 1, za:zb + 1], index=idx, columns=cols))
    if voxel:
        cr.write("floor(h) ที่ใช้วาดกราฟ")
        with cr:
            show(pd.DataFrame(h[xa:xb + 1, za:zb + 1], index=idx, columns=cols))