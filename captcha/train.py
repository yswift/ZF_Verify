from captcha.dataset import *

def build_model():
    num_classes = len(letters);
    input_shape = get_input_shape()
    # 以下模型和mnist-cnn相同
    # 两层3x3窗口的卷积(卷积核数为32和64)，一层最大池化(MaxPooling2D)
    # 再Dropout(随机屏蔽部分神经元)并一维化(Flatten)到128个单元的全连接层(Dense)，最后Dropout输出到33个单元的全连接层（全部字符为33个）
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layersDropout(0.25))
    model.add(keras.layersFlatten())
    model.add(keras.layersDense(128, activation='relu'))
    model.add(keras.layersDropout(0.5))
    model.add(keras.layersDense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    return model

def train():
    x_train, t_train, x_test, t_test = get_image()

    model = build_model()
    batch_size = 64
    epochs = 10
    model.fit(x_train, t_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, t_test))
    score = model.evaluate(x_test, t_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    model.save(r'.\model.h5')

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'