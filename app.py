from flask import Flask, request
from flask import render_template
from PIL import Image
from captcha.predict import predict
# from flask_cors import *

app = Flask(__name__)
# CORS(app, supports_credentials=True)

# 能正常工作的包
# tensorflow 1.15，keras 2.2.5 只支持1.15,不能用2.0以上
# keras 2.2.5，不能用2.3
# 使用 keras 2.3.1 报线程错，

p = predict(r'./model.h5')

@app.route('/')
def hello_world():
    base64,code = p.verify_url()
    return render_template('index.html', base64=base64, code=code)

@app.route("/image_demo", methods=["GET"])
def image_demo():
    return render_template('image_demo.html')

@app.route("/verify/image", methods=["POST"])
def verify_image():
    f = request.files['file']
    image = Image.open(f)
    code = p.verify_image(image)
    return {"status":0, "code":code}

@app.route("/base64_demo", methods=["GET"])
def base64_demo():
    return render_template('base64_demo.html')

@app.route("/verify/base64", methods=["POST"])
def verify_base64():
    base64 = request.form.get('base64')
    print("base64=",base64)
    code = p.verify_base64(base64)
    return {"status":0, "code":code}
    # return {"status":0, "code":"1234"}

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
