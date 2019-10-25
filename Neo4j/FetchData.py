from neo4j.v1 import GraphDatabase
from app import *
driver=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","1814"))
def searchAll():
    with driver.session() as session:
        #注意p,r,q的字段信息
        results=session.run("MATCH(p)-[r]->(q) RETURN p,r,q").values()
        nodesList=[]
        edgesList=[]
        for result in results:
            nodesList.append(result[0])
            nodesList.append(result[2])
            #去除结点列表中的重复元素,
            #nodesList=list(set(tuple(nodesList)))
            edgesList.append(result[1])
        nodes=list(map(buildNodes,nodesList))
        edges=list(map(buildEdges,edgesList))
        return nodes,edges
def serachDiff():
    pass