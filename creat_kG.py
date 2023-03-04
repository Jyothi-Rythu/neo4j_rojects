neo4j_query("""
MATCH (n) DETACH DELETE n;
""")

#Create a first main node
neo4j_query("""
MERGE (l:LaborMarket {name:"Labor Market"}) 
RETURN l
""")

#add entities to KG: skills, expereince, diploma, major-diploma
neo4j_query("""
MATCH (l:LaborMarket)
UNWIND $data as row
MERGE (o:Offer{id:row.text_sha256})
SET o.text = row.text
MERGE (l)-[:HAS_OFFER]->(o)
WITH o, row.annotations as entities
UNWIND entities as entity
MERGE (e:Entity {id:entity.id})
ON CREATE SET 
              e.name = entity.text,
              e.label = entity.label_upper
MERGE (o)-[m:MENTIONS]->(e)
ON CREATE SET m.count = 1
ON MATCH SET m.count = m.count + 1
WITH e as e
CALL apoc.create.addLabels( id(e), [ e.label ] )
YIELD node
REMOVE node.label
RETURN node
""", {'data': parsed_ents})

#Add property 'name' to entity EXPERIENCE
res = neo4j_query("""
MATCH (e:EXPERIENCE)
RETURN e.id as id, e.name as name
""")
# Extract the number of years from the EXPERIENCE name and store in property years
import re
def get_years(name):
  return re.findall(r"\d+",name)[0]
res["years"] = res.name.map(lambda name: get_years(name))
data = res.to_dict('records')
#Add property 'years' to entity EXPERIENCE
neo4j_query("""
UNWIND $data as row
MATCH (e:EXPERIENCE {id:row.id})
SET e.years = row.years
RETURN e.name as name, e.years as years
""",{"data":data})

#Add relations to KG
neo4j_query("""
UNWIND $data as row
MATCH (source:Entity {id: row.head})
MATCH (target:Entity {id: row.tail})
MATCH (offer:Offer {id: row.source})
MERGE (source)-[:REL]->(r:Relation {type: row.type})-[:REL]->(target)
MERGE (offer)-[:MENTIONS]->(r)
""", {'data': predicted_rels})
