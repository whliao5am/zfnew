# -*- coding: utf-8 -*-

import string
from keras.models import load_model
import numpy as np
import cv2


CHRS = string.ascii_lowercase + string.digits  # 小写字母+数字
split_lines = [4, 16, 28, 40, 52]  # 验证码纵向切分的位置
y_min, y_max = 0, 22  # 验证码横向切分的位置
input_shape = (13, 22, 1)


def img_press(image_stream):
    gray_img = cv2.cvtColor(image_stream, cv2.COLOR_BGR2GRAY)  # 灰度化
    ims = [gray_img[y_min:y_max, u:v + 1] for u, v in zip(split_lines[:-1], split_lines[1:])]  # 切分验证码
    return ims


# 图片预测函数
def img_pridict(ims, model_path):
    name = ''

    model = load_model(model_path)
    for i in range(len(ims)):
        test_input = 1.0 * np.array(ims[i])  # 图片转化为矩阵
        test_input = test_input.reshape(1, *input_shape)  # reshape多出来一个1因为预测的时候只有一个样本
        y_probs = model.predict(test_input)  # 模型预测, y_probs的形状为(1, 36)
        name += CHRS[y_probs[0].argmax(axis=0)]
    return name
