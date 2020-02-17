// ==UserScript==
// @name     zf_captcha
// @include  http://jwxt.njupt.edu.cn/
// @require	 https://code.jquery.com/jquery-2.2.4.min.js
// @version  1
// @grant    none
// ==/UserScript==

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

function verify() {
  var img = document.getElementById("icode");
  var b64 = getBase64Image(img);
  // 选择教师
  document.getElementById("RadioButtonList1_1").checked=true;
  $.post('http://localhost:5000' + "/verify/base64",
            {base64:b64},
            function(data) {
                var txtSecretCode = document.getElementById("txtSecretCode");
                // txtSecretCode.keydown(txtSecretCode)
                if (unsafeWindow.keydown) {
                    // 模拟在输入框中按键，有标记设置，和颜色改变
                    unsafeWindow.keydown(txtSecretCode);
                }
                txtSecretCode.value = data.code;
            },
            "json");
}

// 延迟执行
setTimeout(verify,300);

