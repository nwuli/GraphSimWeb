# -*- coding: utf-8 -*-

from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

class DataToNeo4j(object):
    '''将数据存入neo4j'''

    def __init__(self, node_label):
        '''建立连接'''
        link = Graph("http://localhost:7474", user="neo4j", password="1814")
        self.graph = link
        self.node_label = node_label # List
        self.index = 0
        # self.graph.delete_all()


    def create_node(self, node_list):
        '''建立节点'''
        try:
            for attribute in node_list:
                name_node = Node(*self.node_label, id=self.index, **attribute)
                self.graph.create(name_node)
                self.index += 1
        except AttributeError as e:
            print(e)


    def create_relationship(self, relation_ship, *attr, ROOT=False, edge_type="succ"):
        '''建立边，一个函数内节点间的边'''
        index = 0
        try:
            # print("relation_ship is: {0}".format(relation_ship))
            for relation in relation_ship:
                # print("relation is: {0}".foramat(relation))
                if ROOT:
                    node_start = self.graph.nodes.match(*self.node_label, NodeClass=attr).first()
                else:
                    node_start = self.graph.nodes.match(*self.node_label, id=index).first()
                for id in relation:
                    node_end = self.graph.nodes.match(*self.node_label, id=id).first()

                    edge = Relationship(node_start, edge_type, node_end)
                    self.graph.create(edge)
                index += 1
        except AttributeError as e:
            print(e, index, ROOT)

    def create_file_method_relationship(self, file_root, method_root, edge_type="hasMethod"):
        '''建立文件ROOT与其所有函数ROOT间的边'''
        try:
            node_start = self.graph.nodes.match(*self.node_label, NodeClass=file_root).first()
            for method in method_root:
                node_end = self.graph.nodes.match(*self.node_label, NodeClass=method).first()

                edge = Relationship(node_start, edge_type, node_end)
                self.graph.create(edge)
        except AttributeError as e:
            print(e)

    def create_out_file_relationship(self, Version, callMethodList, edge_type="call"):
        '''建立函数调用的边'''
        for _ in callMethodList.items():
            start_file_name, start_method_name, start_node_index = _[0]
            start_label = [Version, start_file_name, start_file_name + "-" + start_method_name]

            try:
                node_start = self.graph.nodes.match(*start_label, id=start_node_index).first()

                for end_file_name, end_method_name in _[1].items():
                    end_label = [Version, end_file_name, end_file_name + "-" + end_method_name]

                    node_end = self.graph.nodes.match(*end_label, NodeClass=end_method_name + "-ROOT").first()
                    edge = Relationship(node_start, edge_type, node_end)
                    self.graph.create(edge)
            except AttributeError as e:
                print(e)


    def find_diff_nodes(self, ):
        '''找出两个哪个图之间不同的节点'''
        pass

    def dfs(self, *label, **properties):
        '''
        Version 1：dfs 直到没有边为止  doing
                    有边相连就遍历，除非遍历到函数-ROOT节点，此时不再往上遍历
        Version 2：dfs 遍历时候添加条件判断
        '''
        matcher = NodeMatcher(self.graph)
        rel_matcher = RelationshipMatcher(self.graph)

        node = matcher.match(*label, **properties)
        node_passed = before = list(node)
        after = list()

        while before:
            # 每次进入循环，向外再遍历一层（层次遍历）
            for now_node in before:
                rels = rel_matcher.match({now_node})
                for rel in rels:
                    start, end = rel.nodes
                    # 此处后面添加，对节点的判断（如到函数根节点时停，节点属性进行判断操作）
                    if start not in node_passed and start.get("NodeClass")[-9:] != "java-ROOT":
                        after.append(start)
                        node_passed.append(start)
                    if end not in node_passed:
                        after.append(end)
                        node_passed.append(end)

            before = after
            after = list()

        # 使用字典保存所有出现的标签
        all_labels = list()
        for _ in node_passed:
            if all_labels:
                temp = sorted(_.labels)
                if temp not in all_labels:
                    all_labels.append(temp)
            else:
                all_labels.append(sorted(_.labels))

        # test
        all_id = set()
        for _ in node_passed:
            all_id.add(_.get("id"))

        return node_passed, sorted(all_id), all_labels