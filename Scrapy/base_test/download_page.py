import requests

# 这里的headers就是我们上图框中的headers
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Cookie':'BAIDUID=3E5FA4E169609C134F78C8232C12758C:FG=1; PSTM=1502161818; pgv_pvi=8697621504; BIDUPSID=74C8F878FAC7DA5F53F27B849422A0A5',
'DNT':'1',
'Host':'0.baidu.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36'
}
formdata ='&#39;python&#39;:&#39;python&#39;'

testurl = "http://httpbin.org/post"
z2 = requests.post(url=testurl,data=formdata,headers=headers)
