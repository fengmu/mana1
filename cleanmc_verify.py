# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: cleanmc_verify.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-28 18:31:50
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

confsql=confsql.Confsql()

mc = memcache.Client(['127.0.0.1:11211'], debug=0)


def cleanmc_verify(request): #审核处理清空内存建议值

    

    myjson = simplejson.loads(request.POST["myjson"])

    rs1=functions.trim_csv(myjson["table"],7)

    s=[] #存放门店名单

    for rs in rs1:

        if rs[0]=="1": #勾选的门店

            s.append(rs[1])

    html=""

    if len(s)>0:

        for rs in s:

            #清空数据库指定建议值及内存指定建议值

            result=confsql.runquery("select * from sugvalue where braid='"+str(rs)+"'")

            for rs in result:

                mc.delete(str(rs['braid'])+"__"+str(rs['proid'])+"__sugvalue") #先根据数据库清内存

                confsql.runquery("delete from sugvalue where braid='"+str(rs['braid'])+"'") #后清数据库

                confsql.runquery("delete from brainfo where 门店代码='"+str(rs['braid'])+"'") 

        result=confsql.runquery("select * from brainfo") #获取门店综合信息 供门店审核是否需要重写

        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"

        for rs in result:

            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"

        return HttpResponse(html)

    else:

        #全部重写

        result=confsql.runquery("select * from sugvalue")

        for rs in result:

            mc.delete(str(rs['braid'])+"__"+str(rs['proid'])+"__sugvalue")

        confsql.runquery("delete from sugvalue")

        confsql.runquery("delete from brainfo")

        result=confsql.runquery("select * from brainfo") #获取门店综合信息 供门店审核是否需要重写

        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"

        for rs in result:

            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"

        return HttpResponse(html)


