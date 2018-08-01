import os
import sys
import zlib
import re
import parseu3d
import md5
import datetime
import shelve
import struct
import random
import traceback
import time

u3d0 = (0xb3ad, 0xb3b4, 0xb3f1, 0x423b33)
u3d1 = (0x428dbf, 0x428dc5, 0x428e13, 0x458328)
page0js = (0x426585, 0x42658a, 0x426594, 0x428d09)
u3d0js = (0x423b6c, 0x423b71, 0x423b7b, 0x42654a)
u3d1js = (0x45e7a6, 0x45e7ab, 0x45e7b5, 0x46415d)
sample_md5 = "9c0ac904dc35ee28d2ed1aeb7a8b6c18"

def valid_sample(s):
    m = md5.new()
    m.update(s)
    return sample_md5 == m.hexdigest()
def replace_str(sample_str,offset4,compress_str):
    len1=offset4[1]-offset4[0]
    len2=offset4[3]-offset4[2]
    assert(len(compress_str)<=len2)
    lenstr=str(len(compress_str))+" "*(len1-len(str(len(compress_str))))
    compress_str=compress_str+" "*(len2-len(compress_str))
    sample_str = sample_str[0:offset4[0]] + lenstr + sample_str[offset4[1]:]
    sample_str = sample_str[0:offset4[2]] + compress_str + sample_str[offset4[3]:]
    return sample_str
def P(per):
    return random.randint(1,100)<=per

def mutate_uint32(sample_str,offs):
    for off2 in offs:
        a,=struct.unpack("<I",sample_str[off2[0]:off2[1]])
        if P(50):
            r=random.choice([0,1,0xffffffff,0x7fffffff,a+1,a-1,a+1,a-1])
            a=(r if r!=a else random.choice([r+1,r-1]))%0x100000000
        elif P(60):
            a=(a+random.choice([-1,1,-2,2,-3,3,4,5,6,7,8]))%0x100000000
        else:
            a=random.randint(0,0xffffffff)
        a=struct.pack("<I",a)
        sample_str=sample_str[0:off2[0]]+a+sample_str[off2[1]:]
    return sample_str
def generate(sample_str,u3d0_str,u3d1_str,page0js_str,u3d0js_str,u3d1js_str,u3d0_offs,u3d1_offs):

    u3d0_str=mutate_uint32(u3d0_str,random.sample(u3d0_offs,random.randint(8,16)))
    u3d1_str = mutate_uint32(u3d1_str, random.sample(u3d1_offs, random.randint(5, 10)))

    page0js_str="console.println(\"qweq\");"+page0js_str

    u3d0_str=zlib.compress(u3d0_str,9)
    u3d1_str=zlib.compress(u3d1_str,9)
    page0js_str=zlib.compress(page0js_str, 9)
    u3d0js_str = zlib.compress(u3d0js_str, 9)
    u3d1js_str=zlib.compress(u3d1js_str, 9)

    sample_str = replace_str(sample_str, u3d0, u3d0_str)
    sample_str = replace_str(sample_str, u3d1, u3d1_str)
    sample_str = replace_str(sample_str, page0js, page0js_str)
    sample_str = replace_str(sample_str, u3d0js, u3d0js_str)
    sample_str = replace_str(sample_str, u3d1js, u3d1js_str)

    new_file_path = os.path.join("input", datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".pdf")
    with open(new_file_path,"wb") as newf:
        newf.write(sample_str)
    print "generate %s successfully!"%(new_file_path)

def loop_generate():
    with open("sample\\sample.pdf","rb") as samplef:
        sample_str=samplef.read()
    assert (valid_sample(sample_str))

    with open("sample\\tu3d.u3d","rb") as u3d0f:
        u3d0_str=u3d0f.read()
    u3d0_offs=shelve.open("sample\\tu3d_block3b_data_sel.dat")
    u3d0_offs=u3d0_offs["offset"]

    with open("sample\\tu3d1.u3d","rb") as u3d1f:
        u3d1_str=u3d1f.read()
    u3d1_offs=shelve.open("sample\\tu3d1_block3b_data_sel.dat")
    u3d1_offs=u3d1_offs["offset"]

    with open("sample\\page0.js","rb") as page0jsf:
        page0js_str=page0jsf.read()
    with open("sample\\u3d0.js","rb") as u3d0jsf:
        u3d0js_str=u3d0jsf.read()
    with open("sample\\u3d1.js","rb") as u3d1jsf:
        u3d1js_str=u3d1jsf.read()

    while True:
	while len(os.listdir(".\\input"))>=100:
		print "sleeping"
		time.sleep(100)
        try:
            generate(sample_str,u3d0_str,u3d1_str,page0js_str,u3d0js_str,u3d1js_str,u3d0_offs,u3d1_offs)
            time.sleep(6)
        except:
            traceback.print_exc()

if "__main__"==__name__:
    loop_generate()






def find_jsaddr():
    with open("sample\\sample.pdf", "rb") as pdf:
        ss = pdf.read()
    page0js = re.search("\<\<\/Filter\[\/FlateDecode\]\/Length\s(10101)\>\>stream\r\n(.*?)\r\nendstream\r", ss, re.S)
    u3d0js = re.search("\<\<\/Filter\[?\/FlateDecode\]?\/Length\s(10703)\>\>stream\r\n(.*?)\r\nendstream\r", ss, re.S)
    u3d1js = re.search("\<\<\/Filter\[?\/FlateDecode\]?\/Length\s(22952)\>\>stream\r\n(.*?)\r\nendstream\r", ss, re.S)
    print "page0js:",hex(page0js.start(1)),hex(page0js.end(1)),hex(page0js.start(2)),hex(page0js.end(2))
    print "u3d0js:", hex(u3d0js.start(1)), hex(u3d0js.end(1)), hex(u3d0js.start(2)), hex(u3d0js.end(2))
    print "u3d1js:", hex(u3d1js.start(1)), hex(u3d1js.end(1)), hex(u3d1js.start(2)), hex(u3d1js.end(2))

def find_u3daddr():
    pattern=re.compile(r"[\r\n]([0-9]{1,3}\s[0-9]{1,3}\sobj\r?\<\<[^\r\n]*?\>\>)(?:\r|stream\r\n)(.*?)(?:\r\nendstream\r)?endobj",re.S)
    with open("sample\\sample.pdf","rb") as pdf:
        s=pdf.read()
    res=re.finditer(pattern,s)
    if res:
        for r in res:
            #print "*"*20
            if r.group(1).find("Flate")>=0:
                if zlib.decompress(r.group(2))[0:3]=="U3D":
                    print "*******************"*2
                    print "u3d:",hex(r.start(2)),hex(r.end(2))
                    print "u3d:",r.start(2)/16,r.end(2)/16
                    print "u3dl:",hex(r.start(1)+r.group(1).find("Length ")+7),s[r.start(1)+r.group(1).find("Length "):r.start(1)+r.group(1).find("Length ")+15]
                    print "u3dl:", (r.start(1) + r.group(1).find("Length "))/16
                    print r.group(1)

