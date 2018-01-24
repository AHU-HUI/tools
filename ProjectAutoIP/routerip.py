# encoding:utf8
import requests
import re


def login(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=15d12a617f60-0f668856b-142c3763-1aeaa0-15d12a617f7ff; CNZZDATA1256793290=1074499663-1499255139-%7C1504884718',
        'DNT': '1',
        'Host': '192.168.1.1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
        'X-DevTools-Emulate-Network-Conditions-Client-Id': '37D484E8-0DCC-4C00-B7D8-E08426FF94A1',
    }
    result = requests.get(url, headers=headers)
    pattern = re.compile('"172(.*?)",')
    ip = '172' + str(re.findall(pattern, result.content.decode('gbk'))[0])
    print(ip)

if __name__ == '__main__':
    url = 'http://192.168.1.1/userRpm/StatusRpm.htm'
    login(url)
