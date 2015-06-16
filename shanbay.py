#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

'''
Read the volcabulary from shanbay.com
'''

import cookielib, urllib2, urllib, Cookie, argparse
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
    'DNT': 1,
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json; charset=UTF-8',
}
#opener.handle_open["http"][0].set_http_debuglevel(1)

recookie = r'__utma=183787513.2091977854.1427359326.1427603481.1427606581.7; __utmz=183787513.1427359326.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); csrftoken=mcI0RVgh8efDI1L4FJB704vqlUiVLXOj; sessionid=osvtxf0v6tsewy6ie6znwb8e9ntzohab; __utmc=183787513; __utmb=183787513.5.10.1427606581; __utmt=1; userid=16474156; language_code=zh-CN'

from os import path
userFolder = path.expanduser('~')
configFolder = path.join(userFolder, '.lshanbay')
configFile = path.join(configFolder, 'cookie')

def getCookieFromFile():
    global headers
    try:
        with open(configFile,'r') as f:
            cookie = f.read().strip('\n')
    except:
        print 'What\'s wrong with your cookie.txt?'
        cookie = ''
    headers['Cookie'] = cookie

def writeCookieToFile(cookie):
    try:
        with open(configFile, 'w') as f:
            f.write(cookie)
    except:
        print 'I can\'t change your cookie file.(%s)' % cookieFile
    

shanbaybdc = 'http://www.shanbay.com/api/v1/bdc/'

def getResponse(url, data={}, method=lambda: 'GET'):
    jsdata = json.dumps(data)
    request = urllib2.Request(url,jsdata)
    request.get_method = method
    for name, values in headers.items():
        request.add_header(name, values)
    response = opener.open(request)
    return response

def searchFromShanbay(volcabulary):
    try:
        response = getResponse(shanbaybdc+'search/?word='+volcabulary)
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
    try:
        response = getResponse(shanbaybdc+'learning/',lvalues,lambda: 'POST')
    except:
        print 'What\'s wrong with your network?'
        return {}
    data = json.loads(response.read())
    return data

def relearnOnShanbay(learnid):
    rlvalues = {'retention':1}
    try:
        response = getResponse(shanbaybdc+'learning/%d' % learnid, rlvalues,lambda: 'PUT')
    except:
        print 'What\'s wrong with your network?'
        return {}
    data = json.loads(response.read())
    return data

def printhr(userid=''):
    print '%s%s%s' % ('-'*10, ' UserId: %10s ' % userid if userid!='' else '-'*20, '-'*10)

def retentionize(val = 0):
    l = ['▃','▄','▅','▆','▇','█','','','','','']
    l[val] = chr(48+val)
    s = '-' + ''.join(l) + '-'
    return s

def run():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    args = sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument('volcabulary', help='Volcabulary you want to change. ', nargs='?')
    parser.add_argument('-c', '--cookie', default='cookie', help='Change the cookie storage in the file')
    pargs = parser.parse_args()
    if pargs.cookie!='cookie':
        writeCookieToFile(pargs.cookie)
        return
    if pargs.volcabulary is not None:
        volcabulary = pargs.volcabulary
    else:
        volcabulary = raw_input('Input your volcabulary: ')
    getCookieFromFile()

    data = searchFromShanbay(volcabulary)
    val = data.get('data',{})
    userid = data.get('userid','')
    printhr(userid)
    if data.get('status_code',1) != 0:
        print 'Unknow word!'
        printhr()
    else:
        print '-> %s [%s] %s' % (val.get('content',volcabulary), val.get('pronunciation','...'),retentionize(val.get('retention',0)) if userid!='' else '')
        print val.get('definition','Nothing...')
        printhr()
        en_def = val.get('en_definitions',{})
        en_array = en_def.get('n',{})
        if (len(en_array)>0):
            print 'Definitions in English:'
            for index in xrange(len(en_array)):
                print '- %d: %s' % (index+1, en_array[index])
            printhr()
        if userid!='':
            learning_id = val.get('learning_id',0)
            s = raw_input('%s for you, learn it? [Y] for yes: '\
                % ('An OLD word' if learning_id else 'A NEW word'))
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
