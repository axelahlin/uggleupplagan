import pandas as pd
from transformers import AutoTokenizer

# Load the data into a pandas df
data = pd.read_json("json_dump.json")

data.head()

kbberttokenizer = "KB/bert-base-swedish-cased"

tokenizer = AutoTokenizer.from_pretrained()


def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)


texts_encoded = data.map(tokenize, batched=True, batch_size=None)
