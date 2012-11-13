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

    if request.method=='POST':
        jlist=simplejson.loads(request.POST["jsonlist"])
        ty=request.POST["ty"]
        if ty=="sub": #非聚集

            if jlist['spcode']<>'' or jlist['spname']<>'' or jlist['mdcode']<>'' or jlist['mdname']<>'': #不全为空

                sqlstr="select mdcode, mdname, spcode, spname, suggest, suggestcost  from dhalldata where assortment is not null and status < '5' and suggest > 0 and shelf > '-1' and dhtag='T' and delivery = 'T' and "

                for j in jlist:

                    if jlist[j]<>'':

                        li=jlist[j].split(",")

                        if len(li)==1:

                            sqlstr+=j+" like '%%"+jlist[j].strip()+"%%' and "

                        else:

                            sqlstr+="("

                            for l in li:

                                sqlstr+=j+" like '%%"+l.strip() +"%%' or  "

                            sqlstr=sqlstr[0:-4]+") and "

                sqlstr=sqlstr[0:-4] #去除最后多余的and

                #sqlstr += " suggest>0 "

                lines=confsql.runquery(sqlstr)

                for rs in lines:

                    res={}

                    res['门店代码']=rs[0]

                    res['门店名称']=rs[1]

                    res['商品代码']=rs[2]

                    res['商品名称']=rs[3]

                    res['建议配货量']=rs[4]

                    res['配货总金额']=rs[5]

                    result.append(res)

                jsonres=simplejson.dumps(result)

                return  HttpResponse(jsonres)

            else:

                #sqlstr='select * from sugvalue'

                sqlstr= "select mdcode, mdname, spcode, spname, suggest, suggestcost  from dhalldata where assortment is not null and status < '5' and suggest > 0 and shelf > '-1' and dhtag='T' and delivery = 'T'"

                lines=confsql.runquery(sqlstr)

                for rs in lines:

                    res={}

                    res['门店代码']=rs[0]

                    res['门店名称']=rs[1]

                    res['商品代码']=rs[2]

                    res['商品名称']=rs[3]

                    res['建议配货量']=rs[4]

                    res['配货总金额']=rs[5]

                    result.append(res)

                jsonres=simplejson.dumps(result)

                return  HttpResponse(jsonres)

        else: #聚集结果

            if jlist['spcode']<>'' or jlist['spname']<>'' or jlist['mdcode']<>'' or jlist['mdname']<>'': #不全为空

                items=""

                dic={'spcode':'商品代码','spname':'商品名称','mdcode':'门店代码','mdname':'门店名称'}

                for j in jlist:

                    if jlist[j]<>'':

                        items+=j+","

                items=items[0:-1]

                sqlstr="select "+items+", sum(suggest) as suggest,sum(suggestcost) as suggestcost from  dhalldata where assortment is not null and status < '5' and suggest > 0 and shelf > '-1' and dhtag='T' and "

                for j in jlist:

                    if jlist[j]<>'':

                        sqlstr+=j+" like '%%"+jlist[j].strip() +"%%' and "

                sqlstr=sqlstr[0:-4] #去除最后多余的and

                #sqlstr += " suggest>0 "

                sqlstr+="group by "+items

                lines=confsql.runquery(sqlstr)

                for rs in lines:

                    i=0

                    res={}

                    for j in jlist:

                        if jlist[j]<>'':

                            res={}

                            res[dic[j]]=rs[i]

                            i+=1

                    res['建议配货量']=rs[i]

                    res['配货总金额']=rs[i+1]

                    result.append(res)

                jsonres=simplejson.dumps(result)

                return  HttpResponse(jsonres)

            else:

                #sqlstr='select * from sugvalue'

                sqlstr='select * from sugvalue where suggest>0 '

                lines=confsql.runquery(sqlstr)

                for rs in lines:

                    res={}

                    res['门店代码']=rs[0]

                    res['门店名称']=rs[1]

                    res['商品代码']=rs[2]

                    res['商品名称']=rs[3]

                    res['建议配货量']=rs[4]

                    res['配货总金额']=rs[5]

                    result.append(res)

                jsonres=simplejson.dumps(result)

                return  HttpResponse(jsonres)

    else:

        t=get_template('mana1/insult_sugvalue.html')

        html=t.render(Context({'result':result}))

        return HttpResponse(html)

