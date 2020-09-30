"""
@author/github: Shirmay1
@software: PyCharm
@file: Pretreatment_TurnGrayField.py
@time: 2020/8/22 0022 上午 9:33
@function:  9领域法,以一点为中心, 即数字九宫格键,去除周边黑点小于阈值的噪点
"""

from PIL import Image
from io import BytesIO


class TurnGrayField:

    @staticmethod
    def field_xy_gather(x: int, y: int, index: int) -> list:
        """
        该点周围选择的领域坐标点
        :param x: x坐标
        :param y: y坐标
        :param index: 对应的索引
        :return: 领域坐标列表
        """
        xy_gather = [
            [(x, y + 1), (x + 1, y), (x + 1, y + 1)],
            [(x, y + 1), (x - 1, y), (x - 1, y + 1)],
            [(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y), (x + 1, y + 1)],
            [(x + 1, y), (x + 1, y - 1), (x, y - 1)],
            [(x, y - 1), (x - 1, y), (x - 1, y - 1)],
            [(x - 1, y), (x + 1, y), (x, y - 1), (x - 1, y - 1), (x + 1, y - 1)],
            [(x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)],
            [(x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1)],
            [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        ]
        return xy_gather[index]

    @staticmethod
    def sum_rim(img, xy_list: list) -> int:
        """
        统计所传坐标白点的个数
        :param img:  Image对象
        :param xy_list: 周边坐标
        :return: 白点个数之和
        """
        sum_rim = 0
        for xy in xy_list:
            sum_rim += img.getpixel(xy)
        return sum_rim

    @staticmethod
    def sum_9_neighborhood(img, x: int, y: int) -> int:
        """
        9邻域框,以当前点为中心的字框,统计所传坐标点周围黑点的个数
        :param x: x的坐标
        :param y: y的坐标
        :param img: Image对象
        :return: 所传坐标点周围黑点的个数
        """
        cur_pixel = img.getpixel((x, y))  # 当前像素点的值
        width = img.width
        height = img.height
        if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
            return 0
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点, 4邻域
                # 中心点旁边3个点
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 0))
                return 4 - sum_rim
            elif x == width - 1:  # 右上顶点, 4邻域
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 1))
                return 4 - sum_rim
            else:  # 最上非顶点,6邻域
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 2))
                return 6 - sum_rim
        elif y == height - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 3))
                return 4 - sum_rim
            elif x == width - 1:  # 右下顶点
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 4))
                return 4 - sum_rim
            else:  # 最下非顶点,6邻域
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 5))
                return 6 - sum_rim
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 6))
                return 6 - sum_rim
            elif x == width - 1:  # 右边非顶点
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 7))
                return 6 - sum_rim
            else:  # 具备9领域条件的
                sum_rim = cur_pixel + TurnGrayField.sum_rim(
                    img, TurnGrayField.field_xy_gather(x, y, 8))
                return 9 - sum_rim

    @staticmethod
    def collect_noise_point(img, n: int) -> list:
        """
        收集所有的噪点，噪点周边黑点个数小于n的即为噪点
        :param img: Image对象
        :param n: 黑点个数的阈值, 小于该阈值被判为噪点
        :return: 噪点的所有坐标集合
        """
        noise_point_list = []
        for x in range(img.width):
            for y in range(img.height):
                res_9 = TurnGrayField.sum_9_neighborhood(img, x, y)
                # 找到孤立点，黑点周围的黑点个数在如果小于n, 则判断为噪点
                if (0 < res_9 < n) and img.getpixel((x, y)) == 0:
                    noise_point_list.append((x, y))
        return noise_point_list

    @staticmethod
    def remove_noise_pixel(img, noise_point_list: list):
        """
        根据噪点的位置信息，消除二值图片的黑点噪声，置白
        :param img: Image对象
        :param noise_point_list:  噪点坐标位置
        :return:
        """
        for x_y in noise_point_list:
            img.putpixel((x_y[0], x_y[1]), 1)
        return img

    @staticmethod
    def turn_img_to_gray_and_binary(im, threshold: int):
        """
        获取灰度转二值的映射table,0表示黑色,1表示白色
        :param im: Image对象
        :param threshold:  必须先转化灰度，再指定二值化阈
        :return:
        """
        im_gray = im.convert('L')  # 转灰度
        table = []
        for i in range(256):
            table.append(0) if i < threshold else table.append(1)
        im_gray = im_gray.point(table, '1')
        return im_gray

    @staticmethod
    def clean_image(binary, crop_size=(), threshold=120, num=6):
        """
        二值化转灰度后的图片，再去噪点
        :param binary: 图片二进制流
        :param crop_size: 可对图片进行裁剪，如：(35, 11, 162, 37)
        :param threshold: 转灰度二值化阈值，控制二值化程度，自行调整（不能超过256）
        :param num: 九宫格法去除像素点周围点的数量（推荐6和7）
        :return:
        """
        # 1、初始化Image对象,可选择性裁剪
        im = Image.open(BytesIO(binary))
        if crop_size:
            im = im.crop(crop_size)
        # 2、转灰度并二值化
        binary_im = TurnGrayField.turn_img_to_gray_and_binary(im, threshold)
        # 3、找孤立的噪点
        noise_point_list = TurnGrayField.collect_noise_point(binary_im, num)
        # 4、去除噪点
        im = TurnGrayField.remove_noise_pixel(binary_im, noise_point_list)
        return im


# if __name__ == '__main__':
#     # 实际案例
#     import base64
#     import requests
#     url = "aHR0cDovL3dlaXhpbi5jY29weXJpZ2h0LmNvbS9tZW1iZXJhcGkvbG9naW4vdmFsaWRhdGVJbWc="
#     url = base64.b64decode(url).decode("utf-8")
#     resp = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36"})
#     # 去噪、二值化后的图片
#     image = TurnGrayField.clean_image(resp.content, (7, 5, 60, 32), 130, 5)
#     image.show()
#     import tesserocr
#     print(tesserocr.image_to_text(image))
