# -*- encoding: utf-8 -*-
"""
@author/github: Shirmay1
@software: PyCharm
@file: CatFilmCrawl.py
@time: 2019/12/17 23:16
@function: 猫眼电影字体反爬
@url: https://maoyan.com/board/1
"""

import requests
import re
from fontTools.ttLib import TTFont
from CatFilmCrawl.KNNAlgorithm import get_true_value
from bs4 import BeautifulSoup


class CatFilmFont:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0"
                          ".3359.139 Safari/537.36 "}

    def save_font(self, woff_url) -> None:
        """
        存woff字体文件
        :return:
        """
        font_content = requests.get(woff_url, headers=self.headers).content
        with open(f'..\\CatFilmCrawl\\font\\web.woff', 'wb') as f:
            f.write(font_content)

    @staticmethod
    def get_xy_info(web_font) -> list:
        """
        获取uni字的xy坐标列表
        :param web_font:
        :return:
        """
        glyf_uni = web_font.getGlyphOrder()[2:]
        info = list()
        for i, g in enumerate(glyf_uni):
            coors = web_font['glyf'][g].coordinates
            coors = [x_y for xy in coors for x_y in xy]  # 一个uni的xy坐标
            coors.insert(0, None)  # [None,x,y,x,y,x,y,...]
            info.append(coors)  # [[true1,x,y,...], [true2,x,y,...],...]
        return info

    def get_uni_num(self, woff_url: str):
        """
        返回加密字体映射{'&#f3ad': 3, '&#ec25': 5, ...}
        :param woff_url: woff文件的url
        :return:
        """
        uni_dict = {}
        self.save_font(woff_url)
        web_font = TTFont('..\\CatFilmCrawl\\font\\web.woff')
        web_xy = self.get_xy_info(web_font)
        true_font = get_true_value(web_xy)
        for index, uni in enumerate(web_font.getGlyphOrder()[2:]):
            web_font = uni.replace("uni", r"&#x").lower() + ";"
            uni_dict[web_font] = str(int(true_font[index]))
        return uni_dict

    @staticmethod
    def parse_fields(text: str):
        """
        解析字体
        :param text:
        :return:
        """
        soup = BeautifulSoup(text, 'lxml')
        dd_tags = soup.select('.board-wrapper dd')
        for dd in dd_tags:
            film_dict = {
                'film_name': dd.find('a')['title'],
                'realtime': dd.select('.realtime')[0].get_text().replace(
                    ' ', '').replace('\n', ''),
                "total_boxoffice": dd.select(
                    '.total-boxoffice')[0].get_text().replace(
                    ' ', '').replace('\n', ''),
                "star": dd.select(".star")[0].get_text(),
                "releasetime": dd.select(".releasetime")[0].get_text(),
            }
            print(film_dict)

    def process(self):
        """
        :return:
        """
        r = requests.get('https://maoyan.com/board/1', headers=self.headers)
        woff_path = re.search(r"vfile(.*?)woff", r.text).group()
        woff_url = f"https://{woff_path}"
        # 获取加密字真实值
        uni_dict = self.get_uni_num(woff_url)
        text = r.text
        # 替换加密字为真实值
        for key in uni_dict:
            text = text.replace(key, uni_dict[key])
        # 解析字段
        self.parse_fields(text)


if __name__ == '__main__':
    _object = CatFilmFont()
    _object.process()
