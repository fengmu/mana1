# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: tranedit.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-28 18:29:10
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql,datetime,memcache
from django.utils import simplejson
import functions
from mylog import log


def tranedit(request):

    myValue = request.POST["value"].encode("utf-8")

    myValuelist = functions.fmwConvertList(myValue, '\n')

    myValuelist2 = [ functions.fmwConvertList(x, '\t') for x in myValuelist]

    myValuelist2.pop(0)    #标题

    myNewValue =  functions.fmw2Htmltable(myValuelist2)

    return HttpResponse(myNewValue)



