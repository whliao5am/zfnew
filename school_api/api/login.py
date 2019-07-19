# -*- coding: utf-8 -*-

import requests
from io import BytesIO
from PIL import Image
from xihua.predict_code.predict import CodePredicting

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class Login(object):

    def login_page(self, url, code_url, account, password):  # 登陆教务系统函数

        chrome_options = Options()
        #chrome_options.add_argument('--headless')
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

            codepredict = CodePredicting()
            code = codepredict.img_denoising(image)
            code = codepredict.img_pridict(code)
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
