from keras import backend as K

# 字符列表
letters = "012345678abcdefghijklmnpqrstuvwxy"

# 输入图片的尺寸
img_rows, img_cols = 12, 23

def get_input_shape():
    # 根据keras的后端是TensorFlow还是Theano转换输入形式
    if K.image_data_format() == 'channels_first':
        input_shape = (1, img_rows, img_cols)
    else:
        input_shape = (img_rows, img_cols, 1)
    print("input shape: ", input_shape)
    return input_shape
