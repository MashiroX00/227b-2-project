import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import streamlit as st
from services.bayes_service import calc_complement, calc_marginal_b, calc_posterior
st.title("Bayes' Theorem Calculator 📊")
st.markdown("---")

st.markdown("""
**สูตรการคำนวณ:**
$$P(A|B) = \\frac{P(B|A) \\times P(A)}{P(B|A) \\times P(A) + P(B|\\neg A) \\times P(\\neg A)}$$
""")

st.subheader("กำหนดค่าความน่าจะเป็น (เลื่อนเพื่อปรับค่า)")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. โอกาสเกิดเหตุการณ์ A (Prior Probability)**")
    p_a = st.slider("P(A)", min_value=0.0000, max_value=1.0000, value=0.0100, step=0.0100, format="%.4f")
    p_not_a = calc_complement(p_a)
    st.info(f"P(¬A) หรือโอกาสไม่เกิด A = {p_not_a:.4f}")

with col2:
    st.markdown("**2. โอกาสเกิดเหตุการณ์ B เมื่อเทียบกับ A**")
    p_b_given_a = st.slider("P(B|A) (True Positive)", min_value=0.0000, max_value=1.0000, value=0.9000, step=0.0100, format="%.4f")
    p_b_given_not_a = st.slider("P(B|¬A) (False Positive)", min_value=0.0000, max_value=1.0000, value=0.0500, step=0.0100, format="%.4f")

st.markdown("---")
if "prev_p" not in st.session_state:
    st.session_state.prev_p = 0.0
p_b = calc_marginal_b(p_a, p_b_given_a, p_not_a, p_b_given_not_a)

if p_b == 0:
    st.error("ไม่สามารถคำนวณได้เนื่องจาก P(B) มีค่าเป็น 0 (หารด้วยศูนย์)")
else:
    # คำนวณ Bayes Theorem
    p_a_given_b = calc_posterior(p_a, p_b_given_a, p_b)
    
    st.subheader("ผลลัพธ์การคำนวณ (Posterior Probability)")
    diff = p_a_given_b - st.session_state.prev_p
    # ใช้ st.metric ให้ดู Fancy ขึ้น
    st.metric(label="ค่าความน่าจะเป็น P(A|B)", value=f"{p_a_given_b:.4f} ({p_a_given_b * 100:.2f}%)", delta=f"{diff * 100:.2f}%")
    st.session_state.prev_p = p_a_given_b
    
    # ซ่อนวิธีทำไว้ใน expander เพื่อความสะอาดตา
    with st.expander("ดูวิธีทำอย่างละเอียด"):
        st.latex(rf"P(A|B) = \frac{{{p_b_given_a:.4f} \times {p_a:.4f}}}{{({p_b_given_a:.4f} \times {p_a:.4f}) + ({p_b_given_not_a:.4f} \times {p_not_a:.4f})}}")
        st.latex(rf"P(A|B) = \frac{{{p_b_given_a * p_a:.4f}}}{{{p_b:.4f}}} = {p_a_given_b:.4f}")