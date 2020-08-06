from io import BytesIO
from PIL import Image
import copy
import requests
import logging
import base64


class CleanIdiomsCode:

    @staticmethod
    def pixel_matrix_visualization(image_path):
        """像素点矩阵可视化"""
        from matplotlib import image, pyplot
        import numpy
        mat = image.imread(image_path)
        pyplot.matshow(mat)
        pyplot.xticks(numpy.arange(1, 70, 1))
        pyplot.yticks(numpy.arange(1, 34, 1))
        pyplot.grid()
        pyplot.show()

    @staticmethod
    def img_binary_to_md5(im=None, path=None):
        """
        将图片二进制流转换为MD5
        :param im: Image对象
        :param path: 图片存储路径
        :return: MD5值
        """
        from hashlib import md5
        if not im:
            im = Image.open(path)  # path = "E:\image_black_whilte\自命不凡.jpg"
        img_byte = BytesIO()
        im.save(img_byte, format='JPEG')
        return md5(img_byte.getvalue()).hexdigest()

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
        # im.save("image.jpg")
        # im.show()
        # print(pytesseract.image_to_string("image.jpg", lang='chi_sim'))
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
            valid_rgb_dict = copy.deepcopy(dict(sorted(rgb_dict.items(), key=lambda xx: xx[1], reverse=True)[:select_rgb_num]))
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
        对图片进行降噪并二值化，适用于每个字符颜色统一的情况，且背景颜色与主颜色几乎无相同
        :param binary: 图片二进制流
        :param crop_size: 可对图片进行裁剪，如：(35, 11, 162, 37)
        :param select_rgb_num: 筛选哪几个rgb要保留
        :param _min: rgb数量的阈值，大于该阈值的会被删除
        :param _max: rgb数量的阈值，小于该阈值的会被删除
        :return: 降噪二值化后的Image对象
        """
        # 1、初始化Image对象,可选择性裁剪
        im = Image.open(BytesIO(binary))
        if crop_size:
            im = im.crop(crop_size)
        # 2、统计每个颜色对应rgb数量
        rgb_dict = CleanIdiomsCode.count_each_rgb(im)
        # 3、删除噪点的rgb数量小于阈值的颜色
        valid_rgb_dict = CleanIdiomsCode.remove_noise(rgb_dict, select_rgb_num, _min, _max)
        logging.info(f"The code need to identify rgb is {valid_rgb_dict}")
        # 4、二值化：对保留下来的颜色改为黑色，其余颜色统一改为白色
        im = CleanIdiomsCode.black_or_white(im, valid_rgb_dict)
        return im

    Headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36"
    }

    def main2(self):
        url = "aHR0cDovL2NyZWRpdC5jdXN0b21zLmdvdi5jbi9jY3Bwc2VydmVyL3ZlcmlmeUNvZGUvY3JlYXRvcg=="
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        im = Image.open(BytesIO(resp.content))
        for num in [6, 7, 8, 9, 11, 12]:
            im.seek(num)
            byte_io = BytesIO()
            im.save(byte_io, format="PNG")
            # 去噪、二值化后的图片
            jpg_im = self.clean_image(byte_io.getvalue(), (10, 0, 90, 34), 2, 500, 200)
            jpg_im.show()
            # import tesserocr
            # print(num, ">>>>", tesserocr.image_to_text(jpg_im))

    def main(self):
        url = "aHR0cDovL3h4Z2suc2h6ei5temouc2guZ292LmNuL0NvZGVTZXJ2bGV0"
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        # 去噪、二值化后的图片
        im = self.clean_image(resp.content, (35, 11, 162, 37), 5, 0, 27)
        im.show()
        # import tesserocr
        # print(tesserocr.image_to_text(im))
        # self.img_binary_to_md5(im)  # 图片二进制流转MD5


if __name__ == '__main__':
    _object = CleanIdiomsCode()
    _object.main()
