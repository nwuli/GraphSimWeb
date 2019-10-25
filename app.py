from flask import Flask,jsonify,render_template
from Neo4j.FetchData import *
app = Flask(__name__)
from neo4j.v1 import GraphDatabase
from report.SimResult import *
from Utils import *
from ParseFile import *
from Graph import *
driver=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","1814"))
@app.route('/')
def HomePage():
    #显示主页
    return render_template('index1.html')
def buildNodes(node):
    #有重复字段出现
    data = {"id": node._id, "version": list(node._labels)[1], "fileName": list(node._labels)[0]}
    #添加结点类型字典
    notype=node._properties["nodeType"]

    data.update({"attribute":node._properties})
    data.update({"nodeType":notype})
    return{"data":data}
def buildEdges(edge):
    data={"source":edge._start_node._id,"target":edge._end_node._id,"relationship":edge.type}
    return {"data":data}
@app.route('/graph')
def getData():
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
    return jsonify(elements={"nodes":nodes,"edges":edges})
@app.route('/Parse')
def GetDiffResult():
    #处理json格式的数据，以函数为单位，返回相差比较大的数据结点
    low_version = "F:\GraphSim\jsondata\V1.0"
    high_version = "F:\GraphSim\jsondata\V1.1"
    base_file_list = []
    target_file_list = []
    pairfileList = []
    getfilePath(low_version, base_file_list)
    getfilePath(high_version, target_file_list)
    PairMethodGraph = getpairMethodGraph(base_file_list, target_file_list)
    #得到相似性结果
    SIm = getMethodSim(PairMethodGraph)
    sim = SimResult(SIm)
    #返回的是：文件名&函数名
    diffs = sim.PareFileResult()
    #
    with driver.session() as session:
        for diff in diffs:
            splits=diff.split("&")
            fileName=splits[0].split("\\\\")
            methodName=splits[1]
            #数据库中待查找到饿结点名字
           # findNodeName=fileName+"-"+methodName
            query="MATCH (p:`CWE190_Integer_Overflow__int_Environment_preinc_81a.java-goodB2G`)-[r]->(q) RETURN p,r,q"
            results=session.run(query)
            nodesList=[]
            edgesList=[]
            for result in results:
                nodesList.append(result[0])
                nodesList.append(result[2])
                # 去除结点列表中的重复元素,
                # nodesList=list(set(tuple(nodesList)))
                edgesList.append(result[1])
            nodes = list(map(buildNodes, nodesList))
            edges = list(map(buildEdges, edgesList))
            _nodes,_edges=searchAll()
            _nodes,_edges=addDiff(_nodes,_edges,nodes,edges)

            #变更变量
            nodes=_nodes
            edges=_edges

        return jsonify(elements={"nodes": nodes, "edges": edges})
def addDiff(_nodes,_edges,nodes,edges):
    for node ,index in zip(_nodes,range(len(_nodes))):
        nodeData=node["data"]
        for nodediff in nodes:
            nodeDiffData=nodediff["data"]
            if(nodeData["id"]==nodeDiffData["id"]):
                tegetID=nodeData["id"]
                #为变化的结点添加修改标注
                _nodes[index]["data"].update({"nodeType":"change"})
    return _nodes,_edges
if __name__ == '__main__':
    app.run(debug=True)
