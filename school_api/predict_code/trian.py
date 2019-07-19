from tensorflow.keras import models, layers, utils, losses, optimizers
import numpy as np
import string


def load_data(cpath):
    a = np.load(cpath)
    cdata = a['data']
    clabel = a['label']
    return cdata, clabel


def network():
    # 模型建立
    # 两层3x3窗口的卷积(卷积核数为32和64)，一层最大池化(MaxPooling2D)
    # 再Dropout(随机屏蔽部分神经元)并一维化(Flatten)到128个单元的全连接层(Dense)，最后Dropout输出到36个单元的全连接层（全部字符为36个）
    model = models.Sequential()
    model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPool2D(pool_size=(2, 2)))
    model.add(layers.Dropout(0.25))  # 随机屏蔽部分神经元
    model.add(layers.Flatten())  # 一维化
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(num_classes, activation='softmax'))

    # 模型编译
    model.compile(loss=losses.categorical_crossentropy,
                  optimizer=optimizers.Adadelta(),
                  metrics=['accuracy'])
    return model


def train_network(model, save_path, *data):
    # 模型训练
    model.fit(data[0], data[1],
              batch_size=128,
              epochs=12,
              verbose=1,
              validation_data=(data[2], data[3]))

    model.save(save_path)  # 保存模型


if __name__ == '__main__':
    path = 'train_pictures/data_label.npz'
    CHRS = string.ascii_lowercase + string.digits  # 小写字母+数字
    num_classes = len(CHRS)  # 分类数
    input_shape = (13, 22, 1)

    X, Y = load_data(path)
    Y = utils.to_categorical(Y, num_classes)  # 对Y进行one-hot编码
    X = X.reshape(X.shape[0], *input_shape)
    # 简单的切分出训练集和测试集
    split_point = len(Y) - 500
    x_train, y_train, x_test, y_test = X[:split_point], Y[:split_point], X[split_point:], Y[split_point:]

    model = network()
    train_network(model, 'verification_code_model.h5', x_train, y_train, x_test, y_test)
