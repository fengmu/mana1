#!coding:utf8
'''
#=============================================================================
#     FileName: shangxiaxian.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-23 11:50:41
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql
from django.utils import simplejson
from mylog import log

confsql=confsql.Confsql()
def insult_shangxiaxian(request):
    '程序计算上下限结果查询'
    if request.method=='POST':
        result=[]
        mendian=request.POST['mendian']
        res=confsql.runquery(sqlstr=" select t1.braid,t1.mdname,t1.proid,t1.spname,t1.prodl_id||'_'||t1.prodl,t1.prozl_id||'_'||t1.prozl,t1.proxl_id||'_'||t1.proxl,week1_amt,week2_amt,week3_amt,week4_amt,t1.maxval,t1.minval,t1.oldmaxval,t1.oldminval from xiaoshou28_maxmin t1 where braid='"+mendian+"' limit 20000")
        for rs in res:
            items={}
            items['braid']=rs[0]
            items['braname']=rs[1]
            items['proid']=rs[2]
            items['proname']=rs[3]
            items['prodl']=rs[4]
            items['prozl']=rs[5]
            items['proxl']=rs[6]
            items['week1_amt']=rs[7]
            items['week2_amt']=rs[8]
            items['week3_amt']=rs[9]
            items['week4_amt']=rs[10]
            items['maxval']=int(rs[11] or 0)
            items['minval']=int(rs[12] or 0)
            items['oldmaxval']=int(rs[13] or 0)
            items['oldminval']=int(rs[14] or 0)
            result.append(items)
        jsonres=simplejson.dumps(result)
        return  HttpResponse(jsonres)
    else:
        t=get_template('mana1/insult_shangxiaxian.html')
        html=t.render(Context())
        return HttpResponse(html)


