from transformers import AutoTokenizer

def initToken(name: str):
    tok = AutoTokenizer.from_pretrained(name)
    tok.pad_token = tok.eos_token
    return tok