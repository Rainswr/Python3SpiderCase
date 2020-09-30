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


# print(get_font_data())
