import keras
import glob
import numpy as np
from random import shuffle
from PIL import Image

from captcha.common import  *

# 读入数据，按80,20的比例划分训练与测试数据
# 返回4个张量：训练数据，训练标记，测试数据，测试标记
def get_image(folder=r"..\train_pictures\train"):
    input_shape = get_input_shape()

    X = []
    print("load images...")
    for f in glob.glob(folder + r"\*"):  # 遍历当前目录下所有png后缀的图片
        c = letters.index(f[-1]) # 将字符转换为相应的0-32数值
        for sf in glob.glob(f + r"\*"):
            im = Image.open(sf).convert('1')
            t = 1.0 * np.array(im)
            t = t.reshape(*input_shape)  # reshape后要赋值
            X.append({"x":t, "t":c})  # 验证码像素列表

    # 打乱次序
    shuffle(X)
    # 再得到数据和标记
    imgs,labels = [],[]
    for xx in X:
        imgs.append(xx["x"])
        labels.append(xx["t"])

    # 进行one-hot编码
    labels = keras.utils.to_categorical(labels, len(letters))
    # 按80,20的比例划分训练与测试数据
    tc = int(len(imgs) * 0.8)
    train_imgs = imgs[:tc]
    train_labels = labels[:tc]
    test_imgs = imgs[tc:]
    test_labels = labels[tc:]

    # X = np.stack(X) # 将列表转换为矩阵
    return np.stack(imgs), np.stack(labels), \
           np.stack(train_imgs), np.stack(train_labels), \
           np.stack(test_imgs), np.stack(test_labels)
