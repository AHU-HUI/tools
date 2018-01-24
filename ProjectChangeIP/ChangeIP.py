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

ip = '172.23.12.22'


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
    print "原文:%s" % plainText
    print "签名:%s" % signText

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
            print url
            httpsConn.request("GET", url)
        elif requestMethod == "POST":
            params = urllib.urlencode(params)
            print headers
            httpsConn.request("POST", requestPath, params, headers)

        response = httpsConn.getresponse()
        data = response.read()
        # print data
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


def change_id(recordId):
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
        'value': ip

    }

    plainText = makePlainText(requestMethod, requestHost, requestPath, params)
    signText = sign(requestMethod, requestHost, requestPath, params, secretKey)
    print "原文:%s" % plainText
    print "签名:%s" % signText

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
            print url
            httpsConn.request("GET", url)
        elif requestMethod == "POST":
            params = urllib.urlencode(params)
            print headers
            httpsConn.request("POST", requestPath, params, headers)

        response = httpsConn.getresponse()
        data = response.read()
        # print data
        jsonRet = json.loads(data)
        json_data = json.dumps(jsonRet, indent=4, ensure_ascii=False)
        print  json_data


    except Exception, e:
        print e
    finally:
        if httpsConn:
            httpsConn.close()


if __name__ == '__main__':
    recordId = get_id()
    print recordId
    change_id(recordId)
