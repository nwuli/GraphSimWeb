from neo4j.v1 import GraphDatabase
from app import *

driver = GraphDatabase.driver("bolt://localhost:11005", auth=("neo4j", "1814"))


# 查找图数据中的所有的结点，然后在前台页面显示
def searchAll():
    with driver.session() as session:
        # 注意p,r,q的字段信息
        results = session.run("MATCH(p)-[r]->(q) RETURN p,r,q").values()
        nodesList = []
        edgesList = []
        for result in results:
            nodesList.append(result[0])
            nodesList.append(result[2])
            # 去除结点列表中的重复元素,
            # nodesList=list(set(tuple(nodesList)))
            edgesList.append(result[1])
        nodes = list(map(buildNodes, nodesList))
        edges = list(map(buildEdges, edgesList))
        return nodes, edges


def serachDiff(normaldiff, connectdiff):
    # 根据变化的文件进行查询，返回查询结果
    allmethod = normaldiff + connectdiff
    nodeLists = []
    edgeLists = []
    for method in allmethod:
        filsplit = os.path.split(method)
        filename = filsplit[1].replace("&", "-")
        with driver.session() as session:

            # TODO 注意查询````````这个符号不是单引号
            results = session.run("MATCH (p:`{p1}`)-[r]->(q) RETURN p,r,q".format(p1=filename)).values()
            for result in results:
                #只统计p结点的个数
                nodeLists.append(result[0])
                #nodeLists.append(result[2])
                # TODO 去除重复元素
                nodeLists = list(set(nodeLists))
                edgeLists.append(result[1])
    diffnodes = list(map(buildNodes, nodeLists))
    diffedges = list(map(buildEdges, edgeLists))
    allnodes,alledges=searchAll() #get all nodes、edges
    nodes,edges=addDiff(allnodes,alledges,diffnodes,diffedges) # add diif flag:nodeType:"change"
    return nodes,edges


def buildNodes(node):
    # TODO 元组的顺序发生变化
    data = {"id": node._id, "version": list(node._labels)[1], "fileName": list(node._labels)[0]}
    # 添加结点类型字典
    notype = node._properties["nodeType"]

    data.update({"attribute": node._properties})
    data.update({"nodeType": notype})
    return {"data": data}


def buildEdges(edge):
    data = {"source": edge._start_node._id, "target": edge._end_node._id, "relationship": edge.type}
    return {"data": data}


def addDiff(_nodes,_edges,nodes,edges):
    # 对于发生改变的结点添加nodeType="change"
    for node ,index in zip(_nodes,range(len(_nodes))):#遍历图中所有的结点
        nodeData=node["data"]
        for nodediff in nodes:
            nodeDiffData=nodediff["data"]
            if(nodeData["id"]==nodeDiffData["id"]):
                tegetID=nodeData["id"]
                #为变化的结点添加修改标注
                _nodes[index]["data"].update({"nodeType":"change"})
    return _nodes,_edges

if __name__ == '__main__':
    low_version = "F:\GraphWeb\jsondata\sV1.0"
    high_version = "F:\GraphWeb\jsondata\sV1.1"
    base_file_list = []
    target_file_list = []
    pairfileList = []
    getfilePath(low_version, base_file_list)
    getfilePath(high_version, target_file_list)
    PairMethodGraph = getpairMethodGraph(base_file_list, target_file_list)
    SIm = getMethodSim(PairMethodGraph)
    sim = SimResult(SIm)
    normaldiff, connectdiff = sim.PareFileResult()
    serachDiff(normaldiff, connectdiff)
