from io import BytesIO
from PIL import Image
import copy
import requests
import logging
import base64


class CleanIdiomsCode:

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
    def remove_noise(rgb_dict, threshold) -> dict:
        """
        删除噪点的相关rgb
        :param rgb_dict: rgb对应总量字典
        :param threshold: rgb数量的阈值，小于该阈值的会被删除
        :return: 关键的所需要的rgb
        """
        valid_rgb_dict = copy.deepcopy(rgb_dict)
        for key in rgb_dict:
            if rgb_dict[key] < threshold:
                del valid_rgb_dict[key]
        if (255, 255, 255) in valid_rgb_dict:
            del valid_rgb_dict[(255, 255, 255)]
        if (0, 0, 0) in valid_rgb_dict:
            del valid_rgb_dict[(0, 0, 0)]
        return valid_rgb_dict

    @staticmethod
    def count_each_rgb(im) -> dict:
        """
        统计每个颜色对应RGB的总量
        :param im: Image对象
        :return: 如这样的格式 {(107, 12, 82): 225, (18, 102, 83): 199, ........}
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
        return rgb_dict

    @staticmethod
    def clean_image(binary, crop_size=(), threshold=27):
        """
        对图片进行降噪并二值化，适用于每个字符颜色统一的情况，且背景颜色与主颜色几乎无相同
        :param binary: 图片二进制流
        :param crop_size: 可对图片进行裁剪，如：(35, 11, 162, 37)
        :param threshold: rgb数量的阈值，过滤小于阈值的rgb色彩, 如： 100
        :return: 降噪二值化后的Image对象
        """
        # 1、初始化Image对象,可选择性裁剪
        im = Image.open(BytesIO(binary))
        if crop_size:
            im = im.crop(crop_size)
        # 2、统计每个颜色对应rgb数量
        rgb_dict = CleanIdiomsCode.count_each_rgb(im)
        # 3、删除噪点的rgb数量小于阈值的颜色
        valid_rgb_dict = CleanIdiomsCode.remove_noise(rgb_dict, threshold)
        logging.info(f"The code need to identify rgb is {valid_rgb_dict}")
        # 4、二值化：对保留下来的颜色改为黑色，其余颜色统一改为白色
        im = CleanIdiomsCode.black_or_white(im, valid_rgb_dict)
        return im

    def main(self):
        url = "aHR0cDovL3h4Z2suc2h6ei5temouc2guZ292LmNuL0NvZGVTZXJ2bGV0"
        url = base64.b64decode(url).decode("utf-8")
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;"
                      "q=0.9,image/webp,image/apng,*/*;q=0.8,applicati"
                      "on/signed-exchange;v=b3;q=0.9",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe"
                          "bKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.169"
                          " Safari/537.36",
        }
        resp = requests.get(url, headers=headers)
        # 去噪、二值化后的图片
        im = self.clean_image(resp.content, (35, 11, 162, 37), 27)
        im.show()
        # self.img_binary_to_md5(im)  # 图片二进制流转MD5


if __name__ == '__main__':
    _object = CleanIdiomsCode()
    _object.main()
