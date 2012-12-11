# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: quehuo.py
#         Desc: 
#       Author: solomon
#        Email: 253376634[at]qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-12-03 13:47:16
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql,datetime
from mylog import log
import datetime

confsql=confsql.Confsql()
def insult_quehuo(request):
    """ 缺货查询 """
    t=get_template('mana1/insult_quehuo.html')
    sqlstr="select mdcode,mdname,barcode,spcode,spname,prodl_id||'_'||prodl as prodl,prozl_id||'_'||prozl as prozl,proxl_id||'_'||proxl as proxl,braxl_id||'_'||braxl as braxl,curqty from dhalldata where assortment='youtu' and curqty<0"
    result=confsql.runquery(sqlstr)
    log(result)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

