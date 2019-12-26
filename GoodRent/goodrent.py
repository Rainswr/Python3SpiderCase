"""
@author/github: Shirmay1
@software: PyCharm
@file: goodrent.py
@time: 2019/12/25 23:23
@function: 好租字体反爬
@url: https://www.haozu.com/bj/house454280/
"""
import requests
import re
from fontTools.ttLib import TTFont
from GoodRent.KNNAlgorithm import get_true_value
from bs4 import BeautifulSoup
import base64


class GoodRentFont:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0"
                          ".3359.139 Safari/537.36 ",
            "Host": "www.haozu.com",
            "Referer": "https://www.haozu.com/safe_verif_view/?token=8uEJnsi"
                       "mq6AFW9Fve&refer=https://www.haozu.com/bj/house454280/"
            }

    @staticmethod
    def save_font(font_content) -> None:
        """
        存woff/ttf字体文件
        :return:
        """
        with open(f'..\\GoodRent\\font\\web.woff', 'wb') as f:
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

    def get_uni_num(self, woff_content):
        """
        返回加密字体映射{'&#f3ad': 3, '&#ec25': 5, ...}
        :param woff_content: woff加密字体
        :return:
        """
        uni_dict = {}
        self.save_font(woff_content)
        web_font = TTFont('..\\GoodRent\\font\\web.woff')
        web_xy = self.get_xy_info(web_font)
        true_font = get_true_value(web_xy)
        for index, uni in enumerate(web_font.getGlyphOrder()[2:]):
            web_font = uni.replace("uni", r"&#x").lower() + ";"
            uni_dict[web_font] = str(int(true_font[index]))
        return uni_dict

    @staticmethod
    def parse_fields(text: str):
        """
        解析内容，可以修改
        :param text:
        :return:
        """
        soup = BeautifulSoup(text, 'lxml')
        li_tags = soup.select(".listCon .clearfix")
        for li in li_tags:
            title = li.select(".h1-title")[0].find('a')['title']
            brief = li.find('p').get_text().replace(
                "\n", '').replace(' ', '').split('/')
            price = li.select(".list-price")[0].get_text().replace(
                "\n", '').replace(' ', '').replace("收藏", "").replace(
                "月", "月，")
            rent_data = {
                "house": brief[0],
                "price": price,
                "area": brief[1] if len(brief) > 1 else '',
                "degree": brief[2] if len(brief) == 3 else '',
                "title": title,
            }
            print(rent_data)

    def flow(self, resp, woff_content):
        """
        主流程
        :param resp:
        :param woff_content:
        :return:
        """
        # 获取加密字真实值
        uni_dict = self.get_uni_num(woff_content)
        text = resp.text
        # 替换加密字为真实值
        for key in uni_dict:
            text = text.replace(key, uni_dict[key])
        # 解析字段
        self.parse_fields(text)

    def process(self):
        """
        入口 ，可以修改
        :return:
        """
        detail_url = 'https://www.haozu.com/bj/house-list/?' \
                     'ca_s=sem_baidu&ca_q=pinzhuan&cid=biaoti&ca_i=hz_ad'
        r = requests.get(
            detail_url, headers=self.headers)
        woff_font = re.search(r'base64,(.*?)\)', r.text).group(1)
        woff_content = base64.b64decode(woff_font)
        self.flow(r, woff_content)


if __name__ == '__main__':
    _object = GoodRentFont()
    _object.process()
