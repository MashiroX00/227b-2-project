import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.prepareDataset import loadDataset
from transformers import AutoModelForCausalLM, Trainer, DataCollatorForLanguageModeling, TrainingArguments
from utils.tok import initToken
name = "wordprediction2"
BASE_MODEL = "gpt2"
dataseturl = "HuggingFaceTB/everyday-conversations-llama3.1-2k"
token = initToken(BASE_MODEL)
ds = loadDataset(token,name=dataseturl)
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)
trainer = Trainer(model=model,
                  args=TrainingArguments("out",num_train_epochs=3,per_device_train_batch_size=8),
                  train_dataset=ds["train_sft"],
                  data_collator=DataCollatorForLanguageModeling(token,mlm=False))
trainer.train()
model.save_pretrained(name)
token.save_pretrained(name)