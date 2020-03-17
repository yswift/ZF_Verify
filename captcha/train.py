# import keras
from captcha.dataset import *
# import tensorflow.keras as keras

def build_model():
    num_classes = len(letters);
    input_shape = get_input_shape()
    # 两层2x2窗口的卷积(卷积核数为32和64)，一层最大池化(MaxPooling2D)
    # 再Dropout(随机屏蔽部分神经元)并一维化(Flatten)到128个单元的全连接层(Dense)，最后Dropout输出到33个单元的全连接层（全部字符为33个）
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(32, kernel_size=(3, 3), padding='same',
                     activation='relu',
                     input_shape=input_shape))
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    # model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    return model

def train():
    x_all,t_all,x_train, t_train, x_test, t_test = get_image()

    model = build_model()
    batch_size = 100
    epochs = 15

    callbacks = [
        keras.callbacks.TensorBoard(
            log_dir="my_log",
            histogram_freq=1,
            embeddings_freq=1,
            #embeddings_data=x_train
        )]
    model.fit(x_train, t_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              # callbacks=callbacks,
              validation_data=(x_test, t_test))
    # 验证所有数据
    score = model.evaluate(x_all, t_all, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    model.save(r'.\model-%.3f.h5'% (score[1]*100))

if __name__ == '__main__':
    # import os
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    train()