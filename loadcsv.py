import pandas as pd
def get_all_documents():
df = pd.read_csv("/content/drive/MyDrive/job_DB1_1_29.csv",sep='"',header=None)
documents = []
for index,row in df.iterrows():
    documents.append(str(row[0]))
    return documents
documents = get_all_documents()
documents = documents[:]
