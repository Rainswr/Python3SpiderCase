# -*- encoding: utf-8 -*-
"""
@author/github: Shirmay1
@software: PyCharm
@file: KNNAlgorithm.py
@time: 2019/12/17 0:33
@function: KNN算法
@url:
"""

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from TrainFont import get_font_data


def get_true_value(gusess_info):
    """
    根据已有的数据集预测，KNN算法
    :param gusess_info:
    :return:
    """
    p_info = get_font_data() + gusess_info
    # 处理缺失值
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    data = pd.DataFrame(imputer.fit_transform(pd.DataFrame(p_info)))  
    # 取出特征值\目标值
    x = data.drop([0], axis=1)   # 删除第一列，只留剩余的特征值
    y = data[0]  #   # 获取第一列，即真实值
    # 分割数据集
    x_train = x.head(100)   # 训练集的前100行对应的特征值
    y_train = y.head(100)   # 训练集的前100行特征值对应的每行真实值
    x_test = x.tail(10)    # 测试集的特征值
    # 进行算法流程
    knn = KNeighborsClassifier(n_neighbors=1)
    # 开始训练
    knn.fit(x_train, y_train)
    # 预测结果
    y_predict = knn.predict(x_test)
    return y_predict


# if __name__ == '__main__':
#     g_info = [[true1,x,y,...], [true2,x,y,...],...]
#     print(get_true_value(g_info))
