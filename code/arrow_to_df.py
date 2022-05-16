from datasets import load_from_disk
import pyarrow as pa
import pandas as pd
from pyarrow import fs

arrow_dataset = load_from_disk("./input/data/train_dataset/")
train_translate = pd.read_csv("./input/data/translate_train_v3.csv")["question"]
val_translate = pd.read_csv("./input/data/translate_val_v3.csv")["question"]
names = arrow_dataset['train'].data.schema.names
metadata = arrow_dataset['train'].data.schema.metadata

train_df = pd.DataFrame(arrow_dataset['train'])
train_df2 = pd.DataFrame(arrow_dataset['train'])
train_df2["question"] = train_translate
train_allData = pd.concat([train_df, train_df2]).to_numpy()
train_allData = np.rot90(np.flip(train_allData, 0), k=-1).tolist()
train_table = pa.table(train_allData, names=names, metadata=metadata)

val_df = pd.DataFrame(arrow_dataset['validation'])
val_df2 = pd.DataFrame(arrow_dataset['validation'])
val_df2["question"] = val_translate
val_allData = pd.concat([val_df, val_df2]).to_numpy()
val_allData = np.rot90(np.flip(val_allData, 0), k=-1).tolist()
val_table = pa.table(val_allData, names=names, metadata=metadata)

with pa.OSFile('./input/data/translate_train_dataset/train/dataset.arrow', 'wb') as sink:
    with pa.RecordBatchStreamWriter(sink, train_table.schema) as writer:
        writer.write_table(train_table)

with pa.OSFile('./input/data/translate_train_dataset/validation/dataset.arrow', 'wb') as sink:
    with pa.RecordBatchStreamWriter(sink, val_table.schema) as writer:
        writer.write_table(val_table)