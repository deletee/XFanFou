# -*- coding: utf-8 -*-
HelpInfo='''
################################################################################
# XFanFou Script to Craw fanfou.com  what he/she/it say                        #
# (Tested with Python 2.7)                                                     #
#                                                                              #
# @author: JingJ XI                                                            #
# @user get you want to craw                                                   #
# @pages how many page need to craw                                            #
# @Example: XFanFou.exe -u RLhcIDBjZAM -p 10                                   #
#                                                                              #
################################################################################
'''
import urllib
import urllib2
import cookielib
import sys
import re
from BeautifulSoup import *
"""cookie"""


cookie = cookielib.CookieJar()
chandle = urllib2.HTTPCookieProcessor(cookie)

def get(url):
    r = urllib2.Request(url)
    opener = urllib2.build_opener(chandle)
    u = opener.open(r)
    data = u.read()
    try:
        data = data.decode('utf-8')
    except:
        data = data.decode('gbk','ignore')
    return data

def post(url, data):
    data = urllib.urlencode(data)
    #data = bytes(data,'utf-8')
    r = urllib2.Request(url,data)
    opener = urllib2.build_opener(chandle)
    u = opener.open(r)
    data = u.read()
    try:
        data = data.decode('utf-8')
    except:
        data = data.decode('gbk','ignore')
    return data

def login():
    rpar = {
                'loginname':'zerohero.xij@qq.com',
                'loginpass':'Aster4data',
                'action':'login',
                'token':'1cfc87a2'
                }
    loginUrl="http://fanfou.com/login"
    post(loginUrl,rpar)
    
def writeFile(path,content):
    try:
        fp = open(path,'w')
        fp.write(content)
    except IOError:
        fp.close() 

def craw(user,pageid):
    print '\n------>Page:%d <------\n'%pageid
    
    visitUrl="http://fanfou.com/%s/p.%d" % (user,pageid)
    r = get(visitUrl)
    
    soup = BeautifulSoup(r)
    
    contents = soup('span')
    ncon=[]
    ntime=[]
    for con in contents:
        if ('class' in dict(con.attrs)):
            if con['class']=='content' :
                ncon.append(str(con)[22:][:-7])
            if con['class']=='stamp' :
                ntime.append(str(con)[72:88])
            
    for i in range(len(ncon)):
        print (ntime[i]+' '+ncon[i])
        f=open(user+'.txt','a')
        f.write(ntime[i]+' '+ncon[i]+'\n')
        f.close()

if __name__ == '__main__':
    
    paraList={}
    user=None
    pages=None
    if len(sys.argv)<4:
        print "\nHELP:"
        print HelpInfo
    else:
        paraList[sys.argv[1]]=sys.argv[2]
        paraList[sys.argv[3]]=sys.argv[4]   
    
    if paraList.has_key('-u'):
        user=paraList['-u']
    if paraList.has_key('-p'):
        pages=paraList['-p']
    if user and pages:
        f=open(user+'.txt','w')
        f.write("")
        login()
        for i in range(1,int(pages)):
            craw(user,i)
