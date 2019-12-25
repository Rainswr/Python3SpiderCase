"""
@author/github: Shirmay1
@software: PyCharm
@file: TrainFont.py
@time: 2019/12/26 0026 上午 1:01
@function: 用于KNN算法的本地woff字体集
@url: 
"""

from fontTools.ttLib import TTFont
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)AppleWebKi"
                  "t/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari"
                  "/537.36 "}


def get_font_content():
    """
    获取woff字体文件
    :return:
    """
    r = requests.get('https://maoyan.com/board/1', headers=headers)
    woff_path = re.search(r"vfile(.*?)woff", r.text).group()
    woff_url = f"https://{woff_path}"
    return requests.get(woff_url, headers=headers).content


def save_font() -> None:
    """
    存woff字体文件
    :return:
    """
    for i in range(10):
        font_content = get_font_content()
        with open(f'..\\GoodRent\\font\\{i + 1}.woff', 'wb') as f:
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
    font_1 = TTFont('..\\GoodRent\\font\\1.woff')
    cli_1 = [2, 9, 4, 3, 6, 7, 5, 8, 1, 0]
    xy_1 = get_xy_info(font_1, cli_1)

    font_2 = TTFont('..\\GoodRent\\font\\2.woff')
    cli_2 = [8, 5, 3, 7, 0, 4, 2, 9, 6, 1]
    xy_2 = get_xy_info(font_2, cli_2)

    font_3 = TTFont('..\\GoodRent\\font\\3.woff')
    cli_3 = [9, 4, 5, 2, 7, 1, 3, 8, 6, 0]
    xy_3 = get_xy_info(font_3, cli_3)

    font_4 = TTFont('..\\GoodRent\\font\\4.woff')
    cli_4 = [5, 0, 2, 1, 4, 8, 6, 3, 7, 9]
    xy_4 = get_xy_info(font_4, cli_4)

    font_5 = TTFont('..\\GoodRent\\font\\5.woff')
    cli_5 = [2, 9, 4, 3, 6, 7, 5, 8, 1, 0]
    xy_5 = get_xy_info(font_5, cli_5)

    font_6 = TTFont('..\\GoodRent\\font\\6.woff')
    cli_6 = [5, 0, 2, 1, 4, 8, 6, 3, 7, 9]
    xy_6 = get_xy_info(font_6, cli_6)

    font_7 = TTFont('..\\GoodRent\\font\\7.woff')
    cli_7 = [7, 8, 6, 9, 0, 1, 2, 5, 4, 3]
    xy_7 = get_xy_info(font_7, cli_7)

    font_8 = TTFont('..\\GoodRent\\font\\8.woff')
    cli_8 = [9, 4, 5, 2, 7, 1, 3, 8, 6, 0]
    xy_8 = get_xy_info(font_8, cli_8)

    font_9 = TTFont('..\\GoodRent\\font\\9.woff')
    cli_9 = [8, 5, 3, 7, 0, 4, 2, 9, 6, 1]
    xy_9 = get_xy_info(font_9, cli_9)

    font_10 = TTFont('..\\GoodRent\\font\\10.woff')
    cli_10 = [4, 8, 1, 7, 5, 0, 9, 2, 3, 6]
    xy_10 = get_xy_info(font_10, cli_10)
    # [[true1,x,y,...], [true2,x,y,...],...]
    info = xy_1 + xy_2 + xy_3 + xy_4 + xy_5 + xy_6 + xy_7 + xy_8 + xy_9 + xy_10
    return info


# print(get_font_data())
