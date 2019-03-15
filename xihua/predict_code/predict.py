# -*- coding: utf-8 -*-

import string
from keras.models import load_model
import config
import numpy as np


class CodePredicting(object):

    def img_denoising(self, image_stream):
        split_lines = [5, 17, 29, 41, 53]  # 验证码纵向切分的位置
        y_min, y_max = 1, 23  # 验证码横向切分的位置

        image = image_stream.convert('L')  # 转化为灰度图像
        ims = [image.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]  # 验证码切分成四个数字
        for i in range(4):
            # 验证码去噪
            rows, cols = ims[i].size
            for r in range(1, rows - 1):
                for l in range(1, cols - 1):
                    num = 0
                    pixel = ims[i].getpixel((r, l))
                    if pixel != 255:
                        if ims[i].getpixel((r, l - 1)) == 255:
                            num += 1
                        if ims[i].getpixel((r - 1, l)) == 255:
                            num += 1
                        if ims[i].getpixel((r, l + 1)) == 255:
                            num += 1
                        if ims[i].getpixel((r + 1, l)) == 255:
                            num += 1
                        if num >= 3 or ims[i].getpixel((r, l)) >= 128:
                            ims[i].putpixel((r, l), 255)
                        elif ims[i].getpixel((r, l)) < 128:
                            ims[i].putpixel((r, l), 0)
            ims[i] = ims[i].convert('1')  # 转化为二值图像

        return ims

    # 图片预测函数
    def img_pridict(self, ims, model_path=config.MODEL_PATH):
        name = []
        CHRS = string.ascii_lowercase + string.digits  # 小写字母+数字

        model = load_model(model_path)
        for i in range(4):
            test_input = 1.0 * np.array(ims[i])  # 图片转化为矩阵
            test_input = test_input.reshape(1, *(12, 22, 1))  # reshape多出来一个1因为预测的时候只有一个样本
            y_probs = model.predict(test_input)  # 模型预测, y_probs的形状为(1, 36)
            name.append(CHRS[y_probs[0].argmax(axis=0)])

        return ''.join(name)  # name列表中元素, 拼接在一起, 中间用''隔开
