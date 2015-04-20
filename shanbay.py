#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

'''
Read the volcabulary from shanbay.com
'''

import cookielib, urllib2, urllib, Cookie
try:
    import json
except ImportError:
    import simplejson as json

cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
headers = {
    'User-Agent' : r'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Cookie': '',
    'Referer': 'http://www.shanbay.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.shanbay.com',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json; charset=UTF-8',
}
#opener.handle_open["http"][0].set_http_debuglevel(1)

recookie = r'__utma=183787513.2091977854.1427359326.1427531029.1427536942.3; __utmz=183787513.1427359326.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); csrftoken=knTmF44uCmfFxfD4aS0xrrKihyUcieM4; sessionid=fldcwgfjmw3fnjkpmad9l6x3g0qlcity; __utmc=183787513; __utmb=183787513.10.10.1427536942; __utmt=1; userid=16474156; language_code=zh-CN'

lmcookie = r'__utma=183787513.2091977854.1427359326.1427549242.1427603481.6; __utmz=183787513.1427359326.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); csrftoken=UztMeDCGsibDvcosbOv19dCG8WoQSpYW; sessionid=0by04k4sto4do3sj2y2r9futtjirfa19; __utmb=183787513.7.10.1427603481; __utmc=183787513; __utmt=1; userid=15137458;'

def getCookieFromFile():
    global headers
    from os import path
    userFolder = path.expanduser('~')
    configFolder = path.join(userFolder, '.lshanbay')
    configFile = path.join(configFolder, 'cookie.txt')
    try:
        with open(configFile,'r') as f:
            cookie = f.read()
    except:
        print 'What\'s wrong with your cookie.txt?'
        cookie = ''
    print cookie
    headers['Cookie'] = cookie
    print headers['Cookie']

def addHttpHeaders(*request):
    for name, values in headers.items():
        request[0].add_header(name, values)

shanbaybdc = 'http://www.shanbay.com/api/v1/bdc/'

def createResponse(url, data={}, method=lambda: 'GET'):
    jsdata = json.dumps(data)
    request = urllib2.Request(url,jsdata)
    request.get_method = method
    for name, values in headers.items():
        request.add_header(name, values)
    response = opener.open(request)
    return response

def searchFromShanbay(volcabulary):
    request = urllib2.Request(shanbaybdc+'search/?word='+volcabulary)
    addHttpHeaders(request)
    try:
        response = opener.open(request)
    except:
        print 'What\'s wrong with your network?'
        return {}
    data = json.loads(response.read())
    c = Cookie.SimpleCookie()
    c.load(response.info().getheader('Set-Cookie'))
    data['userid'] = c['userid'].value
    return data

def learnOnShanbay(wordid):
    lvalues = {'id':wordid, 'content_type':'vocabulary'}
    data = json.dumps(lvalues)
    print data
    lrequest = urllib2.Request(shanbaybdc + 'learning/',data)
    lrequest.get_method = lambda:'POST'
    addHttpHeaders(lrequest)
    try:
        response = opener.open(lrequest)
    except:
        print 'What\'s wrong with your network?'
        raise
        return {}
    data = json.loads(response.read())
    return data

def relearnOnShanbay(learnid):
    rlvalues = {'retention':1}
    data = json.dumps(rlvalues)
    rlrequest = urllib2.Request(shanbaybdc + '/learning/%d' % learnid, data)
    rlrequest.get_method = lambda:'PUT'
    addHttpHeaders(rlrequest)
    try:
        response = opener.open(rlrequest)
    except:
        print 'What\'s wrong with your network?'
        raise
        return {}
    data = json.loads(response.read())
    return data

def printhr(userid=''):
    print '%s%s%s' % ('-'*10, 'UserId: %10s' % userid if userid!='' else '-'*20, '-'*10)

def run():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    args = sys.argv
    if (len(args)==1):
        volcabulary = raw_input()
    else:
        volcabulary = args[1]
    global cookie
    cookie = getCookieFromFile()

    data = searchFromShanbay(volcabulary)
    val = data.get('data',{})
    userid = data.get('userid','')
    printhr(userid)
    if data.get('status_code',1) != 0:
        print 'Unknow word!'
        printhr()
    else:
        print '%s> %s [%s]' % ('-'*(val.get('retention',0)+1),volcabulary, val.get('pronunciation','...'))
        print val.get('definition','Undefined...')
        printhr()
        en_def = val.get('en_definitions',{})
        examples = en_def.get('n',{})
        if (len(examples)>0):
            print 'Example sentence:'
            for index in xrange(len(examples)):
                print '- %d: %s' % (index+1, examples[index])
            printhr()
        if userid!='':
            learning_id = val.get('learning_id',0)
            s = raw_input('%s for you, learn it? [Y] for yes: '\
                % ('An old word' if learning_id else 'A new word'))
            if s.lower()=='y':
                if learning_id!=0:
                    data = relearnOnShanbay(learning_id)
                else:
                    data = learnOnShanbay(val.get('id',0))
                status = data.get('status_code',1)
                if status!=0:
                    print 'Sorry, Failed...'
                else:
                    print 'Success~~~'
            printhr()

if (__name__ == '__main__'):
    run()
