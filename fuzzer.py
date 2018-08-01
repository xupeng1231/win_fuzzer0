import os
import time
import traceback
from subprocess import Popen

sample_path=os.path.join(os.getcwd(),"sample","sample.pdf")
input_dir=os.path.join(os.getcwd(),"input")
if not os.path.exists(sample_path):
    print "ERROR:sample not exist!!!"
    os._exit(0)
if not os.path.exists(input_dir):
    os.makedirs(input_dir)


def kill_windbg(a,b):
    while True:
        res=os.system("taskkill /F /IM windbg.exe")
        if 0 == res:
            break
        print "KILL ERROR!!!"
        time.sleep(1)


def fuzzer(last_input_file):
    fs=os.listdir(input_dir)
    if not last_input_file:
        input_file_path = os.path.join(input_dir, fs[0])
    else:
        for f in fs:
           if last_input_file.find(f)<0:
               input_file_path = os.path.join(input_dir, f)

    Popen("windbg -c \".load pykd;!py " + os.path.join(os.getcwd(), "p.py " + input_file_path.split("\\")[
        -1]) + "\" -o C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\Acrord32.exe " + input_file_path,shell=True)
    #os.system("windbg -c \".load pykd.pyd;!py "+os.path.join(os.getcwd(),"p.py "+input_file_path.split("\\")[-1])+"\" -o C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\Acrord32.exe "+input_file_path)
    time.sleep(13)
    kill_windbg(1,2)
    return input_file_path


if __name__=="__main__":
    Popen(args=["python", "generate.py"])
    Popen(args=["python", "myreport.py"])
    last_input_file=None
    while True:
        try:
            while len(os.listdir(input_dir))<=1:
                time.sleep(2)
                print "waiting"
            input_file = fuzzer(last_input_file)
            if last_input_file:
                os.remove(last_input_file)
            last_input_file=input_file
        except:
            traceback.print_exc()