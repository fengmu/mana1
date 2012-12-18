# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: sugvalue.py
#         Desc: 配送相关
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-24 14:21:51
#      History:
#=============================================================================
'''
import confsql,datetime,memcache
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.utils import simplejson
from mylog import log
from functions import trim_csv,verifyData

confsql=confsql.Confsql()
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def insult_sugvalue(request):
    ''' 建议值查询界面 '''
    result=[] #存放初始表头
    sqlstr="select mdcode, mdname, spcode, spname, suggest, suggestcost  from dhalldata where assortment is not null and status < '5' and suggest > 0 and shelf > '-1' and dhtag='T' and delivery = 'T'"
    lines=confsql.runquery(sqlstr)
    for rs in lines:
        res={}
        res['braid']=rs[0]
        res['braname']=rs[1]
        res['proid']=rs[2]
        res['proname']=rs[3]
        res['suggest']=rs[4]
        res['suggestcost']=rs[5]
        result.append(res)
    t=get_template('mana1/insult_sugvalue.html')
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

