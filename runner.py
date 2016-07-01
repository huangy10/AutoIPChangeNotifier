from bs4 import BeautifulSoup
import urllib2
import re
import os
import smtplib
import yaml

from email.mime.text import MIMEText

SERVERNAME = "MyMachine"
EMAIL = "<email>"
PASSWORD = "<password>"
SMTP_SERVER = "smtp.163.com"
SMTP_SERVER_PORT = '25'

logFile = '/var/log/autoipchangenotifier.log'

request = urllib2.urlopen(
    'http://www.baidu.com/s?wd=ip&rsv_spt=1&rsv_iqid=0xbefbb8610000747d&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=4&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&inputT=1648&rsv_sug4=1648'
)

soup = BeautifulSoup(request)
ipResponse = soup.find('div', {'class': 'result-op c-container'}).get("fk")
print ipResponse
ip = re.search('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', str(ipResponse)).group(0)

prevIp = ip

try:
    with open(logFile, 'r') as log:
        prevIp = log.readline()
        log.close()
except IOError:
    pass

if ip != prevIp:
    target_emails = yaml.load(open(
        os.path.join(os.path.dirname(__file__), 'emails.yaml')))['emails']
    for recipient in target_emails:
        msg = MIMEText("New IP address for {servername} is {ip}".format(
            servername=SERVERNAME, ip=ip
        ))
        msg['Subject'] = 'IP address of {servername} Changed'.format(
            servername=SERVERNAME
        )
        msg['From'] = EMAIL
        print "Connecting to smtp server"
        server = smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL, PASSWORD)

        msg['To'] = recipient
        print 'sending email'
        server.sendmail(EMAIL, recipient, msg.as_string())
        server.quit()
        print "Success!"

with open(logFile, 'w') as log:
    log.write(ip)
    log.close()
