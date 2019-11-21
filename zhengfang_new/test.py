from api import *

lgn = Login()
lgn.login()
# sess = lgn.sess
base_url = 'http://jwc.xhu.edu.cn/'
xiaoming = GetInfo(base_url=base_url, cookies=lgn.cookies)
print(xiaoming.get_message())
#print(classroom(sess))
