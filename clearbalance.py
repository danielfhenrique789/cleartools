import pandas as pd
import os

# Get csv files list
path = 'data/'
files = os.listdir(path)
csv_files = [path+f for f in files if f.endswith('.csv')]

# Reading files
dfs = []
for file in csv_files:
    dfs.append(pd.read_csv(file, delimiter=';'))

# Concatenate all data into one DataFrame
df = pd.concat(dfs, ignore_index=True)

# Renaming Columns
columns = ["operation","closeout","value","description","final_balance"]
df.columns = columns

df["split_desc"] = df["description"].apply(lambda x: x.split())
df["type"] = df["split_desc"].apply(lambda x: x[0])

def get_qtd(x):
  if x[0] in ["RENDIMENTO","DIVIDENDOS"]:
    return x[1]
  elif x[0] in ["JUROS"]:
    return x[2]
  else: return None

def get_ticket(x):
  if x[0] in ["DIVIDENDOS","RENDIMENTO","JUROS"]:
    return x[len(x)-1]
  else: return None

df["qtd"] = df["split_desc"].apply(get_qtd)

df["ticket"] = df["split_desc"].apply(get_ticket)

df = df.drop("split_desc", axis=1)
