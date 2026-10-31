from datasets import load_dataset


def _messages_to_text(batch):
    return {
        "text": [
            "\n".join(f"{m['role']}: {m['content']}" for m in convo)
            for convo in batch["messages"]
        ]
    }


def loadDataset(tokenizer, path: str = None, name: str = None,
                split: str = None, max_length: int = 128):
    if name:
        ds = load_dataset(name, split=split)
    elif path:
        ds = load_dataset("text", data_files={"train": path}, split=split)
    else:
        raise ValueError("ต้องระบุ path หรือ name อย่างใดอย่างหนึ่ง")

    # dataset แบบบทสนทนา -> แปลงเป็นข้อความล้วน
    cols = ds.column_names
    if isinstance(cols, dict):          # DatasetDict จะคืน dict ของ split
        cols = next(iter(cols.values()))
    if "messages" in cols:
        ds = ds.map(_messages_to_text, batched=True, remove_columns=cols)
        cols = ["text"]

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    ds = ds.map(                        # ต้องรับค่ากลับมา
        lambda x: tokenizer(x["text"], truncation=True, max_length=max_length),
        batched=True,
        remove_columns=cols,
    )
    return ds