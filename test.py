# from api.get_info import *
# from api.login import Login

lgn = Login()
lgn.login()
# print(lgn.sess.post('http://jwc.xhu.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151', data={'xnm': '2019', 'xqm': '3'}).json())
# print('http://jwc.xhu.edu.cn/xtgl/index_cxDbsy.html')
# Login.get_rsa('31231', '321', '312')
sess = lgn.sess

get_ = class_schedule(sess)