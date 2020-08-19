import datetime
import time

INFO = 1

def pl(msg,level=1):
    outstr = ""
    now = datetime.datetime.now()
    outstr += str(now)
    if level == 1:
        outstr += " [INFO] "
    outstr += msg
    print(outstr)