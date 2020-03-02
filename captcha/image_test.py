#!/usr/bin/env python
# coding: utf-8
# image 读入测试
from PIL import Image
import numpy as np

sf = r"../train_pictures/train/0/1.png"
im = Image.open(sf).convert('1')
t = 1.0 * np.array(im)
print(t)
# 结果如下：
# [[1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 0. 0. 0. 0. 1. 1. 1. 1. 1.]
#  [1. 0. 0. 0. 0. 0. 0. 0. 1. 1. 1. 1.]
#  [1. 1. 0. 1. 1. 1. 1. 0. 0. 1. 1. 1.]
#  [1. 0. 0. 1. 1. 1. 1. 0. 0. 1. 1. 1.]
#  [1. 0. 0. 1. 1. 1. 1. 0. 0. 1. 1. 1.]
#  [1. 0. 0. 1. 1. 1. 1. 1. 0. 0. 1. 1.]
#  [1. 0. 0. 1. 1. 1. 1. 1. 0. 1. 1. 1.]
#  [1. 0. 0. 1. 1. 1. 1. 1. 0. 0. 1. 1.]
#  [1. 0. 0. 1. 1. 1. 1. 1. 0. 1. 1. 1.]
#  [1. 0. 0. 1. 1. 1. 1. 1. 0. 0. 1. 1.]
#  [1. 1. 0. 1. 1. 1. 1. 1. 0. 1. 1. 1.]
#  [1. 1. 0. 0. 1. 1. 1. 1. 0. 1. 1. 1.]
#  [1. 1. 0. 0. 0. 0. 0. 0. 0. 0. 1. 1.]
#  [1. 1. 1. 0. 0. 0. 0. 0. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 0. 0. 0. 1. 1. 1. 1. 1.]
#  [0. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]]

sf = r"../train_pictures/source/0a13.png"
im = Image.open(sf).convert('1')
im = im.crop([5, 0, 17, 23])
t = 1.0 * np.array(im)
print("从验证码中分离出的0")
print(t)
# 从验证码中分离出的0
# [[1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 0. 0. 0. 0. 0. 1. 1. 1. 1. 1.]
#  [1. 0. 0. 0. 0. 0. 0. 0. 1. 1. 1. 1.]
#  [1. 0. 0. 0. 1. 0. 0. 0. 0. 1. 1. 1.]
#  [0. 0. 0. 1. 1. 1. 0. 0. 0. 1. 1. 1.]
#  [0. 0. 0. 1. 1. 1. 0. 0. 0. 0. 1. 1.]
#  [0. 0. 0. 1. 1. 1. 1. 0. 0. 0. 1. 1.]
#  [0. 0. 0. 1. 1. 1. 1. 0. 0. 0. 0. 1.]
#  [1. 0. 0. 0. 1. 1. 1. 0. 0. 0. 1. 1.]
#  [1. 0. 0. 0. 1. 1. 1. 1. 0. 0. 0. 1.]
#  [1. 0. 0. 0. 1. 1. 1. 1. 0. 0. 0. 1.]
#  [1. 0. 0. 0. 0. 1. 1. 1. 0. 0. 0. 1.]
#  [1. 1. 0. 0. 0. 1. 1. 1. 0. 0. 0. 1.]
#  [1. 1. 0. 0. 0. 0. 0. 0. 0. 0. 1. 1.]
#  [1. 1. 1. 0. 0. 0. 0. 0. 0. 0. 1. 1.]
#  [1. 1. 1. 1. 0. 0. 0. 0. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 0. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 0.]
#  [1. 0. 1. 0. 1. 1. 1. 1. 1. 1. 1. 1.]]
