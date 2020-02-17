import keras
import requests
import io
import glob
import random
import numpy as np
from PIL import Image
import tensorflow as tf
from captcha.common import *
import base64

graph = tf.get_default_graph()
# graph = tf.compat.v1.get_default_graph
# keras模型应用于flask app时会报bug !!
# 以下链接可以解决问题
# https://github.com/fchollet/keras/issues/2397

class predict:
    def __init__(self):
        # self.model = keras.models.load_model(r'./captcha/model.h5')
        self.model = keras.models.load_model(r'./model.h5')

    def get_image_from_url(self,url="http://jwxt.njupt.edu.cn/CheckCode.aspx"):
        '''
        从教务处网站获取验证码
        '''
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        }
        res = requests.get(url, headers=headers)
        image_file = io.BytesIO(res.content)
        self.image = Image.open(image_file)
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
        # im = image.point(lambda i: i != 43, mode='1')
        im = image.convert('1')
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

    def verify_image(self, image):
        images = self.handle_split_image(image)
        code = self.predict(images)
        print("code=", code)
        return code

    def verify_base64(self, b64):
        '''
        验证base64编码的图像，返回识别得到的验证码
        :param base64: base64编码的图像
        :return: 识别得到的验证码
        '''
        bs = base64.b64decode(b64)
        self.image = Image.open(io.BytesIO(bs))
        # self.show_image()
        images = self.handle_split_image(self.image)
        code = self.predict(images)
        print("code=",code)
        return code

    def verify_url(self,url="http://jwxt.njupt.edu.cn/CheckCode.aspx"):
        '''
        获取网络上的图像，并识别
        :param url: 图像url
        :return: base64编码的图像, 识别得到的验证码
        '''
        image = self.get_image_from_url(url)
        images = self.handle_split_image(image)
        code = self.predict(images)
        print("code = ", code)
        return self.base64, code

    def verify_local(self):
        '''
        随机获取本地图像，并识别
        :return: 识别得到的验证码
        '''
        image = self.get_image_from_local()
        images = self.handle_split_image(image)
        code = self.predict(images)
        print("code = ", code)
        return code

    def show_image(self):
        import matplotlib.pyplot as plt
        plt.imshow(self.image)
        plt.show()

if __name__ == '__main__':
    p = predict()
    p.verify_local()
    # p.verify_url()
    p.show_image()
    # for i in range(1,5):
    #     p.test()