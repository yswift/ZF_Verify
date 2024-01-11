// ==UserScript==
// @name     zf_captcha2
// @include  http://jwgl.uoh.edu.cn/
// @require	 http://localhost/zf_code/tf.min.js
// @version  1
// @grant    none
// ==/UserScript==

//greasemonkey.aboutIsGreaseable = true;
//greasemonkey.fileIsGreaseable = true;

// 油猴脚本，用于自动识别和填写网页正方系统的验证码
// njupt的教务系统外网可访问

// 图像转base64,
// https://stackoverflow.com/questions/934012/get-image-data-url-in-javascript
function getBase64Image(img) {
    // Create an empty canvas element
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    // Copy the image contents to the canvas
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    // Get the data-URL formatted image
    // Firefox supports PNG and JPEG. You could check img.src to
    // guess the original format, but be aware the using "image/jpg"
    // will re-encode the image.
    var dataURL = canvas.toDataURL("image/png");

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

function img2Tensor(imgData) {
    let tensor = tf.browser.fromPixels(imgData, numChannels = 1);
    //resize to 12 x 23
    //const resized = tf.image.resizeBilinear(tensor, [12, 23]).toFloat();
    // Normalize the image
    const offset = tf.scalar(255.0);
    //const normalized = tf.scalar(1.0).sub(tensor.div(offset));
    const normalized = tensor.div(offset);
    return tensor.reshape([12, 23, 1]);
}

function getImages() {
    var canvas = document.createElement("canvas");
    // Copy the image contents to the canvas
    var ctx = canvas.getContext("2d");
    var img = document.getElementById("icode");
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    ctx.drawImage(img, 0, 0);
    // 分割图像
    var sw = [5, 17, 28, 41];
    var imgs = [];
    for (var i = 0; i < sw.length; i++) {
        var d = ctx.getImageData(sw[i], 0, 12, 23);
        imgs.push(img2Tensor(d));
    }
    // 合并到一个张量中
    return tf.stack([imgs[0], imgs[1], imgs[2], imgs[3]]);
}

async function detect() {
    tf.enableProdMode();
    var labels = "012345678abcdefghijklmnpqrstuvwxy";
    var model;
    try {
        model = await tf.loadLayersModel('localstorage://zf-code');
        console.log('load localstorage://zf-code success');
    } catch(err) {
        console.log('load localstorage://zf-code failed');
        model = await tf.loadLayersModel('http://localhost/zf_code/model.json');
        console.log('load model from http success');
        await model.save('localstorage://zf-code');
    }
    var data = getImages();
    var idx = await model.predict(data).argMax([-1]).dataSync();
    var code = "";
    for (var i = 0; i < idx.length; i++) {
        code += labels[idx[i]];
    }
    console.log("predict = " + code);
    return code;
}

async function verify() {
    //var img = document.getElementById("icode");
    //var b64 = getBase64Image(img);
    // 选择教师
    document.getElementById("RadioButtonList1_1").checked = true;
    var txtSecretCode = document.getElementById("txtSecretCode");
    txtSecretCode.value = "识别...";
    var code = await detect();
    if (unsafeWindow.keydown) {
        // 模拟在输入框中按键，有标记设置，和颜色改变
        unsafeWindow.keydown(txtSecretCode);
    }
    txtSecretCode.value = code;
}

// 延迟执行
setTimeout(verify, 300);

