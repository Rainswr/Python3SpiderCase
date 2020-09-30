"""
@author/github: Shirmay1
@software: PyCharm
@file: KnnIdentifyVerification.py
@time: 2020/8/29
@function: KNN训练模型识别验证码
"""

from io import BytesIO
import numpy as np
from hashlib import md5
from PIL import Image
import joblib
from sklearn.neighbors import KNeighborsClassifier
import os
import random


class RecognitionProcess:

    @staticmethod
    def img_binary_to_md5(im=None, path=None, img_format='JPEG'):
        """
        将图片二进制流转换为MD5
        :param im: Image对象
        :param path: 图片存储路径
        :param img_format: 图片是JPEG还是PNG
        :return: MD5值
        """
        if not im:
            im = Image.open(path)  # path = "E:\image_black_whilte\自命不凡.jpg"
        img_byte = BytesIO()
        im.save(img_byte, format=img_format)
        return md5(img_byte.getvalue()).hexdigest()

    @staticmethod
    def save_crop_image_to_son_dir(origin_image_dir, crop_xy, height):
        """
        切割图片, 并将图片存储到不同子文件夹, 每张图片名称即图片识别值
        :param origin_image_dir: 存图片的文件夹如: r"E:\Image\case3"
        :param crop_xy: 切割xy对应坐标: [(5, 20), (20, 35), (35, 50), (50, 65)]
        :param height: 图片高度
        :return: 存储分割图片的文件夹路径
        """
        parent_crop_dir = f"{origin_image_dir}_crop"
        os.mkdir(parent_crop_dir)
        for image_name in os.listdir(origin_image_dir):
            image_path = os.path.join(origin_image_dir, image_name)
            im = Image.open(image_path)
            for index, xx in enumerate(crop_xy):
                new_im = im.crop((xx[0], 0, xx[1], height))
                crop_dir_name = image_name[index]
                son_crop_dir = os.path.join(parent_crop_dir, crop_dir_name)
                if crop_dir_name not in os.listdir(parent_crop_dir):
                    os.mkdir(son_crop_dir)
                crop_im_path = os.path.join(son_crop_dir, f"{crop_dir_name}_{int(random.random() * 1000)}.png")
                new_im.save(crop_im_path)
        return parent_crop_dir

    @staticmethod
    def knn_model_train(character: list, value: list, model_save_path: str):
        """
        knn模型训练
        注意: character列表的子列表长度一致,且每个子列表与value列表值一一对应
        :param character: 特征值如: [[1, 2, 2, 3], [1, 2, 2, 3], [1, 2, 2, 3]]
        :param value: 特征值对应的真实值如: [8, 3, 0]
        :param model_save_path: 训练好的模型保存路径如: "captcha_num.model"
        :return:  训练好的模型路径
        """
        array_character = np.asarray(character)
        array_value = np.asarray(value)
        knn = KNeighborsClassifier()
        knn.fit(array_character, array_value)
        joblib.dump(knn, model_save_path)
        return model_save_path

    @staticmethod
    def extracted_features(im=None, path=None):
        """
        提取图片特征值
        :param im: Image对象
        :param path: 图片路径
        :return: 特征值列表single_character_array
        """
        if not im:
            im = Image.open(path)
        pix = np.asarray(im)
        single_character_array = pix.reshape(pix.size)
        return single_character_array

    @staticmethod
    def predict_image_value(character: list, model_path: str):
        """
        预测图片结果
        :param character: 特征值list如: [[1, 2, 2, 3]]
        :param model_path: 选择已经训练好的模型
        :return: 预测结果
        """
        array_character = np.asarray(character)
        predict_result = joblib.load(model_path).predict(array_character)
        return predict_result

    @staticmethod
    def save_crop_image_to_dir(origin_image_dir, crop_xy):
        """
        切割图片, 并将分割图片另存到一个文件夹, 每张图片名称即图片识别值
        :param origin_image_dir: 存图片的文件夹如: r"E:\Image\case3"
        :param crop_xy: 切割xy对应坐标: [(5, 20), (20, 35), (35, 50), (50, 65)]
        :return: 存储分割图片文件夹的路径
        """
        parent_crop_dir = f"{origin_image_dir}_crop_sum"
        if not os.path.exists(parent_crop_dir):
            os.mkdir(parent_crop_dir)
        for image_name in os.listdir(origin_image_dir):
            image_path = os.path.join(origin_image_dir, image_name)
            im = Image.open(image_path)
            for index, xx in enumerate(crop_xy):
                new_im = im.crop((xx[0], 0, xx[1], im.size[1]))
                crop_im_name = image_name[index]
                crop_im_path = os.path.join(parent_crop_dir, f"{crop_im_name}_{int(random.random() * 10000)}.jpg")
                new_im.save(crop_im_path)
        return parent_crop_dir

    @staticmethod
    def process_knn_model_train(origin_image_dir, crop_xy, model_path):
        """
        验证码训练模型
        :param origin_image_dir: 存放已标记好的验证码: "E:\Image\case3"
        :param crop_xy: 切割xy对应坐标: [(5, 20), (20, 35), (35, 50), (50, 65)]
        :param model_path: 存储模型的路径
        :return:
        """
        # 1` 切割字符,并存到另一个文件夹
        crop_dir = RecognitionProcess.save_crop_image_to_dir(origin_image_dir, crop_xy)
        # 2` 提取特征值
        character_list, value_list = [], []
        for crop_str in os.listdir(crop_dir):
            crop_str_path = os.path.join(crop_dir, crop_str)
            c_arr = RecognitionProcess.extracted_features(None, crop_str_path)
            character_list.append(c_arr)
            value_list.append(crop_str[0])
        # 3` 训练模型
        RecognitionProcess.knn_model_train(character_list, value_list, model_path)

    @staticmethod
    def process_identify_image(model_path, pr_im=None, path=None, crop_x=None):
        """
        识别图片验证码
        :param model_path: 训练好的模型
        :param pr_im: 待识别的图片对应Image
        :param path: 或者待识别的图片路径
        :param crop_x: 整张图片分割xy坐标
        :return: 识别结果
        """
        if not pr_im:
            pr_im = Image.open(path)
        if pr_im:
            c_list = []
            for index, xx in enumerate(crop_x):
                new_im = pr_im.crop((xx[0], 0, xx[1], pr_im.size[1]))
                _arr = RecognitionProcess.extracted_features(new_im)
                c_list.append(_arr)
            predict_result = RecognitionProcess.predict_image_value(c_list, model_path)
            return "".join(predict_result)


# if __name__ == '__main__':
#     # 1` 训练模型
#     RecognitionProcess.process_knn_model_train(r"E:\Image\case3", [(5, 20), (20, 35), (35, 50), (50, 65)], "case.model")
#     # 2` 识别验证码
#     result = RecognitionProcess.process_identify_image("case.model", None, "E:\Test_com\Captaca\code.png", [(5, 20), (20, 35), (35, 50), (50, 65)])
#     print(result)
