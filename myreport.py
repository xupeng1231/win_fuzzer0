import xclient
import hashlib
import os
import time

hash=hashlib.md5()
crash_dir=os.path.join(os.getcwd(),"crashes")
if not os.path.exists(crash_dir):
    os.makedirs(crash_dir)

reported=[]

while True:
    fs=os.listdir(crash_dir)
    for f in fs:
        if f in reported:
            continue
        with open(os.path.join(crash_dir,f),"rb") as fd:
            crash_string = fd.read()
        xclient.report_crash(crash_string)
        reported.append(f)
    time.sleep(100)

