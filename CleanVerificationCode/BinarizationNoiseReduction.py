from io import BytesIO
from PIL import Image
import copy
import requests
import logging
import base64
import tesserocr


class RecognitionProcess:
    """用于后续进一步可识别处理的方法"""
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


class MainColorNoiseReductionBinary:
    """适用于，主色明显的，降噪并二值化"""

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
        主色与噪色分类，直接过滤噪色
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
        rgb_dict = MainColorNoiseReductionBinary.count_each_rgb(im)
        # print(f"each_total_rgb: {rgb_dict}")
        # 3、删除噪点的rgb数量小于阈值的颜色
        valid_rgb_dict = MainColorNoiseReductionBinary.remove_noise(rgb_dict, select_rgb_num, _min, _max)
        logging.info(f"The code need to identify rgb is {valid_rgb_dict}")
        # 4、二值化：对保留下来的颜色改为黑色，其余颜色统一改为白色
        im = MainColorNoiseReductionBinary.black_or_white(im, valid_rgb_dict)
        return im


class TurnGrayNoiseReductionBinary:

    @staticmethod
    def sum_rim(img, xy_list):
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
    def sum_9_neighborhood(img, x, y):
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
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x, y + 1), (x + 1, y), (x + 1, y + 1)])
                return 4 - sum_rim
            elif x == width - 1:  # 右上顶点, 4邻域
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x, y + 1), (x - 1, y), (x - 1, y + 1)])
                return 4 - sum_rim
            else:  # 最上非顶点,6邻域
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y), (x + 1, y + 1)])
                return 6 - sum_rim
        elif y == height - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x + 1, y), (x + 1, y - 1), (x, y - 1)])
                return 4 - sum_rim
            elif x == width - 1:  # 右下顶点
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x, y - 1), (x - 1, y), (x - 1, y - 1)])
                return 4 - sum_rim
            else:  # 最下非顶点,6邻域
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x - 1, y), (x + 1, y), (x, y - 1), (x - 1, y - 1), (x + 1, y - 1)])
                return 6 - sum_rim
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)])
                return 6 - sum_rim
            elif x == width - 1:  # 右边非顶点
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1)])
                return 6 - sum_rim
            else:  # 具备9领域条件的
                sum_rim = cur_pixel + TurnGrayNoiseReductionBinary.sum_rim(img, [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)])
                return 9 - sum_rim

    @staticmethod
    def collect_noise_point(img, n):
        """
        收集所有的噪点，噪点周边黑点个数小于n的即为噪点
        :param img: Image对象
        :param n: 周围的哪几个点进行对比
        :return: 噪点的所有坐标集合
        """
        noise_point_list = []
        for x in range(img.width):
            for y in range(img.height):
                res_9 = TurnGrayNoiseReductionBinary.sum_9_neighborhood(img, x, y)
                # 找到孤立点，黑点周围的黑点个数在0~n
                if (0 < res_9 < n) and img.getpixel((x, y)) == 0:
                    noise_point_list.append((x, y))
        return noise_point_list

    @staticmethod
    def remove_noise_pixel(img, noise_point_list):
        """
        根据噪点的位置信息，消除二值图片的黑点噪声，置白
        :param img: Image对象
        :param noise_point_list:  噪点坐标位置
        :return:
        """
        for item in noise_point_list:
            img.putpixel((item[0], item[1]), 1)
        return img

    @staticmethod
    def turn_img_to_gray_and_binary(im, threshold):
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
        binary_im = TurnGrayNoiseReductionBinary.turn_img_to_gray_and_binary(im, threshold)
        # 3、找孤立的噪点
        noise_point_list = TurnGrayNoiseReductionBinary.collect_noise_point(binary_im, num)
        # 4、去除噪点
        im = TurnGrayNoiseReductionBinary.remove_noise_pixel(binary_im, noise_point_list)
        return im


class ActualCase:
    Headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36"
    }

    def case3(self):
        """验证码为主色提取， 字母数字"""
        url = "aHR0cDovL2NyZWRpdC5jdXN0b21zLmdvdi5jbi9jY3Bwc2VydmVyL3ZlcmlmeUNvZGUvY3JlYXRvcg=="
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        im = Image.open(BytesIO(resp.content))
        for num in [6, 7, 8, 9, 11, 12]:
            im.seek(num)
            byte_io = BytesIO()
            im.save(byte_io, format="PNG")
            # im = Image.open(BytesIO(resp.content))
            # im.show()
            # 去噪、二值化后的图片
            jpg_im = MainColorNoiseReductionBinary.clean_image(byte_io.getvalue(), (10, 0, 90, 34), 2, 500, 200)
            jpg_im.show()
            # print(num, ">>>>", tesserocr.image_to_text(jpg_im))

    def case2(self):
        """验证码为主色提取，四字成语"""
        url = "aHR0cDovL3h4Z2suc2h6ei5temouc2guZ292LmNuL0NvZGVTZXJ2bGV0"
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        # im = Image.open(BytesIO(resp.content))
        # im.show()
        # 去噪、二值化后的图片
        im = MainColorNoiseReductionBinary.clean_image(resp.content, (35, 11, 162, 37), 5, 0, 27)
        im.show()
        # print(tesserocr.image_to_text(im))

    def case1(self):
        url = "aHR0cDovL3dlaXhpbi5jY29weXJpZ2h0LmNvbS9tZW1iZXJhcGkvbG9naW4vdmFsaWRhdGVJbWc="
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        # im = Image.open(BytesIO(resp.content))
        # im.show()
        # 去噪、二值化后的图片
        im = TurnGrayNoiseReductionBinary.clean_image(resp.content, (7, 5, 60, 32), 130, 5)
        im.show()
        # print(tesserocr.image_to_text(im))


if __name__ == '__main__':
    _object = ActualCase()
    _object.case1()
