#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

'''
Read the volcabulary from shanbay.com
'''

def getFromShanbay(volcabulary):
    import urllib2
    try:
        import json
    except ImportError:
        import simplejson as json
    shanbay = 'https://api.shanbay.com/'
    wordQueryURL = shanbay+'bdc/search/?word='+volcabulary
    try:
        response = urllib2.urlopen(wordQueryURL)
    except:
        print 'What\'s wrong with your network?'
        return {}
    data = json.loads(response.read())
    return data

def run():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    args = sys.argv
    if (len(args)==1):
        volcabulary = raw_input()
    else:
        volcabulary = args[1]
    data = getFromShanbay(volcabulary)
    print '-' * 40
    if data.get('status_code',1) != 0:
        print 'Unknow word!'
    else:
        val = data.get('data',{})
        print '-> %s [%s]' % (volcabulary, val.get('pronunciation','...'))
        print val.get('definition','Undefined...')
    print '-' * 40

if (__name__ == '__main__'):
    run()
