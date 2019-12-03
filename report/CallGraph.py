import networkx as nx
import json
from Utils import *


# 获得函数的调用图，通过callGraph来将所有有相互调用关系的几点连接起来
class CallGraph:
    fileList = []

    def __init__(self, fileList):
        self.fileList = fileList

    def file2CallGraph(self):
        G = nx.DiGraph()
        for path in self.fileList:
            with open(path, mode="rt", encoding="utf-8") as file:
                lines = file.readlines()
                # 第一行为头文件
                header = lines[0]
                pjson = json.loads(header)
                # 文件的相关信息
                fileName = pjson["fileName"]
                Version = pjson["version"]
                # 后面的为文件下面所有的函数
                methodbody = lines[1:]
                G = self.addNode(G, fileName, Version, methodbody)
        return G

    def addNode(self, G, fileNmae, Version, methodbody):
        fileNodeName = fileNmae + "_" + Version
        # 文件节点的属性还没有添加
        for method in methodbody:
            methodjson = json.loads(method)
            methodNodeName = methodjson["methodName"]
            connection = {"connecting": "include"}
            # fileNode->methodNode :relation:include
            G.add_edge(fileNodeName, methodNodeName,**{"connecting": "include"})
            if methodjson["callMethodNameReferTo"] != "":
                # TODO 添加函数中某一结点调用外部函数的结点
                callMethodNameReferToDic = methodjson["callMethodNameReferTo"]
                for nodeindex in callMethodNameReferToDic.keys():
                    methodNodeName =methodjson["fileName"]+"-"+ methodjson["methodName"]
                    # TODO 被调用函数结点的名字，可能存在逻辑bug
                    calledMethodNodeName =callMethodNameReferToDic[nodeindex]
                    connection = {"connecting": "call"}
                    G.add_edge(methodNodeName, calledMethodNodeName, **{"connecting": "call"})
        return G


if __name__ == '__main__':
    # 测试函数的功能
    low_version = "H:\GraphSimWeb\jsondata\s0.9.22"
    high_version = "H:\GraphSimWeb\jsondata\sV1.1"
    base_file_list = []
    target_file_list = []
    pairfileList = []
    getfilePath(low_version, base_file_list)
    getfilePath(high_version, target_file_list)
    callgraph = CallGraph(base_file_list).file2CallGraph()

    #绘制函数调用图
    pos = nx.circular_layout(callgraph)
    nx.draw_circular(callgraph, with_labels=True)
    nx.draw_networkx_edge_labels(callgraph, pos, font_size=7, alpha=0.5, rotate=True)
    plt.axis('off')
    plt.show()
    #========================
    print("done")
