# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: delivery.py
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

def import_sku(request):
    ''' 配送日期导入 '''
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value, itemlenth=3) #去除行尾多余换行符 rs1存放初始值
        rs2,rs1=verifyData(rs1,length=3,required=[0])

        #数据库已存在给予提示
        temp=[]
        for rs in rs1:
            if confsql.checkExist(u"select * from sku where 门店代码='"+rs[0]+"'")==1:
                temp.append(rs)
                rs.append(u'数据库已存在!')
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '门店代码商品代码 长度检查'
        temp=[]
        for rs in rs1:
            if len(rs[0])<>5: #门店代码 5位
                rs.append(u'门店代码长度必须为5位！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='800'><tr><th>门店代码</th><th>门店名称</th><th>店面面积</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td style='background-color:yellow;'>" + rs[3] + "</td>"
                html+="</tr>"
        #log(rs1)
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(html)
    else:
        t=get_template('mana1/import_sku.html')
        html=t.render(Context())
        return HttpResponse(html)

def insult_sku(request):
    ''' 配送日查询 '''
    result=[] #存放初始表头
    if request.method=='POST':
        yuedu=request.POST['yuedu']
        sqlstr=u"select 门店代码,门店名称,店面面积,sku总数,流通品牌,自有品牌,彩妆l,彩妆z,护肤l,护肤z,化妆工具l,化妆工具z,美发护理l,美发护理z,男士护理l,男士护理z,日用品l,日用品z,身体护理l,身体护理z,婴童护理l,婴童护理z,食品l,食品z from skuVal where 月度='"+yuedu+"'"
        result=confsql.runquery(sqlstr)
        t=get_template('mana1/insult_sku.html')
        html=t.render(Context({'result':result}))
        return HttpResponse(html)
    else:
        t=get_template('mana1/insult_sku.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_sku(request):
    '''配送规则导入检查并插入数据库'''
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])

    for rs in rs1:
        if rs[3]<>'':
            if rs[3]==u'数据库已存在':
                try:
                    sqlstr =u"delete from sku where 门店代码='"+rs[0]+"';"
                    sqlstr +="insert into sku(门店代码,门店名称,店面面积) values('"+rs[0]+"','"+rs[1]+"','"+rs[2]+"') "
                    confsql.runSql(sqlstr)
                    rs[3]=u'插入成功!'
                except:
                    rs[3]=u'插入失败!'
            else:
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['mianji']=rs[2]
                    res['info']=rs[3]
                    result.append(res)
        else:
            try:
                sqlstr=u"insert into sku(门店代码,门店名称,店面面积) values('"+rs[0]+"','"+rs[1]+"',"+rs[2]+")"
                confsql.runSql(sqlstr)
                rs[3]=u'插入成功!'
            except:
                rs[3]=u'插入失败!'
            res={}
            res['braid']=rs[0]
            res['braname']=rs[1]
            res['mianji']=rs[2]
            res['info']=rs[3]
            result.append(res)

    jsonres=simplejson.dumps(result)
    return  HttpResponse(jsonres)

def delete_sku(request):
    '删除配送规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=3)
        rs2,rs1=verifyData(rs1,length=3,required=[0,1])

        html=u"<table width='800'><tr><th>门店代码</th><th>门店名称</th><th>门店面积</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td style='background-color:yellow;'>" + rs[3] + "</td>"
                html+="</tr>"
        #log(rs1)
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(html)
    else:
        t=get_template('mana1/delete_sku.html')
        html=t.render(Context())
        return HttpResponse(html)


def deleteData_sku(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],itemlenth=0)
    if len(rs1)>0:
        for rs in rs1:
            if rs[3]<>'': #出错信息的保留
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['mianji']=rs[2]
                res['info']=rs[3]
                result.append(res)
            else:
                try:
                    sqlstr=u"delete from sku where 门店代码='"+rs[0]+"'"
                    confsql.runSql(sqlstr)
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['mianji']=rs[2]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['mianji']=rs[2]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

