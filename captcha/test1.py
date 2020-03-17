import glob
import keras
from captcha.common import  *
from PIL import Image
import numpy as np

input_shape = get_input_shape()

model = keras.models.load_model(r'./model-99.967.h5')

folder = r"..\train_pictures\train"
total_acc = 0
total = 0
for f in glob.glob(folder + r"\*"):  # 遍历当前目录下所有png后缀的图片
    c = f[-1]
    print("验证:", f)
    acc = 0
    tol = 0
    for sf in glob.glob(f + r"\*"):
        im = Image.open(sf).convert('1')
        t = 1.0 * np.array(im)
        t = t.reshape(1,*input_shape)  # reshape后要赋值
        # t = np.stack(t)
        y_probs = model.predict([t])
        y = letters[y_probs[0].argmax(-1)]
        # print(y, end='')
        tol += 1
        if c == y:
            acc += 1
        else:
            print("error: ", y, ",", sf)
    print("\nacc ", acc, "/", tol)
    total_acc += acc
    total += tol

print("total acc ", total_acc, "/", total, (1.0*total_acc/total))

