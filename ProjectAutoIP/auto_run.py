# -*- coding: utf-8 -*-
# !/usr/bin/python
import urllib
import urllib2
import httplib
import binascii
import hashlib
import hmac
import time
import random
import sys
import json
import requests
import re

url = 'http://192.168.1.1/userRpm/StatusRpm.htm'

#从路由器获取校内网IP地址
def get_ip(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Authorization': 'Basic U2hpbmU6cHBubjEz',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=15d12a617f60-0f668856b-142c3763-1aeaa0-15d12a617f7ff; CNZZDATA1256793290=1074499663-1499255139-%7C1504884718',
        'DNT': '1',
        'Host': '192.168.1.1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
        'X-DevTools-Emulate-Network-Conditions-Client-Id': '37D484E8-0DCC-4C00-B7D8-E08426FF94A1',
    }
    try:
        result = requests.get(url, headers=headers)
        pattern = re.compile('"172(.*?)",')
        ip = '172' + str(re.findall(pattern, result.content.decode('gbk'))[0])
        print 'Internal network Address:'+ip
        return ip
    except Exception, e:
        print e
    



# 拼出签名字符串原文
def makePlainText(requestMethod, requestHost, requestPath, params):
    str_params = "&".join(k + "=" + str(params[k]) for k in sorted(params.keys()))
    source = '%s%s%s?%s' % (
        requestMethod.upper(),
        requestHost,
        requestPath,
        str_params
    )
    return source


# 签名
def sign(requestMethod, requestHost, requestPath, params, secretKey):
    source = makePlainText(requestMethod, requestHost, requestPath, params)
    hashed = hmac.new(secretKey, source, hashlib.sha1)
    return binascii.b2a_base64(hashed.digest())[:-1]


def get_id():
    # secretId 和 secretKey
    secretId = 'AKIDoniArbbGFpSExjcLEFueKsSxAITkEmbY'
    secretKey = 'HXp5Ni0jcaYRrLDDJKGKqfRNR4uz7nbR'
    requestMethod = 'GET'
    requestHost = 'cns.api.qcloud.com'
    requestPath = '/v2/index.php'

    # 请求参数
    params = {
        'domain': 'shinehui.xyz',
        'SecretId': secretId,
        'Timestamp': int(time.time()),
        'Nonce': random.randint(1, sys.maxint),
        'Region': 'sh',
        'Action': 'RecordList',
        # 'Action':'RestartInstances',
        # 'instanceIds.1':'qcvm82b2fe32a4fb45f4564470e0c93c2d82'
    }
    plainText = makePlainText(requestMethod, requestHost, requestPath, params)
    signText = sign(requestMethod, requestHost, requestPath, params, secretKey)
    params['Signature'] = signText
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    # 发送请求
    httpsConn = None
    try:
        httpsConn = httplib.HTTPSConnection(host=requestHost, port=443)
        if requestMethod == "GET":
            params['Signature'] = urllib.quote(signText)
            str_params = "&".join(k + "=" + str(params[k]) for k in sorted(params.keys()))
            url = 'https://%s%s?%s' % (requestHost, requestPath, str_params)
            httpsConn.request("GET", url)
        elif requestMethod == "POST":
            params = urllib.urlencode(params)
            httpsConn.request("POST", requestPath, params, headers)

        response = httpsConn.getresponse()
        data = response.read()
        jsonRet = json.loads(data)
        json_data = json.dumps(jsonRet, indent=4, ensure_ascii=False)
        data = json.loads(json_data)
        id = data['data']['records'][0]['id']
        return id
    except Exception, e:
        print e
    finally:
        if httpsConn:
            httpsConn.close()


def change_id(recordId,ipaddress):
    # secretId 和 secretKey
    secretId = 'AKIDoniArbbGFpSExjcLEFueKsSxAITkEmbY'
    secretKey = 'HXp5Ni0jcaYRrLDDJKGKqfRNR4uz7nbR'
    requestMethod = 'GET'
    requestHost = 'cns.api.qcloud.com'
    requestPath = '/v2/index.php'

    # 请求参数
    params = {
        'domain': 'shinehui.xyz',
        'SecretId': secretId,
        'Timestamp': int(time.time()),
        'Nonce': random.randint(1, sys.maxint),
        'Region': 'sh',
        'Action': 'RecordModify',
        'recordId': int(recordId),
        'subDomain': '@',
        'recordType': 'A',
        'recordLine': '默认',
        'value': ipaddress

    }
    plainText = makePlainText(requestMethod, requestHost, requestPath, params)
    signText = sign(requestMethod, requestHost, requestPath, params, secretKey)
    params['Signature'] = signText
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    # 发送请求
    httpsConn = None
    try:
        httpsConn = httplib.HTTPSConnection(host=requestHost, port=443)
        if requestMethod == "GET":
            params['Signature'] = urllib.quote(signText)
            str_params = "&".join(k + "=" + str(params[k]) for k in sorted(params.keys()))
            url = 'https://%s%s?%s' % (requestHost, requestPath, str_params)
            httpsConn.request("GET", url)
        elif requestMethod == "POST":
            params = urllib.urlencode(params)
            httpsConn.request("POST", requestPath, params, headers)

        response = httpsConn.getresponse()
        data = response.read()
        jsonRet = json.loads(data)
        json_data = json.dumps(jsonRet, indent=4, ensure_ascii=False)
        print  json_data


    except Exception, e:
        print e
    finally:
        if httpsConn:
            httpsConn.close()


if __name__ == '__main__':
    #初始化IP
    try:
        ipaddress_init = get_ip(url)
        recordId = get_id()
        print 'Analytical records:'+ str(recordId)
        change_id(recordId,ipaddress_init)
    except Exception, e:
        print e   
    #循环判断ip是否变更
    while True:
    	log = open('log.txt','a')
        ipaddress_now = get_ip(url)
        if (ipaddress_init != ipaddress_now):
            time.sleep(10)
            try:
                recordId = get_id()
                print 'Analytical records:'+ str(recordId)
                change_id(recordId,ipaddress_now)
                ipaddress_init = ipaddress_now
                message = "IP has change to:" + str(ipaddress_now) + '      ' +time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+ '\n'
                log.write(message)
                log.close()
            except Exception, e:
                print e
        else:
            time.sleep(2)