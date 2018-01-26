#coding:utf-8
import smtplib
from email.mime.text import MIMEText

mail_to = "867690427@qq.com"  # 收件人列表

# 发送方信息
mail_user = "ahu_hui@163.com"
mail_pass = "w7"

# 邮件标题
mail_sub = "huizhi"

# 邮件文本内容
mail_content = "hi!"


def send_mail(mail_to, mail_sub, mail_content):
    msg = MIMEText(mail_content)
    msg['Subject'] = mail_sub
    msg['From'] = mail_user
    msg['To'] = mail_to
    try:
        server = smtplib.SMTP('smtp.163.com:25')
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, mail_to, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    if send_mail(mail_to, mail_sub, mail_content):
        print "send success"
    else:
        print "send failed"
