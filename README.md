# ZF_Verify
使用CNN识别正方教务系统验证码，学习AI后的第一个应用

初始的已标记好的训练集来自于：3tnet/zfjw-captcha-cnn 和 maxnoodles/zhengfang_login

## 训练好的的参数

最终的参数是 model-99.967.h5   
参数训练框架版本：keras 2.3.1, tensorflow 2.1

## 其他平台
训练好的模型可以提供给其他系统使用，有两个demo

### 1.tensorflow.js
转换模型：keras -> tensoflow.js
```bash
tensorflowjs_converter --input_format keras model-99.967.h5 .
```
得到两个文件
```bash
model.json
group1-shard1of1.bin
```
复制这两个文件到`static`文件夹，把
```"paths": ["group1-shard1of1.bin"]```   
改为   
```"paths": ["static/group1-shard1of1.bin"]```   
打开`http://localhost:5000/static/kerasjs.html`查看结果

### 2.Android
使用tenforflow lite框架   
转换模型：keras -> android
```bash
tflite_convert --keras_model_file=model-99.967.h5 --output_file=model.tflite
```
得到文件
```bash
model.tflite
```
使用方法参见：[TFLiteZf](https://github.com/yswift/TFLiteZf)

## 问题解决

1. 错误：cannot import name 'shape_poly' from 'jax.experimental.jax2tf' 
```
vim ~/.local/lib/python3.10/site-packages/tensorflowjs/converters/jax_conversion.py
#line29 comment
#PolyShape = shape_poly.PolyShape
#line 20 comment
#from jax.experimental.jax2tf import shape_poly
from jax.experimental.jax2tf import PolyShape
```

2. tensorflow.python.framework.errors_impl.NotFoundError: D:\Work\Machine-Learning\mlenv\Lib\site-packages\tensorflow_decision_forests\tensorflow\ops\inference\inference.so not found
> windows 系统下的错误，用 wsl

