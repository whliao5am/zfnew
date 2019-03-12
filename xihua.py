from keras.models import load_model
import io
from PIL import Image
import string
import numpy as np
import getpass
import requests
from lxml import etree
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# 图片预测函数
def pridict(image):
    split_lines = [5, 17, 29, 41, 53]  # 验证码纵向切分的位置
    y_min, y_max = 1, 23  # 验证码横向切分的位置
    model_path = 'verification_code_model.h5'
    name = []  # 验证码

    image = image.convert('L')
    ims = [image.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]  # 验证码切分成四个数字
    for i in range(4):
        # 验证码去噪
        rows, cols = ims[i].size
        for r in range(1, rows-1):
            for l in range(1, cols-1):
                num = 0
                pixel = ims[i].getpixel((r, l))
                if pixel != 255:
                    if ims[i].getpixel((r, l-1)) == 255:
                        num += 1
                    if ims[i].getpixel((r-1, l)) == 255:
                        num += 1
                    if ims[i].getpixel((r, l+1)) == 255:
                        num += 1
                    if ims[i].getpixel((r+1, l)) == 255:
                        num += 1
                    if num >= 3 or ims[i].getpixel((r, l)) >= 128:
                        ims[i].putpixel((r, l), 255)
                    elif ims[i].getpixel((r, l)) < 128:
                        ims[i].putpixel((r, l), 0)
        ims[i] = ims[i].convert('1')

    CHRS = string.ascii_lowercase + string.digits  # 小写字母+数字

    model = load_model(model_path)
    for i in range(4):
        test_input = 1.0 * np.array(ims[i])  # 图片转化为矩阵
        test_input = test_input.reshape(1, *(12, 22, 1))  # reshape多出来一个1因为预测的时候只有一个样本
        y_probs = model.predict(test_input)  # 模型预测, y_probs的形状为(1, 36)
        name.append(CHRS[y_probs[0].argmax(axis=0)])
    return ''.join(name)  # name列表中元素, 拼接在一起, 中间用''隔开


class Xihua(object):

    def login(self, url, code_url, account, password):  # 登陆教务系统函数

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome()

        browser.get(url)
        browser.implicitly_wait(10)  # 隐式等待10s

        try:  # 检测网页加载是否完成
            browser.find_element_by_class_name('login_right')
            index = True
        except:
            index = False
            print('网页加载失败！')

        if index:
            # 获取cookies 和 设置headers
            cookies = browser.get_cookies()
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookiestr = '; '.join(item for item in cookie)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                'Cookie': cookiestr,
                'Host': 'jwc.xhu.edu.cn'
            }
            #  输入账号密码动作
            browser.find_element_by_id('txtUserName').clear()
            browser.find_element_by_id('txtUserName').send_keys(account, Keys.TAB, Keys.TAB, password)
            # 获取验证码
            response = requests.get(code_url, headers=headers)
            image = Image.open(BytesIO(response.content))

            code = pridict(image)
            print(code)

            # 输入验证码，登陆
            browser.find_element_by_id('txtSecretCode').send_keys(code)
            browser.find_element_by_id('Button1').click()

            name = browser.find_element_by_xpath('//*[@id="xhxm"]').text.replace('同学', '')
            __VIEWSTATE = browser.find_element_by_xpath('//*[@id="Form1"]/input[3]').get_attribute('value')
            # browser.get('http://jwc.xhu.edu.cn/content.aspx')
            # __VIEWSTATE_post = browser.find_element_by_xpath('//*[@id="form1"]/input').get_attribute('value')
            # print(__VIEWSTATE_post)

            return browser, cookiestr, name, headers, __VIEWSTATE

    def get_tests(self, cookies, __VIEWSTATE):  # 获取考试信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Cookie': cookies,
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112',
            'Host': 'jwc.xhu.edu.cn',
            '__VIEWSTATE': __VIEWSTATE
        }
        response = requests.get(
            'http://jwc.xhu.edu.cn/xskscx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121604', headers=headers)
        html = etree.HTML(response.text)

    def get_announcement(self, cookies, __VIEWSTATE):  # 获取公告
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Cookie': cookies,
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112',
            'Host': 'jwc.xhu.edu.cn',
            '__VIEWSTATE': __VIEWSTATE
        }
        response = requests.get('http://jwc.xhu.edu.cn/content.aspx', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        for i in soup.find_all(name='td'):
            text = str(i.string)
            if text != 'None':
                print(text)
        # response = requests.get('http://jwc.xhu.edu.cn/ggsm.aspx?fbsj=2018-12-13%2011:27:52&yxqx=2019-07-13&xh=242', headers=headers)
        # response = requests.get('http://jwc.xhu.edu.cn/wbwj/2018-2019学年第2学期西华大学校本部开课情况一览表（20181213）.xls')
        # with open('a.xls', 'wb') as f:
        #   f.write(response.content)

    def get_class_schedule(self, cookies, __VIEWSTATE):  # 获取课程表
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Cookie': cookies,
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112',
            'Host': 'jwc.xhu.edu.cn',
            '__VIEWSTATE': __VIEWSTATE
        }
        response = requests.get(
            'http://jwc.xhu.edu.cn/xskbcx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121603', headers=headers)
        print(response.text)

    def choose_class(self, browser):  # 选课
        # 快速选课
        browser.execute_script('window.open()')
        browser.switch_to_window(browser.window_handles[1])
        browser.get('http://jwc.xhu.edu.cn/xsxk.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121101')
        browser.find_element_by_xpath('/html/body/h2/a').click()
        browser.find_element_by_xpath('//*[@id="Button2"]').click()
        # 校公选课
        browser.find_element_by_xpath('//*[@id="Button2"]').click()
        browser.switch_to_window(browser.window_handles[2])
        browser.find_element_by_xpath('//*[@id="ListBox1"]/option').click()
        browser.find_element_by_xpath('//*[@id="Button1"]').click()
        browser.switch_to_window(browser.window_handles[1])

        n = len('//*[@id="kcmcgrid"]/tbody/tr[12]/td/b/*')
        index = False
        for i in range(2, n + 1):
            browser.find_element_by_xpath('//*[@id="kcmcgrid"]/tbody/tr[12]/td/b/a[' + str(i) + ']').click()
            for son in browser.find_elements_by_xpath('//*[@id="kcmcgrid"]/tbody/tr/td[1]/a'):
                if son.text == '151188019':
                    son.click()
                    index = True
                    break

            while index:
                break

    def get_expriment_fraction(self, cookies, __VIEWSTATE):  # 获取实验考试分数
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Cookie': cookies,
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112',
            'Host': 'jwc.xhu.edu.cn',
            '__VIEWSTATE': __VIEWSTATE
        }
        response = requests.get(
            'http://jwc.xhu.edu.cn/xssycjcx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121609',
            headers=headers)
        print(response.text)

    def get_grade(self, browser):  # 获取成绩
        browser.get('http://jwc.xhu.edu.cn/xscjcx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121605')
        browser.find_element_by_xpath()
        pass


if __name__ == '__main__':
    account = '3120170807112'
    password = 'liao787960'
    url = 'http://jwc.xhu.edu.cn/'  # 教务系统网页url
    code_url = 'http://jwc.xhu.edu.cn/CheckCode.aspx'  # 教务系统验证码url


    #get_announcement(ret[1], ret[4])
    #get_class_schedule(ret[1], ret[4])
    #choose_class(ret[0])
    #get_expriment_fraction(ret[1], ret[4])
    #get_grade(ret[0])
