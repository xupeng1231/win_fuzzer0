import pykd
import os
import time
import shutil
import sys
import datetime
from subprocess import Popen,call
import traceback

def log(log_str):
    with open("p.log","at") as log:
        log.write(log_str)

def sleep():
    time.sleep(200)

e=pykd.dbgCommand
input_dir=os.path.join(os.getcwd(),"input")
crash_dir=os.path.join(os.getcwd(),"crashes")
if not os.path.exists(input_dir):
    log("ERROR:input dir not exists")
    os._exit(0)
if not os.path.exists(crash_dir):
    os.makedirs(crash_dir)


def save_sample(who_find):
    try:
        log( "\n"+str(who_find)+" FIND VULNERABILITY!!!"+"#"*64+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
    except:
        traceback.print_exc()

    sample_file=sys.argv[1]
    try:
        Popen(args=["python", "mycopy.py",os.path.join(input_dir, sample_file),os.path.join(crash_dir, sample_file)],shell=True)
    except:
        traceback.print_exc()

    try:
        shutil.copyfile(os.path.join(input_dir, sample_file), os.path.join(crash_dir, sample_file))
    except:
        traceback.print_exc()
        shutil.copyfile(os.path.join(input_dir, sample_file), os.path.join(crash_dir, sample_file))

    try:
        logf=open(os.path.join(crash_dir,"log_"+sample_file+".txt"),"wt")
        logf.write("*"*40+".lastevent"+"*"*40+"\n"*2)
        logf.write(e(".lastevent")+"\n"*4)
        logf.write("*"*40+"r"+"*"*40+"\n"*2)
        logf.write(e("r")+"\n"*4)
        logf.write("*"*40+"u "+"*"*40+"\n"*2)
        logf.write(e("u")+"\n"*4)
        logf.write("*"*40+"ub"+"*"*40+"\n"*2)
        logf.write(e("ub eip")+"\n"*4)
        logf.write("*"*40+"callstack"+"*"*40+"\n"*2)
        logf.write(e("kv")+"\n"*4)
        logf.write("*" * 40 + "lm" + "*" * 40 + "\n" * 2)
        logf.write(e("lm") + "\n" * 4)
        logf.close()
    except:
        traceback.print_exc()
        log( "ERROE:crashlog create error!")
    sleep()

while True:
    try:
        res_g=e("sxd cpr;sxd ld;sxd ct;sxd et;g")
        event=e(".lastevent")
        kstr=e("k L2")
        rstr=e("r")
        if not (kstr.find("verifier!VerifierStopMessage") >= 0):
            save_sample("M")
        if event.find("WOW64 breakpoint") > 0 or event.find("Break instruction exception") > 0 or event.find("Exit process") > 0 or rstr.find("ntdll!KiFastSystemCallRet") > 0:
            continue
        save_sample("I")
    except:
        pass