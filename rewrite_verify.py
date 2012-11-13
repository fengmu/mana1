# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: rewrite_verify.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-28 18:31:19
#      History:
#=============================================================================
'''
from django.template.loader import get_template

from django.template import Context

from django.http import HttpResponse

import confsql,datetime,memcache

from django.utils import simplejson

#import writemc

import functions
from mylog import log


def rewrite_verify(request): #审核处理重写

    #os.system("cmd /c D:/django/mysite/mana1/writemc.py")

    myjson = simplejson.loads(request.POST["myjson"])

    rs1=functions.trim_csv(myjson["table"],7)

    s="" #存放门店名单

    for rs in rs1:

        if rs[0]=="1": #勾选的门店

            s+="'"+rs[1]+"',"

    s=s[0:-1]

    #os.system('cmd.exe /c c:/ZSW/memcached/memcached.exe -m 256 -p 11211') #开启内存服务

    html=""

    if s<>"":

        writemc.Writemc(sqlstr=s)

        result=confsql.runquery(u"select * from brainfo where 门店代码 in("+s+")") #获取门店综合信息 供门店审核是否需要重写

        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"

        for rs in result:

            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"

        return HttpResponse(html)

    else:

        writemc.Writemc() #全部重写

        result=confsql.runquery("select * from brainfo") #获取门店综合信息 供门店审核是否需要重写

        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"

        for rs in result:

            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"

        return HttpResponse(html)

