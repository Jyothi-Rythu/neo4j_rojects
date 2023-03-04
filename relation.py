import random
import typer
from pathlib import Path
import spacy
from spacy.tokens import DocBin, Doc
from spacy.training.example import Example

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

#restart the runtime after installation of deps
nlp2 = spacy.load("/content/drive/MyDrive/training_rel_roberta/model-best")

def extract_relations(documents,nlp,nlp2):
  predicted_rels = list()
  for doc in nlp.pipe(documents, disable=["tagger", "parser"]):
    source_hash = hashlib.sha256(doc.text.encode('utf-8')).hexdigest()
    for name, proc in nlp2.pipeline:
          doc = proc(doc)

    for value, rel_dict in doc._.rel.items():
      for e in doc.ents:
        for b in doc.ents:
          if e.start == value[0] and b.start == value[1]:
            max_key = max(rel_dict, key=rel_dict. get)
            #print(max_key)
            e_id = hashlib.sha256(str(e).encode('utf-8')).hexdigest()
            b_id = hashlib.sha256(str(b).encode('utf-8')).hexdigest()
            if rel_dict[max_key] >=0.9 :
              #print(f" entities: {e.text, b.text} --> predicted relation: {rel_dict}")
              predicted_rels.append({'head': e_id, 'tail': b_id, 'type':max_key, 'source': source_hash})
  return predicted_rels

predicted_rels = extract_relations(documents,nlp,nlp2)
