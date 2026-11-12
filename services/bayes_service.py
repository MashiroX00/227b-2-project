import pandas as pd

def calc_complement(probability: float) -> float:
    """คำนวณความน่าจะเป็นของเหตุการณ์ตรงข้าม เช่น 1 - P(A)"""
    return 1.0 - probability

def calc_marginal_b(p_a: float, p_b_given_a: float, p_not_a: float, p_b_given_not_a: float) -> float:
    """คำนวณ P(B) รวมทั้งหมด (Total Probability)"""
    return (p_b_given_a * p_a) + (p_b_given_not_a * p_not_a)
    
def calc_posterior(p_a: float, p_b_given_a: float, p_b: float) -> float:
    """คำนวณ P(A|B) ตามทฤษฎีบทของเบย์"""
    if p_b == 0:
        return 0.0 # ป้องกันการหารด้วย 0
    return (p_b_given_a * p_a) / p_b