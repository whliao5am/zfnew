# -*- coding: utf-8 -*-

from lxml import etree
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import requests


class GetInfo(object):
    def __init__(self, base_url, cookies):
        self.base_url = base_url
        self.headers = {
            'Referer': 'http://jwc.xhu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        self.cookies = cookies

    def get_pinfo(self):
        """获取个人信息"""

    def get_notice(self):
        """获取通知"""
        pass

    def get_file(self):
        """获取文件"""
        pass

    def get_message(self):
        """获取消息"""
        url = 'http://jwc.xhu.edu.cn/xtgl/index_cxDbsy.html?doType=query'
        data = {
            'sfyy': '1',  # 是否已阅，未阅未1，已阅为2
            'flag': '1',
            '_search': 'false',
            'nd': '1571744696313',
            'queryModel.showCount': '50',  # 最多条数
            'queryModel.currentPage': '1',  # 当前页数
            'queryModel.sortName': 'cjsj',
            'queryModel.sortOrder': 'desc',  # 时间倒序
            'time': '0'
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        return res

    def get_elective_list(self):
        """获取选课名单信息"""
        pass

    def get_expriment_grade(self):
        """获取实验成绩信息"""
        pass

    def get_grade(self, year, term):
        """获取成绩"""
        url = self.base_url + '/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        elif term == '0':
            term = ''
        else:
            print('Please enter the correct term value！！！ ("0" or "1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12, 整个学年为空''
            '_search': 'false',
            'nd': int(time.time()*1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = requests.post(self, url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        if jres.get('items'):  # 防止数据出错items为空
            res_dict = {
                'name': jres['items'][0]['xm'],
                'studentId': jres['items'][0]['xh'],
                'schoolYear': jres['items'][0]['xnm'],
                'schoolTerm': jres['items'][0]['xqmmc'],
                'course': [{
                    'courseTitle': i['kcmc'],
                    'teacher': i['jsxm'],
                    'courseId': i['kch_id'],
                    'className': i['jxbmc'],
                    'courseNature': ''if i.get('kcxzmc')== None else i.get('kcxzmc'),
                    'credit': i['xf'],
                    'grade': i['cj'],
                    'gradePoint': '' if i.get('jd') == None else i.get('jd'),
                    'gradeNature': i['ksxz'],
                    'startCollege': i['kkbmmc'],
                    'courseMark': i['kcbj'],
                    'courseCategory': i['kclbmc'],
                    'courseAttribution': '' if i.get('kcgsmc') == None else i.get('kcgsmc')
                } for i in jres['items']]}
            return res_dict
        else:
            return {}

    def get_schedule(self, year, term):
        """获取课程表信息"""
        # 'http://jwc.xhu.edu.cn/kbcx/xskbcx_cxXsShcPdf.html?doType=list&xnm=2019&xqm=3&xszd.sj=true&xszd.cd=true&xszd.js=true&xszd.jszc=false&xszd.jxb=true&xszd.xkbz=true&xszd.kcxszc=true&xszd.zhxs=true&xszd.zxs=true&xszd.khfs=true&xszd.xf=true&xnmc=2019-2020&xqmmc=1&xm=%25E5%25BB%2596%25E6%2596%2587%25E8%25B1%25AA&jgmc=undefined&xxdm=&gnmkdm=N2151'
        url = self.base_url + '/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151'
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,
            'xqm': term
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        res_dict = {
            'name': jres['xsxx']['XM'],
            'studentId': jres['xsxx']['XH'],
            'schoolYear': jres['xsxx']['XNM'],
            'schoolTerm': jres['xsxx']['XQMMC'],
            'normalCourse': [{
                'courseTitle': i['kcmc'],
                'teacher': i['xm'],
                'courseSection': i['jc'],
                'courseWeek': i['zcd'],
                'campus': i['xqmc'],
                'courseRoom': i['cdmc'],
                'courseId': i['kch_id'],
                'className': i['jxbmc'],
                'hoursComposition': i['kcxszc'],
                'weeklyHours': i['zhxs'],
                'totalHours': i['zxs'],
                'credit': i['xf']
            } for i in jres['kbList']],
            'otherCourses': [{'info': i['qtkcgs']} for i in jres['sjkList']]}
        return res_dict

    def get_classroom(self):
        """获取空教室信息"""
        url = 'http://jwc.xhu.edu.cn/cdjy/cdjy_cxKxcdlb.html?gnmkdm=N2155&layout=default'
        data = {
            'fwzt': 'cx',
            'xqh_id': '1',
            'xnm': '2019',
            'xqm': '3',
            'cdlb_id': '',
            'cdejlb_id': '',
            'qszws': '',
            'jszws': '',
            'cdmc': '',
            'lh': '',
            'qssd': '',
            'jssd': '',
            'qssj': '',
            'jssj': '',
            'jyfs': '0',
            'cdjylx': '',
            'zcd': '256',
            'xqj': '3',
            'jcd': '9',
            '_search': 'false',
            'nd': '1571744696313',
            'queryModel.showCount': '50',  # 最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': 'cdbh',
            'queryModel.sortOrder': 'asc',
            'time': '1'
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        return res

    def get_exam(self, year, term):
        """获取考试信息"""
        url = self.base_url + '/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105'
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        if jres.get('items'):  # 防止数据出错items为空
            res_dict = {
                'name': jres['items'][0]['xm'],
                'studentId': jres['items'][0]['xh'],
                'schoolYear': jres['items'][0]['xnmc'][:4],
                'schoolTerm': jres['items'][0]['xqmmc'],
                'exams': [{
                    'courseTitle': i['kcmc'],
                    'teacher': i['jsxx'],
                    'courseId': i['kch'],
                    'reworkMark': i['cxbj'],
                    'selfeditingMark': i['zxbj'],
                    'examName': i['ksmc'],
                    'paperId': i['sjbh'],
                    'examTime': i['kssj'],
                    'eaxmLocation': i['cdmc'],
                    'campus': i['xqmc'],
                    'examSeatNumber': i['zwh']
                } for i in jres['items']]}
            return res_dict
        else:
            return {}
