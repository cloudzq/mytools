# -*- coding:utf-8 -*-
"""
@Project:watchmen
@Language:Python3.6.4
@Author:Hans
@File:mail.py
@Ide:PyCharm
@Time:2018/8/20 14:59
@Remark:
"""

import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from email.mime.application import MIMEApplication


class MailClient(object):
    def __init__(self, mail_to_list, mail_cc_list, mail_title, html_file,
                 mail_user='sboms@xxx.com.cn',
                 mail_host='192.168.108.193', attachment=[]):
        """
         email function
        :param mail_to_list: 发给谁 ,list or tuple
        :param mail_cc_list:抄送给谁 ,list or tuple
        :param mail_title: 邮件标题 ,str
        :param html_file:邮件正文 ,str
        :param mail_user:发送邮件的人 ,str
        :param mail_host: SMTP服务器地址 ,str
        :param attachment: 附件 ,默认为None,list or tuple 绝对路径
        """

        print(mail_to_list)
        print(mail_cc_list)

        self.mail_tolist = ['xxx@xxx.com.cn','<xxx@xxx.com.cn>']
        self.mail_cclist = ['xxx@xxx.com.cn']

        self.mail_title = mail_title
        self.attachment = attachment
        self.mail_content = self._get_content(html_file)
        self.mail_host = mail_host
        self.mail_user = mail_user

    def _get_content(self,html_file):
        try:
            with open(html_file,'r',encoding='UTF-8') as f:
                content = f.read()
                return content
        except Exception:
            return html_file

    def retry_send(num=3,interval=5):
        def inner(func):
            @wraps(func)
            def wrap(*args,**kwargs):
                count = 0
                while count < num:
                    ret = func(*args,**kwargs)
                    if ret:
                        return ret
                    count += 1
                    time.sleep(interval)
                return ret
            return wrap
        return inner

    @retry_send(3,5)
    def send_mail(self):
        me = self.mail_user
        msg = MIMEMultipart
        msg['Subject'] = self.mail_title
        msg['From'] = me
        msg['To'] = ";".join(self.mail_tolist)
        msg['Cc'] = ";".join(self.mail_cclist)
        try:
            mailtext = MIMEText(self.mail_content,_subtype='html',_charset='utf-8')
            msg.attach(mailtext)
            #添加附件
            for file in self.attachment:
                with open(file,'rb') as f:
                    content = f.read()
                part = MIMEApplication(content)
                part.add_header('Content-Disposition','attachment',filename=file.split('/')[-1])
                msg.attach(part)
            s = smtplib.SMTP()
            #连接到指定的SMTP服务器，参数分别表示SMTP主机和端口
            s.connect(self.mail_host)
            #发送内容
            s.sendmail(me,self.mail_tolist + self.mail_cclist,msg.as_string())
            s.close()
            return True
        except Exception:
            return False

if __name__ == '__main__':
    client = MailClient(mail_to_list=['xxx@xxx.com.cn'],
               mail_cc_list=['xxx@xxx.com.cn','xxb@xxx.com.cn'],
               html_file='/tmp/pages.html',
               attachment=['/tmp/pages.html',
                           '/tmp/test.sh',
                           '/home/mypages.tgz'],
               mail_user='xxx@xxx.com.cn',
               mail_title='xxxxx')

    client.send_mail()

