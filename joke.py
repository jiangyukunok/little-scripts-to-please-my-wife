'''
a script that crawls a joke and the weather, which can be uploaded to aws ec2 and use
cron job to trigger aws email service.
'''

# -*- coding: utf-8 -*-
import os, sys, urllib, urllib2, json
import smtplib
from email.mime.text import MIMEText

def getJoke():
  hour_feed = os.system('date +"%H"')
  url = 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text?page='+str(hour_feed)
  req = urllib2.Request(url)
  req.add_header("apikey", "API_KEY")
  resp = urllib2.urlopen(req)
  content = resp.read()
  return content

def getWeather():
  url = 'http://apis.baidu.com/apistore/weatherservice/weather?citypinyin=guilin'
  req = urllib2.Request(url)
  req.add_header("apikey", "API_KEY")
  resp = urllib2.urlopen(req)
  content = resp.read()
  return content

mail_content = '<font size="15" face="elephant" color="red">&#128147;&#128147;&#128147;</font>'


weather_content = getWeather()
if weather_content:
  json_result = json.loads(weather_content)
  mail_content += '<p>今天' +json_result['retData']['city'].encode('utf8')+ '的天气是</p>'
  mail_content += '<p>'+json_result['retData']['weather'].encode('utf8')+', '+ json_result['retData']['WS'].encode('utf8') + '. 温度' + json_result['retData']['l_tmp'].encode('utf8')+ '到' + json_result['retData']['h_tmp'].encode('utf8') + '摄氏度' +'</p>'
else:
  print "get weather error"


joke_content = getJoke()
if(joke_content):
  json_result = json.loads(joke_content)
  content_list = json_result['showapi_res_body']['contentlist']
  #first_title = content_list[0]['title'].encode('utf8')
  hour_feed = os.system('date +"%H"')
  first_text = content_list[0]['text'].encode('utf8')
  mail_content += ('<p>每天一个笑话：）</p><p>' + str(first_text) + '</p>')
else:
  print "get joke error"
mail_content += '<br><p><b>Da~Yan~Bao~</b></p>'


subject = 'YOUR_SUBJECT'
msg = MIMEText(mail_content,'html','utf-8')
msg['Subject'] = subject

mail_server = 'smtp.gmail.com'
mail_server_port = 587
server = smtplib.SMTP(mail_server, mail_server_port)

username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
sender = 'YOUR_EMAIL'
receiver = 'RECEIVER_EMAIL'

mail_server = 'MAIL_SERVER'
mail_server_port = 587
server = smtplib.SMTP(mail_server, mail_server_port)

server.ehlo()
server.starttls()
server.login(username, password)
server.sendmail(sender, receiver, msg.as_string())

server.quit()
print "DONE!!!"
