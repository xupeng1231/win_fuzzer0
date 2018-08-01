import time
import redis
import traceback
import os
import hashlib

pool=redis.ConnectionPool(host="192.168.4.2",port="6379",decode_responses=True)

def init_name():
    if os.path.exists("name.txt"):
        return
    while True:
        try:
            r=redis.Redis(connection_pool=pool)
            vname=r.get("thisvname")
            if not vname is None:
                with open("name.txt", "wt") as idf:
                    idf.write(vname)
                break
            time.sleep(2)
        except:
            traceback.print_exc()
            pass


def get_name():
    with open("name.txt","rt") as idf:
        vname=idf.read()
    return vname


def beat():
    vname=get_name()
    for _ in range(4):
        try:
            r = redis.Redis(connection_pool=pool)
            r.set(vname, str(time.time()))
            break
        except:
            traceback.print_exc()
            pass


def report_crash(crash):
    hash=hashlib.md5()
    hash.update(crash)
    md5=hash.hexdigest()
    for _ in range(4):
        try:
            r = redis.Redis(connection_pool=pool)
            md5_len=int(r.llen("crashes_md5"))
            for i in range(0,md5_len):
                if md5 == r.lindex("crashes_md5",i):
                    print "already existed!!"
                    return
            r.rpush("crashes",crash)
            r.rpush("crashes_md5",md5)
            break
        except:
            traceback.print_exc()
            pass


if __name__=="__main__":
    init_name()
    beat()
    report_crash("crash---")