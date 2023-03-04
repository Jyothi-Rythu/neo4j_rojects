import hashlib

def extract_ents(documents,nlp):
  docs = list()
  for doc in nlp.pipe(documents, disable=["tagger", "parser"]):
      dictionary=dict.fromkeys(["text", "annotations"])
      dictionary["text"]= str(doc)
      dictionary['text_sha256'] =  hashlib.sha256(dictionary["text"].encode('utf-8')).hexdigest()
      annotations=[]
      
      for e in doc.ents:
        ent_id = hashlib.sha256(str(e.text).encode('utf-8')).hexdigest()
        ent = {"start":e.start_char,"end":e.end_char, "label":e.label_,"label_upper":e.label_.upper(),"text":e.text,"id":ent_id}
        if e.label_ == "EXPERIENCE":
          ent["years"] = int(e.text[0])

        annotations.append(ent)
        
      dictionary["annotations"] = annotations
      docs.append(dictionary)
  #print(annotations)
  return docs

parsed_ents = extract_ents(documents,nlp)
