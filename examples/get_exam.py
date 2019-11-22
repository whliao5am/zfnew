# 获取考试信息例子

from zfnew import GetInfo, Login

base_url = '学校教务系统的主页url'

lgn = Login(base_url=base_url)
lgn.login('账号', '密码')
cookies = lgn.cookies  # cookies获取方法
person = GetInfo(base_url=base_url, cookies=cookies)
exam = person.get_exam('2019', '1')  # 2019年、第1学期(1 or 2)
print(exam)
