from grakel import Graph
from grakel import GraphKernel
import networkx as nx
from Utils import *
from grakel import graph_from_networkx
if __name__ == '__main__':
    low_version = "H:\GraphSimWeb\jsondata\s0.9.22"
    high_version = "H:\GraphSimWeb\jsondata\s0.9.23"
    base_file_list = []
    target_file_list = []
    pairfileList=[]
    #getfilePath(low_version,base_file_list)
    #getfilePath(high_version,target_file_list)
    extractFile(low_version,base_file_list)
    extractFile(high_version,target_file_list)
    PairMethodGraph=getpairMethodGraph(base_file_list,target_file_list)
    #当存在多个文件对匹配的情况，文件数目会缺失。
    SIm=getMethodSim(PairMethodGraph)
    print("kernal_Done!")


