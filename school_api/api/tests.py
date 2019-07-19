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
