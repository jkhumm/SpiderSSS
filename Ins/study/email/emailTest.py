import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _formot_addr(s):
    name,addr = parseaddr(s)
    str = formataddr((Header(name, 'utf-8').encode(), addr))
    print(str)
    return str
smtp_server = 'smtp.163.com'
# 发件人地址
from_addr = 'heian_humm@163.com'
# 163的授权码
password = 'xxxx'

# 收件人地址
to_addr = '905285977@qq.com'

msg = MIMEMultipart()
html_content = """
<html>
    <body>
        <h1>study python let me happy</h1>
        <p>我的语雀地址：<a>https://www.yuque.com/humingming</a></p>
    </body>
</html>    
               """
msg['Form'] = _formot_addr(from_addr)
msg['To'] = _formot_addr(to_addr)
msg['Subject'] = Header('发送邮件的标题：','utf-8').encode()

#MIMEText('hello word','plain','utf-8') # 纯文本邮件
msg.attach(MIMEText(html_content,'html','utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open('''D:\humm\python-project\SpiderSSS\Ins\study\email\emailTest.py''', 'rb') as f:
    # 设置附件的MIME和文件名，这里是jpg类型:
    mime = MIMEBase('text', 'py', filename='emailTest.py')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='emailTest.py')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)



# 待发邮件
server = smtplib.SMTP(smtp_server,25)
#server.set_debuglevel(1) #就可以打印出和SMTP服务器交互的所有信息
server.login(user=from_addr,password=password)
# 发送邮件
server.sendmail(from_addr=from_addr,to_addrs=[to_addr], msg=msg.as_string())
server.quit()