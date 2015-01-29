import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(subject,content,resultFile,receiverList):
    resultFileName = resultFile.split("\\")[-1]
    msg = MIMEMultipart()
    att1 = MIMEText(open('%s' % resultFile, 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="*"'.replace("*",resultFileName)
    msg.attach(att1)
    txt = MIMEText(content,_subtype='html',_charset='gb2312')     
    msg.attach(txt)
    strTo = receiverList.split(',')
    msg['to'] = ','.join(strTo)
    print msg['to']
    msg['from'] = 'CodecPnP.TestSuite@intel.com'
    msg['subject'] = subject

    try:
        server = smtplib.SMTP()
        server.connect('smtp.intel.com')
        server.sendmail(msg['from'], strTo ,msg.as_string())
        server.quit()
        print 'Email send successfully!!'
    except Exception, e:
        print str(e)