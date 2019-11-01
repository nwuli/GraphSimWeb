# -*- coding: utf-8 -*-
import os
import json
import pprint
from Neo4j.DataToNeo4j import *

os.chdir("H:\GraphSimWeb\jsondata\s0.9.22")


def data_extraction():
    callMethodList = dict()
    Version = None

    for r, d, f_list in os.walk(os.getcwd()):
        for cur_file in f_list:
            if cur_file[-4:] == ".txt":
                fileName = os.path.join(r, cur_file)

                with open(fileName, encoding="utf-8") as f:
                    _ = f.readlines()
                    print("\nfileName is : {0}\n".format(fileName))

                    for line in _[1:]:
                        user_dict = json.loads(line.strip())

                        print("method is : {0}".format(user_dict["methodName"]))
                        #普通的结点
                        node_label = ["node"]
                        create_data = DataToNeo4j(node_label)
                        create_data.create_node(user_dict["attribute"], nodeType="node")  # 传入attribute列表
                        create_data.create_relationship(user_dict["succs"])

                        method_root_name = user_dict["methodName"] + "-ROOT"
                        # create_data.create_node([{"NodeClass": method_root_name}])
                        node_label=["method"]
                        create_data=DataToNeo4j(node_label)
                        create_data.create_node([method_root_name], nodeType="method")
                        start_node = [[0]] if user_dict["succs"] else []
                        create_data.create_relationship(start_node, method_root_name, ROOT=True)
                        # 保存函数调用
                        callMethod = user_dict["callMethodNameReferTo"]
                        if callMethod:
                            for start_index in callMethod.keys():
                                start = (user_dict["fileName"], user_dict["methodName"], int(start_index))

                                callMethodList[start] = callMethod[start_index]

                    # 创建当前文件根节点，及与其包含函数根节点的连线
                    user_dict = json.loads(_[0].strip())

                    node_label = ["file"]
                    create_data = DataToNeo4j(node_label)

                    file_root_name = user_dict["fileName"] + "-ROOT"
                    # create_data.create_node([{"NodeClass": file_root_name}])
                    create_data.create_node([file_root_name], nodeType="file")
                    method_root_name = [temp + "-ROOT" for temp in user_dict["hasMethodName"]]
                    create_data.create_file_method_relationship(file_root_name, method_root_name)

                    if not Version:
                        Version = user_dict["version"]

    # 所有文件的节点都创建完了，开始连接函数调用的边
    # 形式：
    # before: {(文件名，函数名，节点索引):{文件名：函数名，文件名：函数名, ...}, ...}
    # now {(文件名，函数名（包含参数），节点索引)：文件名-函数名（包含参数），....}
    print("\nThe function call relationship is as follows:\n")
    pprint.pprint(callMethodList)
    DataToNeo4j([]).create_out_file_relationship(Version, callMethodList)


def process():
    label = ("CWE190_Integer_Overflow__int_Environment_preinc_81a.java",
             "CWE190_Integer_Overflow__int_Environment_preinc_81a.java-main")
    # properties = {id:18, name:"Expression Stmt "}

    node_passed, all_id, all_labels = DataToNeo4j([]).dfs(label, properties)
    print(node_passed)
    print(all_id)
    print(all_labels)


def main():
    data_extraction()


if __name__ == "__main__":
    main()
