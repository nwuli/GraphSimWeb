import numpy as np
from Utils import *
from Graph import *


class SimResult:
    sim = {}
    # 误差值
    eps = 0.1
    # 通过简单比较得到相似性改变的函数
    normaldiff = []
    # 文件或者函数的删除
    deletediff = []
    # 文件或者函数的增加
    adddiff = []
    # 关联分析得到的改变的函数
    connectdiff = []
    # 没有匹配的函数，文件中的内容全部被重写
    nomatch = []

    # 传入sim值进行分析
    def __init__(self, sim):
        # 文件名存的是base的文件名
        self.sim = sim

    def PareFileResult(self):
        # 遍历文件对
        for file in self.sim:
            if self.sim[file] != "":
                dic = self.sim[file]
                for methodDictkey in self.sim[file].keys():
                    # 人为标记"sim"字段
                    if methodDictkey == 'sim':
                        if dic["sim"] == '0.0':
                            # 无匹配,函数均发生变化
                            self.nomatch.append(file.replace(".txt", ""))
                        elif dic["sim"] == "-1.0":
                            # sim="-1.0"删除
                            self.deletediff.append(file.replace(".txt", ""))
                        elif dic["sim"] == "2.0":
                            # 增加文件
                            self.adddiff.append(file.replace(".txt", ""))
                        else:
                            # 接口文件，没有函数，不需要扫描
                            pass


                    # 传入所在的文件名 + 两个对应的函数对的相似度
                    else:
                        self.PareMethodResult(file, methodDictkey, dic)
            else:
                # TODO 存在文件残缺对,直接扫描扫描文件即可,无法分清函数的增加还是删除，这部分不会执行，上面使用change进行标注，已经解决了。
                # self.normaldiff.append(file.replace(".txt", ""))
                print("是否进入")
                pass
        return self.normaldiff, self.connectdiff, self.deletediff, self.adddiff, self.nomatch

    def PareMethodResult(self, file, methodDictkey, dic):
        # 比较的两个函数对
        methodTupeKey = methodDictkey
        # 函数的相似度
        # TODO 这里得拆分可能有问题[文件全名_版本号]
        candiate_filename1 = methodDictkey[0]
        candiate_filename2 = methodDictkey[1]
        methodTupeValue = dic[methodDictkey]

        # 只要元组键值缺少元素，则认为是函数发生了增删操作
        if methodTupeKey[0] == '' or methodTupeKey[1] == '':
            if methodTupeKey[0] == '':
                self.adddiff.append(file.replace(".txt", "") + "&" + methodTupeKey[1])
            else:
                self.deletediff.append(file.replace(".txt", "") + "&" + methodTupeKey[0])
        # 只是函数的内容发生了变化
        else:
            s = methodTupeValue[0][0]
            if np.allclose(s, 1.0, self.eps):
                # 0.1的误差范围内，则认为是相似的，没有发生变化
                print("相似函数:{name}".format(name=methodTupeKey[1]))
            else:
                # 发生了变化，需要根据程度进行判断，分析相关的部分
                print("发生变化函数：{name}".format(name=file.replace(".txt", "") + "&" + candiate_filename2))
                self.normaldiff.append(file.replace(".txt", "") + "&" + candiate_filename2)
                # 关联分析得到的函数变化
                self.Node2NodeConnect(file, methodTupeKey[1])  # file:url

    def Node2NodeConnect(self, fieUrl, diffmethodName):
        # TODO 新函数的函数调用和旧函数的函数的调用的callreferto信息均需要参考
        with open(fieUrl, 'rt', encoding='utf-8') as file:
            lines = file.readlines()
            methodLines = lines[1:]
            for methodLine in methodLines:
                method = json.loads(methodLine)
                # 该文件下:函数名+版本号
                methodName = method["methodName"] + "_" + method["version"]
                if methodName == diffmethodName:
                    # 找到变化的函数
                    callMethodNameReferT = method["callMethodNameReferTo"]
                    for referFile in callMethodNameReferT.values():
                        # TODO referFile可能需要进行文件名的解析
                        self.connectdiff.append(referFile)
                        print("函数调用文件：{name}".format(name=referFile))


if __name__ == '__main__':
    low_version = "H:\GraphSimWeb\jsondata\s0.9.22"
    high_version = "H:\GraphSimWeb\jsondata\s0.9.23"
    base_file_list = []
    target_file_list = []
    pairfileList = []
    getfilePath(low_version, base_file_list)
    getfilePath(high_version, target_file_list)
    PairMethodGraph = getpairMethodGraph(base_file_list, target_file_list)
    SIm = getMethodSim(PairMethodGraph)
    sim = SimResult(SIm)
    normaldiff, connectdiff, deletediff, adddiff, nomatch = sim.PareFileResult()
    dic = {};
    dic["normaldiff"] = normaldiff
    dic["connectdiff"] = connectdiff
    dic["deletediff"] = deletediff
    dic["adddiff"] = adddiff
    dic["nomatch"] = nomatch
    toText(dic, "./", "result.txt")
    print("done!")
