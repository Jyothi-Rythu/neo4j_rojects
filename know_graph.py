documents = get_all_documents()
documents = documents[:]
parsed_ents = extract_ents(documents,nlp)
predicted_rels = extract_relations(documents,nlp,nlp2)

#basic neo4j query function  
from neo4j import GraphDatabase
import pandas as pd

host = 'bolt:/3308:15'
user = 'neo4j'
password = 'neo4j'
driver = GraphDatabase.driver(host,auth=(user, password))

def neo4j_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params)
        return pd.DataFrame([r.values() for r in result], columns=result.keys())
