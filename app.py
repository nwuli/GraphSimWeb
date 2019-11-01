from flask import Flask,jsonify,render_template
from Neo4j.FetchData import *
app = Flask(__name__)
from neo4j.v1 import GraphDatabase
from report.SimResult import *
from Utils import *
from ParseFile import *
from Graph import *
@app.route('/')
def HomePage():
    #显示主页
    return render_template('index1.html')
@app.route('/graph')
def getData():
    nodes,edges=searchAll()# get all data
    return jsonify(elements={"nodes":nodes,"edges":edges})

@app.route('/Parse')
def GetDiffResult():
    #处理json格式的数据，以函数为单位，返回相差比较大的数据结点
    low_version = "H:\GraphSimWeb\jsondata\sV1.0"
    high_version = "H:\GraphSimWeb\jsondata\sV1.1"
    base_file_list = []
    target_file_list = []
    pairfileList = []
    getfilePath(low_version, base_file_list)
    getfilePath(high_version, target_file_list)
    PairMethodGraph = getpairMethodGraph(base_file_list, target_file_list)
    #得到相似性结果
    SIm = getMethodSim(PairMethodGraph)# result of parsing similarity
    sim = SimResult(SIm) # all diffFile
    #返回的是：文件名&函数名
    normaldiff,connectdiff = sim.PareFileResult()
    nodes,edges=serachDiff(normaldiff,connectdiff)
    return jsonify(elements={"nodes": nodes, "edges": edges})

if __name__ == '__main__':
    app.run(debug=True)
