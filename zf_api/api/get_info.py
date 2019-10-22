# -*- coding: utf-8 -*-

from lxml import etree
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


class GetInfo(object):
    def __init__(self, session):
        self.session = session
        self.main_url = 'http://jwc.xhu.edu.cn/'

    def get_announcement(self):
        headers = {
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112',
        }
        a_data = []

        response = self.session.get('http://jwc.xhu.edu.cn/content.aspx', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        for i in soup.find(attrs={'class': 'datelist'}).find_all(attrs={'href': '#'}):
            url = self.main_url + re.search(r"'(.*?)'", i.attrs['onclick']).group(1)
            info = []
            for j in i.parent.parent.find_all('td'):
                info.append(j.string)

            res = self.session.get(url)
            soup1 = BeautifulSoup(res.text, 'lxml')
            try:
                content = re.sub(r'<span.*?>|</span>|</a>|<a.*?>|<p>|</p>|&nbsp;|<br/>',
                                 '',
                                 soup1.find('textarea').string)
            except TypeError:
                content = 'None'
            try:
                download = [i.string for i in soup1.find(attrs={'class': 'download'}).find('table').find_all('a')]
            except TypeError:
                download = []

            a_data.append(
                {'url': url,
                 'title': info[0],
                 'issued': info[1],
                 'release_time': info[2],
                 'validity_period': info[3],
                 'content': content,
                 'download': download
                 })
        return a_data

    def get_expriment_grade(self):
        headers = {
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112'
        }
        response = self.session.get(
            'http://jwc.xhu.edu.cn/xssycjcx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121609',
            headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        g_data = []
        for i in soup.find(attrs={'class': 'datelist'}).find_all('tr'):
            info = []
            for j in i.find_all('td'):
                info.append(j.string)
            g_data.append(
                {'学年': info[0],
                 '学期': info[1],
                 '课程名称': info[2],
                 '项目名称': info[3],
                 '项目代码': info[4],
                 '项目学分': info[5],
                 '项目性质':	info[6],
                 '项目成绩': info[7]
                 })
        return g_data[1:]

    def get_grade(self):  # 获取成绩
        headers = {
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112',
        }
        data = {
            'xnd': '2018 - 2019',
            'xqd': '2'
        }
        respose = self.session.get(
            'http://jwc.xhu.edu.cn/xskbcx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121603',
            headers=headers,
            data=data)
        soup = BeautifulSoup(respose.text, 'lxml')
        #print(soup.prettify())
        print(soup.find(attrs={'id': 'Table1'}))

    def get_class_schedule(self, cookies, __VIEWSTATE):  # 获取课程表
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Cookie': cookies,
            'Referer': 'http://jwc.xhu.edu.cn/xs_main.aspx?xh=3120170807112',
            'Host': 'jwc.xhu.edu.cn',
            '__VIEWSTATE': __VIEWSTATE
        }
        response = self.session.get(
            'http://jwc.xhu.edu.cn/xskbcx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121603', headers=headers)
        print(response.text)
