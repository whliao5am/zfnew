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
