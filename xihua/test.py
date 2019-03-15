import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Cookie': 'JSESSIONID=10E8CCA0DCD73249258055881A3775B4.node_portal0',
    'Host': 'urp.xhu.edu.cn',
    'Referer': 'http://urp.xhu.edu.cn/login/xhu/login.jsp?errorCode=000',
    'Origin': 'http://urp.xhu.edu.cn'
}

data = {'login': '3120170807112',
        'password': 'liao787960'
        }

url = 'http://urp.xhu.edu.cn/c/portal/login'

reponse = requests.post(url, headers=headers, data=data)
print(reponse.status_code)
