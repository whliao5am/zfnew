import os
import numpy as np
import cv2
import string


def process(path):
    # 处理一个目录的图片，并返回处理后的图片数据和相应标签数据
    cdata = []
    clabel = []
    for file_name in os.listdir(path):
        if file_name[-3:] != 'png':
            continue
        img = cv2.imread(path + file_name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化
        ims = [img[y_min:y_max, u:v+1] for u, v in zip(split_lines[:-1], split_lines[1:])]  # 切分验证码
        cdata = np.concatenate((cdata, ims), axis=0) if cdata != [] else ims  # shape = (x, 22, 13)
        for i in file_name[:4]:
            clabel.append(CHRS.index(i))
    return cdata, clabel


if __name__ == '__main__':
    split_lines = [4, 16, 28, 40, 52]  # 验证码纵向切分的位置
    y_min, y_max = 0, 22  # 验证码横向切分的位置

    height = 27
    width = 72

    old_code_path = 'train_pictures/old_code/'
    new_code_path = 'train_pictures/new_code/'

    CHRS = string.ascii_lowercase + string.digits  # 小写字母+数字

    data_1, label_1 = process(old_code_path)
    data_2, label_2 = process(new_code_path)

    data = np.concatenate((data_1, data_2), axis=0)  # shape = (9060, 22, 13)
    data = data / 255  # [0, 255] 转为 [0, 1]
    label = np.array(label_1 + label_2)  # shape = (9060, )
    np.savez('train_pictures/data_label.npz', data=data, label=label)  # 保存数据
    print('save done...')
