import requests
from io import BytesIO
import numpy as np
from PIL import Image
from school_api.predict_code import predict
import re


main_url = 'http://jwc.xhu.edu.cn'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

session = requests.Session()

_ = session.get(main_url, headers=headers)
viewstate = re.search('"__VIEWSTATE" value="(.*?)"', _.text)  # 获取viewstate参数

# cookies = _.cookies
# print(cookies)
# cookiestr = '; '.join([item[0] + '=' + item[1] for item in cookies.items()])
# print(cookiestr)


code_url = 'http://jwc.xhu.edu.cn/CheckCode.aspx'

#response1 = session.get(code_url)
#img = Image.open(BytesIO(response1.content))  # 验证码图片
#img = np.asarray(img)  # 验证码处理为numpy
#ims = predict.img_press(img)  # 验证码切分
#code = predict.img_pridict(ims, 'predict_code/verification_code_model.h5')  # 验证码预测

data = {'__VIEWSTATE': viewstate.group(1),
        'txtUserName': '3120170807112',
        'TextBox2': 'liao787960',
        'txtSecretCode': code,
        'RadioButtonList1': '学生'.encode('gb2312'),  # %D1%A7%C9%FA
        'TextBox1': '',
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': ''
        }

login_url = 'http://jwc.xhu.edu.cn/default2.aspx'
response = session.post(login_url, data=data)
print(response.text)

# content_headers = {
#     'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112'
# }
#
# response = session.get('http://jwc.xhu.edu.cn/xskbcx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121603', headers=content_headers)
# print(response.text)
