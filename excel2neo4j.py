# -*- coding: utf-8 -*-
from dataToNeo4jClass.DataToNeo4jClass import DataToNeo4j
import os
import pandas as pd


# extract excel data，and transfer to dateframe
# os.chdir('xxxx')

task_excel_data = pd.read_excel('task_info.xlsx', header=0, encoding='utf8')
print(task_excel_data)


def data_extraction():
    """NODE INFO EXTRACTION"""

    # extract job info to list
    node_list_key = []
    for i in range(0, len(task_excel_data)):
        node_list_key.append(task_excel_data['Job_Name'][i])

    # duplicate removal
    node_list_key = list(set(node_list_key))

    # value抽出作node
    node_list_value = []
    for i in range(0, len(task_excel_data)):
        for n in range(1, len(task_excel_data.columns)):
            # 取出表头名称invoice_data.columns[i]
            node_list_value.append(task_excel_data[task_excel_data.columns[n]][i])
    # duplicate removal
    node_list_value = list(set(node_list_value))
    # change to string type
    node_list_value = [str(i) for i in node_list_value]

    return node_list_key, node_list_value


def relation_extraction():
    """RELATION EXTRACTION"""

    links_dict = {}
    name_list = []
    relation_list = []
    name2_list = []

    for i in range(0, len(task_excel_data)):
        m = 0
        name_node = task_excel_data[task_excel_data.columns[m]][i]
        while m < len(task_excel_data.columns)-1:
            relation_list.append(task_excel_data.columns[m+1])
            name2_list.append(task_excel_data[task_excel_data.columns[m+1]][i])
            name_list.append(name_node)
            m += 1

    # change to string type
    name_list = [str(i) for i in name_list]
    name2_list = [str(i) for i in name2_list]

    # integrate list to dict
    links_dict['name'] = name_list
    links_dict['relation'] = relation_list
    links_dict['name2'] = name2_list
    # chang to DataFrame
    df_data = pd.DataFrame(links_dict)
    return df_data



data_extraction()
relation_extraction()
create_data = DataToNeo4j()

create_data.create_node(data_extraction()[0], data_extraction()[1])
create_data.create_relation(relation_extraction())
