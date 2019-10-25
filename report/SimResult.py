import numpy as np
from Utils import *
from Graph import *
class SimResult:
    sim={}
    #误差值
    eps=0.1
    diff=[]
    #传入像版本的代码的图
    def __init__(self,sim):
        #文件名存的是base的文件名
        self.sim=sim
    def PareFileResult(self):
        #遍历文件对
        for file in self.sim:
            # 文件键值不为空,则两个版本下，文件均存在
            if self.sim[file]!="":
                dic=self.sim[file]
                for methodDictkey in self.sim[file].keys():
                    #传入所在的文件名+两个对应的函数对的相似度
                    self.PareMethodResult(file,methodDictkey,dic)



            else:
                #存在文件残缺对,直接扫描扫描文件即可
                self.diff.append(file)
        return self.diff

    def PareMethodResult(self,file,methodDictkey,dic):
        # 比较的两个函数对
        methodTupeKey = methodDictkey
        # 函数的相似度
        methodTupeValue = dic[methodDictkey]

        #只要元组键值缺少元素，则认为是函数发生了增删操作
        if methodTupeKey[0]=='' or methodTupeKey[1]=='':
            methName=methodTupeKey[0] if methodTupeKey[0] else methodTupeKey[1]

            self.diff.append(file+"&"+methName)

        #只是函数的内容发生了变化
        else:
            s=methodTupeValue[0][0]
            if np.allclose(s,1.0,self.eps):
                #0.1的误差范围内，则认为是相似的，没有发生变化
                print("相似函数")

            else:

                #发生了变化，需要根据程度进行判断，分析相关的部分
                self.diff.append(file+"&"+methodTupeKey[1])
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
    sim=SimResult(SIm)
    diff=sim.PareFileResult()
    print("done!")


