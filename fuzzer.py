import os
import re
import thread
import time
import generate
import datetime
import shutil
import traceback
from subprocess import Popen

sample_path=os.path.join(os.getcwd(),"sample","sample.pdf")
input_dir=os.path.join(os.getcwd(),"input")
if not os.path.exists(sample_path):
    print "ERROR:sample not exist!!!"
    os._exit(0)
if not os.path.exists(input_dir):
    os.makedirs(input_dir)

next_gate=True
def kill_windbg(a,b):
    next_gate=False
    res=os.system("taskkill /F /IM windbg.exe")
    if 0!=res:
        time.sleep(1)
        res=os.system("taskkill /F /IM windbg.exe")
    if 0!=res:
        print "KILL ERROR!!!"
        next_gate=True
        os._exit(0)
    next_gate=True

def fuzzer(last_input_file):
    fs=os.listdir(input_dir)
    if not last_input_file:
        input_file_path = os.path.join(input_dir, fs[0])
    else:
        for f in fs:
           if last_input_file.find(f)<0:
               input_file_path = os.path.join(input_dir, f)

    Popen("windbg -c \".load pykd.pyd;!py " + os.path.join(os.getcwd(), "p.py " + input_file_path.split("\\")[
        -1]) + "\" -o C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\Acrord32.exe " + input_file_path,shell=True)
    #os.system("windbg -c \".load pykd.pyd;!py "+os.path.join(os.getcwd(),"p.py "+input_file_path.split("\\")[-1])+"\" -o C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\Acrord32.exe "+input_file_path)
    time.sleep(13)
    kill_windbg(1,2)
    return input_file_path

def delete_old_input(f):
    os.remove(f)
def generate_new(a,b):
    while True:
        try:
            generate.generate()
            print "generate right"
            if len(os.listdir(input_dir)) > 5:
                time.sleep(30)
            else:
                time.sleep(2)
        except:
            traceback.print_exc()
if __name__=="__main__":
    #thread.start_new_thread(generate_new, (1, 2))
    #thread.start_new_thread(generate_new, (1, 2))
    last_input_file=None
    while True:
        try:
            while not next_gate or len(os.listdir(input_dir))<=1:
                time.sleep(4)
                print "waiting"
            #new_file_path=os.path.join(input_dir,datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".pdf")
            #generate.generate_new()#sample_path,new_file_path,u3djs_path,u3d1js_path,page0js_path)
            input_file=fuzzer(last_input_file)
            if last_input_file:
                delete_old_input(last_input_file)
            last_input_file=input_file
        except:
            traceback.print_exc()