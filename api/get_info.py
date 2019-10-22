# -*- coding: utf-8 -*-

from lxml import etree
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


def personal_information():
    """获取个人信息"""
    pass


def announcement():
    """获取公共"""
    pass


def class_schedule(session):
    """获取课程表"""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'Referer': 'http://jwc.xhu.edu.cn/xtgl/login_slogin.html'}

    data = {'xnm': '2019',
            'xqm': '3'}
    response = session.post(
            'http://jwc.xhu.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151', headers=headers, data=data)
    print(response.json())


def grade(session):
    """获取成绩"""
    url = 'http://jwc.xhu.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'

    data = {'xnm': '2018',
            'xqm': '12',
            '_search': 'false',
            'nd': '1571650469473',
            'queryModel.showCount': '50',
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '5'}

    response = session.post(
            'http://jwc.xhu.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151', headers=headers, data=data)
    print(response.json())


def expriment_grade():
    """获取实验成绩"""
    pass


def rank():
    """获取排名信息"""
    pass


def exam():
    response = requests.get(
        'http://jwc.xhu.edu.cn/xskscx.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121604')
    html = etree.HTML(response.text)

