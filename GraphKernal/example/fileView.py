from grakel import Graph
from grakel import GraphKernel
import networkx as nx
from Utils import *
from numpy import array
from grakel import graph_from_networkx
from View import *
if __name__ == '__main__':
    low_version = "F:\GraphSim\jsondata\V1.0"
    high_version = "F:\GraphSim\jsondata\V1.1"
    base_file_list = []
    target_file_list = []
    pairfileList=[]
    getfilePath(low_version,base_file_list)
    getfilePath(high_version,target_file_list)

    pairfileList=getpairFile(base_file_list,target_file_list)
    for pair in pairfileList:
        basefile=pair[0]
        targetfile=pair[1]
        g1=ParseFile(basefile)
        g2=ParseFile(targetfile)
        #basefileGraph、targetfileGraph分别为待比较结点得图
        _basefileGraph=g1.connectFile()
        _targetfileGraph=g2.connectFile()
        showView(_basefileGraph,_targetfileGraph)

