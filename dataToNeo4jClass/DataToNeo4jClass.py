# -*- coding: utf-8 -*-
from py2neo import Node, Graph, Relationship


class DataToNeo4j(object):
    """extract excel data to import into neo4j"""

    def __init__(self):
        """create link to neo4j database"""
        link = Graph("http://127.0.0.1:7474", username="neo4j", password="123456")
        self.graph = link
        # 定义label
        self.job_node = 'job_node'
        self.data_node = 'data_node'
        #self.graph.delete_all()

    def create_node(self, node_list_key, node_list_value):
        """create node"""
        for name in node_list_key:
            name_node = Node(self.job_node, name=name)
            self.graph.create(name_node)
        print("create job node:", len(node_list_key))

        for name in node_list_value:
            value_node = Node(self.data_node, name=name)
            self.graph.create(value_node)
        print("create data node: ", len(node_list_value))



    def create_relation(self, df_data):
        """create relation"""
        print("start to create relation... ")
        m = 0
        for m in range(0, len(df_data)):
            try:
                #print(df_data['name'][m], df_data['name2'][m])
                rel = Relationship(self.graph.find_one(label=self.job_node, property_key='name', property_value=df_data['name'][m]),
                                   df_data['relation'][m], self.graph.find_one(label=self.data_node, property_key='name',
                                   property_value=df_data['name2'][m]))
                self.graph.create(rel)
            except AttributeError as e:
                print(e, m)
        print("create relation: ", m)
        print("create completed.")

