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
