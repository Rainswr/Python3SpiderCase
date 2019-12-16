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
from fontTools.ttLib import TTFont
import requests
import re


def get_font_content(self):
    """
    获取woff字体文件
    :return:
    """
    r = requests.get('https://maoyan.com/board/1', headers=self.headers)
    woff_path = re.search(r"vfile(.*?)woff", r.text).group()
    woff_url = f"https://{woff_path}"
    return requests.get(woff_url, headers=self.headers).content


def save_font() -> None:
    """
    存woff字体文件
    :return:
    """
    for i in range(10):
        font_content = get_font_content()
        with open(f'..\\CatFilmCrawl\\font\\{i + 1}.woff', 'wb') as f:
            f.write(font_content)


def get_xy_info(font, cli):
    """
    形成KNN的目标值、特征值数据集
    :param font:
    :param cli:
    :return:
    """
    glyf_uni = font.getGlyphOrder()[2:]
    info = list()
    for i, g in enumerate(glyf_uni):
        coors = font['glyf'][g].coordinates
        coors = [x_y for xy in coors for x_y in xy]  # 一个uni的xy坐标
        coors.insert(0, cli[i])  # [true1,x,y,x,y,x,y,...]
        info.append(coors)  # [[true1,x,y,...], [true2,x,y,...],...]
    return info


def get_font_data() -> list:
    """
    合并数据集和测试数据集
    :return:
    """
    # List[List[List[int]]]
    font_1 = TTFont('..\\CatFilmCrawl\\font\\1.woff')
    cli_1 = [8, 6, 7, 4, 2, 1, 0, 5, 9, 3]
    xy_1 = get_xy_info(font_1, cli_1)

    font_2 = TTFont('..\\CatFilmCrawl\\font\\2.woff')
    cli_2 = [2, 6, 1, 9, 4, 0, 3, 5, 7, 8]
    xy_2 = get_xy_info(font_2, cli_2)

    font_3 = TTFont('..\\CatFilmCrawl\\font\\3.woff')
    cli_3 = [4, 8, 2, 3, 7, 5, 6, 9, 0, 1]
    xy_3 = get_xy_info(font_3, cli_3)

    font_4 = TTFont('..\\CatFilmCrawl\\font\\4.woff')
    cli_4 = [9, 0, 7, 5, 4, 6, 8, 1, 3, 2]
    xy_4 = get_xy_info(font_4, cli_4)

    font_5 = TTFont('..\\CatFilmCrawl\\font\\5.woff')
    cli_5 = [4, 3, 6, 5, 1, 7, 8, 9, 2, 0]
    xy_5 = get_xy_info(font_5, cli_5)

    font_6 = TTFont('..\\CatFilmCrawl\\font\\6.woff')
    cli_6 = [3, 6, 5, 8, 4, 9, 7, 1, 2, 0]
    xy_6 = get_xy_info(font_6, cli_6)

    font_7 = TTFont('..\\CatFilmCrawl\\font\\7.woff')
    cli_7 = [2, 6, 4, 5, 7, 1, 9, 0, 3, 8]
    xy_7 = get_xy_info(font_7, cli_7)

    font_8 = TTFont('..\\CatFilmCrawl\\font\\8.woff')
    cli_8 = [0, 6, 2, 5, 9, 7, 8, 4, 3, 1]
    xy_8 = get_xy_info(font_8, cli_8)

    font_9 = TTFont('..\\CatFilmCrawl\\font\\9.woff')
    cli_9 = [0, 1, 6, 2, 3, 4, 5, 9, 8, 7]
    xy_9 = get_xy_info(font_9, cli_9)

    font_10 = TTFont('..\\CatFilmCrawl\\font\\10.woff')
    cli_10 = [7, 2, 4, 5, 0, 1, 6, 8, 9, 3]
    xy_10 = get_xy_info(font_10, cli_10)
    # [[true1,x,y,...], [true2,x,y,...],...]
    info = xy_1 + xy_2 + xy_3 + xy_4 + xy_5 + xy_6 + xy_7 + xy_8 + xy_9 + xy_10
    return info


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
    x = data.drop([0], axis=1)
    y = data[0]
    # 分割数据集
    x_train = x.head(100)   # 训练集的特征值
    y_train = y.head(100)
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
