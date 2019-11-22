# 新版正方教务教务系统API
一个有关新版正方教务管理系统的API，可以实现教务系统内基础的查询功能，未来还会添加选课抢课，一键评价等功能。

## 已实现与待实现
* [x] 自动登陆、cookies获取
* [x] 个人信息
* [x] 学校通知
* [x] 调课、改课消息
* [x] 成绩
* [x] 课程表
* [x] 考试信息
* [ ] 自动抢课
* [ ] 一键评价
* [ ] 选课名单
* [ ] 实验考试
* [ ] 选课名单

## 如何开始
使用pip命令安装 `pip install zfnew`

接着在python中运行如下代码验证：
```python
from zfnew import *

base_url = '学校教务系统的主页url'

lgn = Login(base_url=base_url)
lgn.login('账号', '密码')
cookies = lgn.cookies  # cookiejar类cookies获取方法
person = GetInfo(base_url=base_url, cookies=cookies)
print(person.get_pinfo())

```
如果能输出json形式的个人信息，说明运行成功。

## 详细API介绍
推荐可以直接结合调用例子：[examples]('')来

### Login类
#### 
## 返回json数据

## 自动登陆、cookies获取
```python
from zfnew import Login

base_url = '学校教务系统的主页url'

lgn = Login(base_url=base_url)
lgn.login('账号', '密码')  # 登陆
print(lgn.cookies)  # cookiejar类的cookies
print(lgn.cookies_str)  # 字符串形式的的cookies
```
成功登陆后，可以返回的cooikes有cookiejar和字符串两种形式，后面我们多使用cookiejar类的cookies进行会话保持，字符串格式的cookies只是为了方便保存到本地或者其他用处。

### 个人信息
```python
from zfnew import GetInfo, Login

base_url = '学校教务系统的主页url'

lgn = Login(base_url=base_url)
lgn.login('账号', '密码')
cookies = lgn.cookies  # cookies获取方法
person = GetInfo(base_url=base_url, cookies=cookies)
print(person.get_pinfo())
```
登陆获取cookiejar类的cookies后，再调用GetInfo模块，base_url

### 学校通知
### 调课、改课消息
### 成绩
### 课程表
### 考试信息