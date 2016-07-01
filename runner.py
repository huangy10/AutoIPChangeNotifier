from bs4 import BeautifulSoup
import urllib2
import re
import smtplib
import yaml

from email.mime.text import MIMEText

SERVERNAME = "MyMachine"
EMAIL = "<email>"
PASSWORD = "<password>"
SMTP_SERVER = "smtp.163.com"
SMTP_SERVER_PORT = '25'

logFile = '/var/log/autoipchangenotifier.log'

request = urllib2.urlopen('http://internet.yandex.ru')

soup = BeautifulSoup(request)
ipResponse = soup.find('div', {'class': 'client__desc'})
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
    target_emails = yaml.load(open('emails.yaml'))['emails']
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
