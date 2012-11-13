# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: check_advmaxmin.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-28 18:29:54
#      History:
#=============================================================================
'''
import datetime

from django.template.loader import get_template

from django.template import Context

from django.http import HttpResponse

import confsql,datetime,memcache

from django.utils import simplejson

#import writemc

import functions
from mylog import log


confsql=confsql.Confsql()

mc = memcache.Client(['127.0.0.1:11211'], debug=0)


def check_advmaxmin(request):

    fmdata = simplejson.loads(request.POST["myjson"])

    fmdatatag = fmdata["tag"]

    fmdatalist= functions.fmwConvertList(fmdata["table"].encode("utf-8"), '\n')

    fmdatalist2 = [ functions.fmwConvertList(x, '\t') for x in fmdatalist]

    fmdatalist2.pop(0)

    tag_fmdata   = [ x for x in fmdatalist2 if x[0] =="1"]

    notag_fmdata = [ x for x in fmdatalist2 if x[0] =="0"]

    if fmdatatag == 'del':

        setadvMaxMin(tag_fmdata)

        myNewValue = functions.fmw2Htmltable(notag_fmdata)

    elif fmdatatag == 'save':
        

        updateMaxMin(tag_fmdata)

        tag_fmdata2 = [ x + ["数据已保存"] for x in tag_fmdata]

        myNewValue = functions.fmw2Htmltable(tag_fmdata2+notag_fmdata)

        #myNewValue = str(tag_fmdata2)

    else:

        myNewValue = functions.fmw2Htmltable([])

    return HttpResponse(myNewValue)


def setadvMaxMin(datalist):
    remarks = 'del'
    verifydate = datetime.datetime.now().strftime('%Y-%m-%d')

    for x in datalist:

        #cachedAdvMaxMin(x[1], x[3], x[5], x[6], x[7], x[8])
        confsql.insertAdvMaxMin(x[1], x[3], x[5], x[6], x[7], x[8], x[9], verifydate, remarks)


def updateMaxMin(datalist):
    remarks = 'save'
    verifydate = datetime.datetime.now().strftime('%Y-%m-%d')

    for x in datalist:        
        confsql.maxmin_update(x[1], x[3], x[5], x[6], x[7], x[8])
        confsql.insertAdvMaxMin(x[1], x[3], x[5], x[6], x[7], x[8], x[9], verifydate, remarks)


def cachedAdvMaxMin(mdcode, spcode, oldmax, oldmin, newmax, newmin):

    advMaxMin = mc.get("advMaxMin")

    myvalue = str(mdcode) +"__"+ spcode + "__" + oldmax + "__" + oldmin +"__"+ newmax +"__"+ newmin  #这里有陷阱，首选必须用str

    if not advMaxMin :

        mc.set("advMaxMin", myvalue)

    else:

        mc.append("advMaxMin", ","+myvalue)

