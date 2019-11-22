# 新版正方教务教务系统API
一个有关新版正方教务管理系统（如下图展示的主页面即为新版教务系统）的API，可以实现教务系统内基础的查询功能，未来还会添加选课抢课，一键评价等功能。
![主页](doc/image/main_page.png)

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
**推荐直接结合调用例子：**[examples]('https://github.com/NeroAsmarr/zfnew/tree/master/examples')

### Login类
- 调用方法：`from zfnew import Login`
- 传入参数：
    - `base_url  # 学校教务系统的主页url`
- 属性：
    - `self.base_url  # 学校教务系统的主页url`
    - `self.headers  # 登陆的headers` 
    - `self.sess  # 登陆的会话`
    - `self.cookies  # 登陆的cookiejar`
    - `self.cookies_str  # 登陆的cookie字符串`
- 方法：
    - `login(sid, password)`
        - sid: 学号
        - password: 密码

### GetInfo类
- 调用方法：`from zfnew import GetInfo`
- 传入参数：
    - `base_url  # 学校教务系统的主页url`
    - `self.cookies  # 登陆的cookiejar`
- 属性：
    - `self.base_url  # 学校教务系统的主页url`
    - `self.headers  # 登陆的headers` 
    - `self.cookies  # 登陆的cookiejar`
- 方法：
    - `get_pinfo() # 获取个人信息`
    - `get_notice(sid, password) # 获取学校通知`
    - `get_message(sid, password) # 获取调课、改课消息`
    - `get_grade(year, term) # 获取成绩`
        - year: 学年（如：2019）
        - term: 学期（0：全年，1：第一学期，2：第二学期）
    - `get_exam(sid, password) # 获取考试信息`
        - year: 学年（如：2019）
        - term: 学期（1：第一学期，2：第二学期）
    - `get_schedule(sid, password) # 获取课程表`
        - year: 学年（如：2019）
        - term: 学期（1：第一学期，2：第二学期）

#### 方法返回的json数据
1. get_pinfo 获取个人信息
```json
{
  "name": "姓名",
  "studentId": "学号",
  "brithday": "生日",
  "idNumber": "身份证号",
  "candidateNumber": "考试号",
  "status": "学籍状态",
  "collegeName": "学院名",
  "majorName": "专业名",
  "className": "班级",
  "entryDate": "入学日期",
  "graduationSchool": "毕业中学",
  "domicile": "户籍所在地",
  "politicalStatus": "政治面貌",
  "national": "民族",
  "education": "教育程度",
  "postalCode": "邮政编码"
}
```
2. get_notice 获取学校通知
```json
[
  {
    "title": "通知标题",
    "publisher": "发布者",
    "ctime": "发布时间",
    "vnum": "浏览量",
    "content": "发布内容",
    "doc_urls": ["文内附带文件链接", "..."]
  }, 
  "..."
]
```
3. get_message 获取调课、改课消息
```json
[
  {
    "message": "发布内容",
    "ctime": "发布时间"
  },
  "..."
]
```
4. get_grade 获取成绩
```json
{
  "name": "姓名",
  "studentId": "学号",
  "schoolYear": "学年",
  "schoolTerm": "学期",
  "course":
    [
      {
        "courseTitle": "课程名",
        "teacher": "授课老师",
        "courseId": "课程号",
        "className": "教学班",
        "courseNature": "课程性质",
        "credit": "课程学分",
        "grade": "成绩",
        "gradePoint": "绩点",
        "gradeNature": "考试性质",
        "startCollege": "开课学院",
        "courseMark": "课程标记",
        "courseCategory": "课程类别",
        "courseAttribution": "课程归属"
      },
      "..."
    ]
}
```
5. get_exam 获取考试信息
```json
{
  "name": "姓名",
  "studentId": "学号",
  "schoolYear": "学年",
  "schoolTerm": "学期",
  "exams":
    [
      {
        "courseTitle": "课程名",
        "teacher": "授课老师",
        "courseId": "课程号",
        "reworkMark": "重修标记",
        "selfeditingMark": "自修标记",
        "examName": "考试名称",
        "paperId": "试卷编号",
        "examTime": "考试时间",
        "eaxmLocation": "考试地点",
        "campus": "考试校区",
        "examSeatNumber": "座位号",
      },
      "..."
    ]
}
```
6. get_schedule 获取课程表
```json
{
  "name": "姓名",
  "studentId": "学号",
  "schoolYear": "学年",
  "schoolTerm": "学期",
  "normalCourse":
    [
      {
        "courseTitle": "课程名",
        "teacher": "授课老师",
        "courseId": "课程号",
        "courseSection": "课程节次",
        "courseWeek": "课程周次",
        "courseRoom": "上课地点",
        "className": "教学班名称",
        "hoursComposition": "课程学时组成",
        "weeklyHours": "周学时",
        "totalHours": "总学时",
        "credit": "学分"
      },
      "..."
    ],
  "otherCourses": ["其他课程信息", "..."]
}
```