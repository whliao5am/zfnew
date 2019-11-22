# 获取学校通知例子

from zfnew import GetInfo, Login

base_url = '学校教务系统的主页url'

lgn = Login(base_url=base_url)
lgn.login('账号', '密码')
cookies = lgn.cookies  # cookies获取方法
person = GetInfo(base_url=base_url, cookies=cookies)
notice = person.get_notice()
print(notice)
