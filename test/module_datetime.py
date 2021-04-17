###############################################
# module test : datetime 
###############################################
import datetime

now = datetime.datetime.now()

print(now)

print(now + datetime.timedelta(hours=10))
print(now - datetime.timedelta(minutes=10))