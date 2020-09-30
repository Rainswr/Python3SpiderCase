"""
@author/github: Shirmay1
@software: PyCharm
@file: Pretreatment_MainColorRgb.py
@time: 2020/8/22 0022 上午 9:17
@function:  对图片验证码降噪、二值化，适用于提取字段颜色与背景颜色完全相同的验证码
"""
import copy
from PIL import Image
from io import BytesIO


class MainColorRgb:

    @staticmethod
    def black_or_white(im, valid_rgb_dict):
        """
        对图片进行二值化处理
        :param im: Image
        :param valid_rgb_dict: 已保留的有效rgb
        :return: 二值化后的Image对象
        """
        im = im.convert('RGB')
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                rgb = im.getpixel((x, y))
                if rgb in valid_rgb_dict:
                    im.putpixel((x, y), (0, 0, 0))
                else:
                    im.putpixel((x, y), (255, 255, 255))
        return im

    @staticmethod
    def remove_noise(rgb_dict, select_rgb_num=0, _min=0, _max=0) -> dict:
        """
        删除噪点的相关rgb
        :param rgb_dict: rgb对应总量字典
        :param select_rgb_num: 筛选哪几个rgb要保留
        :param _min: rgb数量的阈值，大于该阈值的会被删除
        :param _max: rgb数量的阈值，小于该阈值的会被删除
        :return: 关键的所需要的rgb
        """
        valid_rgb_dict = copy.deepcopy(rgb_dict)
        new_rgb_dict = copy.deepcopy(rgb_dict)
        if select_rgb_num:
            valid_rgb_dict = copy.deepcopy(dict(sorted(
                rgb_dict.items(), key=lambda xx: xx[1], reverse=True
            )[:select_rgb_num]))
            new_rgb_dict = copy.deepcopy(valid_rgb_dict)
        for key in new_rgb_dict:
            if _max:
                if new_rgb_dict[key] < _max:
                    del valid_rgb_dict[key]
            if _min:
                if new_rgb_dict[key] > _min:
                    del valid_rgb_dict[key]
        return valid_rgb_dict

    @staticmethod
    def count_each_rgb(im) -> dict:
        """
        统计每个颜色对应RGB的总量
        :param im: Image对象
        :return: 如这样的格式{(241, 244, 215): 868, (108, 128, 142): 356 ......}
        """
        im = im.convert('RGB')
        rgb_dict = {}
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                rgb = im.getpixel((x, y))
                if rgb in rgb_dict:
                    rgb_dict[rgb] += 1
                else:
                    rgb_dict[rgb] = 0
        rgb_list = sorted(rgb_dict.items(), key=lambda xx: xx[1], reverse=True)
        resp_rgb_dict = {item[0]: item[1] for item in rgb_list}
        if (255, 255, 255) in resp_rgb_dict:
            del resp_rgb_dict[(255, 255, 255)]
        if (0, 0, 0) in resp_rgb_dict:
            del resp_rgb_dict[(0, 0, 0)]
        return resp_rgb_dict

    @staticmethod
    def clean_image(binary, crop_size=(), select_rgb_num=0, _min=0, _max=0):
        """
        主色与噪色分类，直接过滤噪色
        对图片进行降噪并二值化，适用于每个字符颜色统一的情况，且背景颜色与主颜色完全无相同
        以下脚本有部分是调试查看结果的，#注释的日志部分和im.show()可以用来看结果
        :param binary: 图片二进制流
        :param crop_size: 可对图片进行裁剪，如：(35, 11, 162, 37)
        :param select_rgb_num: 筛选哪几个rgb要保留
        :param _min: rgb数量的阈值，大于该阈值的会被删除
        :param _max: rgb数量的阈值，小于该阈值的会被删除
        :return: 降噪二值化后的Image对象
        """
        # import logging
        # logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.DEBUG)
        """1、初始化Image对象,可选择性裁剪"""
        im = Image.open(BytesIO(binary))
        # im.show()
        if crop_size:
            im = im.crop(crop_size)
        """2、统计每个颜色对应rgb数量"""
        rgb_dict = MainColorRgb.count_each_rgb(im)
        # logging.info(f"each_total_rgb of image is: {rgb_dict}")
        """3、删除噪点的rgb数量小于阈值的颜色"""
        valid_rgb_dict = MainColorRgb.remove_noise(
            rgb_dict, select_rgb_num, _min, _max)
        # logging.info(f"The code need to identify rgb is {valid_rgb_dict}")
        """4、二值化：对保留下来的颜色改为黑色，其余颜色统一改为白色"""
        im = MainColorRgb.black_or_white(im, valid_rgb_dict)
        # im.show()
        return im


# if __name__ == '__main__':
#     # 实际案例
#     import base64
#     import requests
#     url = "aHR0cDovL3h4Z2suc2h6ei5temouc2guZ292LmNuL0NvZGVTZXJ2bGV0"
#     url = base64.b64decode(url).decode("utf-8")
#     resp = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36"})
#     # 去噪、二值化后的图片
#     image = MainColorRgb.clean_image(resp.content, (35, 11, 162, 37), 5, 0, 27)
#     image.show()
