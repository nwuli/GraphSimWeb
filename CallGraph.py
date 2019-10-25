import networkx as nx
import json
from Utils import *
class CallGraph:
    fileList=[]
    def __init__(self,fileList):
        self.fileList=fileList
    def file2CallGraph(self):
        G=nx.DiGraph()
        for path in self.fileList:
            with open(path,mode="rt",encoding="utf-8") as file:
                lines=file.readlines()
                #第一行为头文件
                header=lines[0]
                pjson=json.load(header)
                #文件的相关信息
                fileName=pjson["fileName"]
                Version=pjson["Version"]
                #后面的为文件下面所有的函数
                methodbody=lines[1:]
                G=self.addNode(G,fileName,Version,methodbody)
        return G
    def addNode(self,G,fileNmae,Version,methodbody):
        fileNodeName=fileNmae+"_"+Version
        #文件节点的属性还没有添加
        for method in methodbody:
            methodjson =json.load(method)
            methodNodeName=methodjson["MethodName"]
            connection={"connecting":"include"}
            #fileNode->methodNode :relation:include
            G.add_edge(fileNodeName,methodNodeName,connection)
            if method["callMethodNameReferTo"]!="":
                # TODO 添加函数中某一结点调用外部函数的结点
                callMethodNameReferToDic=method["callMethodNameReferTo"]
                for nodeindex in callMethodNameReferToDic.keys():
                    methodNodeName=methodjson["MethodName"]
                    # TODO 被调用函数结点的名字，可能存在逻辑bug
                    calledMethodNodeName=callMethodNameReferToDic[nodeindex].split("_")[1]
                    connection={"connecting":"call"}
                    G.add_edge(methodNodeName,calledMethodNodeName,connection)
        return G
        pass

if __name__ == '__main__':
    # 测试函数的功能
    low_version = "F:\GraphSim\jsondata\V1.0"
    high_version = "F:\GraphSim\jsondata\V1.1"
    base_file_list = []
    target_file_list = []
    pairfileList = []
    getfilePath(low_version, base_file_list)
    getfilePath(high_version, target_file_list)
    callgraph = CallGraph(base_file_list).file2CallGraph()






