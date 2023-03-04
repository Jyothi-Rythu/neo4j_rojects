other_id = "8de6e42ddfbc2a8bd7008d93516c57e50fa815e64e387eb2fc7a27000ae904b6"

query = """
MATCH (o1:Offer {id:$id})-[m1:MENTIONS]->(s:Entity)<- [m2:MENTIONS]-(o2:Offer)  
RETURN DISTINCT o1.id as Source,o2.id as Proposed_Offer, count(*) as freq, collect(s.name) as common_terms
ORDER BY freq
DESC LIMIT $limit
"""
res = neo4j_query(query,{"id":other_id,"limit":3})
res

#In neo4j browser,use this query to show graph of best matched job
"""MATCH (o1:Offer {id:"8de6e42ddfbc2a8bd7008d93516c57e50fa815e64e387eb2fc7a27000ae904b6"})-[m1:MENTIONS]->(s:Entity)<- [m2:MENTIONS]-(o2:Offer) 
WITH o1,s,o2, count(*) as freq
MATCH (o1)--(s)
RETURN collect(o2)[0], o1,s, max(freq)""
