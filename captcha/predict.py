import keras
import requests
import io
import glob
import random
import numpy as np
from PIL import Image
import tensorflow as tf
from captcha.common import *

graph = tf.get_default_graph()
# graph = tf.compat.v1.get_default_graph
# keras模型应用于flask app时会报bug !!
# 以下链接可以解决问题
# https://github.com/fchollet/keras/issues/2397

class predict:
    def __init__(self, from_url = False, tobase64=False):
        self.from_url = from_url
        self.tobase64 = tobase64
        # self.model = keras.models.load_model(r'./captcha/model.h5')
        self.model = keras.models.load_model(r'./model.h5')
        print("init predict")

    def get_image(self):
        if self.from_url:
            return self.get_image_from_url()
        else:
            return self.get_image_from_local()

    def get_image_from_url(self):
        '''
        从教务处网站获取验证码
        '''
        url = "http://jwxt.njupt.edu.cn/CheckCode.aspx"
        self.fn = url
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        }
        res = requests.get(url, headers=headers)
        image_file = io.BytesIO(res.content)
        self.image = Image.open(image_file)
        if self.tobase64:
            import base64
            self.base64 = str(base64.b64encode(io.BytesIO(res.content).read()), "utf-8")
        return self.image

    def get_image_from_local(self):
        # 从本地随机获取验证码
        fs = glob.glob(r"..\train_pictures\source\*")
        self.fn = random.sample(fs, 1)[0]

        self.image = Image.open(self.fn)
        return self.image

    def handle_split_image(self, image):
        '''
        切割验证码，返回包含四个字符图像的列表
        '''
        im = image.point(lambda i: i != 43, mode='1')
        y_min, y_max = 0, 23  # im.height - 1 # 26
        split_lines = [5, 17, 29, 41, 53]
        ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
        # w = w.crop(w.getbbox()) # 切掉白边 # 暂不需要
        return ims

    def predict(self, images):
        '''
        使用模型对四个字符的列表对应的验证码进行预测
        '''
        input_shape = get_input_shape()
        Y = []
        for i in range(4):
            im = images[i]
            test_input = np.concatenate(np.array(im))
            test_input = test_input.reshape(1, *input_shape)
            y_probs = None
            with graph.as_default():
                y_probs = self.model.predict(test_input)
            Y.append(letters[y_probs[0].argmax(-1)])
        return ''.join(Y)

    def test(self):
        image = self.get_image()
        images = self.handle_split_image(image)
        code = self.predict(images)
        if self.from_url:
            import matplotlib.pyplot as plt
            plt.imshow(self.image)
            plt.show()
        else:
            print("get image file: ", self.fn)
        print("code = ", code)

if __name__ == '__main__':
    p = predict(True, True)
    p.test()
    # for i in range(1,5):
    #     p.test()