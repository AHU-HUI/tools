from lxml import etree

# 定义一个函数，给他一个html，返回xml结构
def getxpath(html):
    return etree.HTML(html)

# 下面是我们实战的第一个html
sample1 = """
<html>
<head>
<title>MyPage</title>
</head>
  <body>
    <ul>
      <li>Quote 1</li>
      <li>Quote 2 with <a href="contents1...">link</a></li>
      <li>Quote 3 with <a href="contents2..." >another link</a></li>
      <li><h2><a src="contents3...">Quote 4 title</a></h2> ...</li>
    </ul>
  </body>
</html>
"""
# 获取xml结构
s1 = getxpath(sample1)

# 获取标题(两种方法都可以)
str1=s1.xpath('//title/text()')
str2=s1.xpath('/html/head/title/text()')
#获取属性为src的值
str3=s1.xpath('//h2/a/@src')
#获取属性为href的值
str4=s1.xpath('//@href')
#获取所有的文本
str5=s1.xpath('//text()')
print(str1)
print(str2)
print(str3)
print(str4)
print(str5)
