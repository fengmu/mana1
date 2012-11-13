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

def import_delivery(request):
    ''' 配送日期导入 '''
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value, itemlenth=3) #去除行尾多余换行符 rs1存放初始值
        rs2,rs1=verifyData(rs1,length=3,required=[0,2],delivery=1)
        
        #数据库已存在给予提示
        temp=[]
        for rs in rs1:
            if confsql.checkExist("select * from delivery where braid='"+rs[0]+"' and weekdelivery='"+rs[2]+"'")==1:
                temp.append(rs)
                rs.append(u'数据库已存在!')
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='800'><tr><th>门店代码</th><th>门店名称</th><th>配送日</th></tr>"
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
        t=get_template('mana1/import_delivery.html')
        html=t.render(Context())
        return HttpResponse(html)

def insult_delivery(request):
    ''' 配送日查询 '''
    result=[] #存放初始表头
    if request.method=='POST':
        jlist=simplejson.loads(request.POST["jsonlist"])
        if jlist['braid']<>'' or jlist['weekdelivery']<>'' or jlist['braname']<>'': #不全为空
            sqlstr='select braid,braname,weekdelivery,adddate from (select t1.braid,t2.braname,t1.weekdelivery,t1.adddate from delivery t1,branch t2 where t1.braid=t2.braid) t1 where '
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
            lines=confsql.runquery(sqlstr)
            for rs in lines:
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['weekdelivery']=rs[2]
                res['adddate']=rs[3]
                result.append(res)
            jsonres=simplejson.dumps(result)
            return  HttpResponse(jsonres)
        else: #全为空，查询所有
            sqlstr='select t1.braid,t2.braname,t1.weekdelivery,t1.adddate from delivery t1,branch t2 where t1.braid=t2.braid'
            lines=confsql.runquery(sqlstr)
            for rs in lines:
                res={}
                res['braid']=rs[0]
                res['braname']= rs[1]
                res['weekdelivery']=rs[2]
                res['adddate']=rs[3]
                result.append(res)
            jsonres=simplejson.dumps(result)
            return  HttpResponse(jsonres)
    else:
        t=get_template('mana1/insult_delivery.html')
        html=t.render(Context({'result':result}))
        return HttpResponse(html)

def save_delivery(request):
    '''配送规则导入检查并插入数据库'''
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])
    adddate=datetime.datetime.now().strftime('%Y-%m-%d')

    for rs in rs1:
        #log(rs)
        if rs[3]<>'':
            if rs[3]==u'数据库已存在':
                try:
                    #confsql.runSql("update delivery set adddate='"+adddate+"' where braid='"+rs[0]+"' and weekdelivery='"+rs[2]+"'")
                    sqlstr ="delete from delivery where braid='"+rs[0]+"' and weekdelivery='"+rs[2]+"'; "
                    sqlstr +=" insert into delivery(braid,weekdelivery,adddate) values('"+rs[0]+"','"+rs[2]+"','"+adddate+"') "
                    confsql.runSql(sqlstr)
                    rs[3]=u'插入成功!'
                except:
                    rs[3]=u'插入失败!'
            else:
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['weekdelivery']=rs[2]
                    res['adddate']=adddate
                    res['info']=rs[3]
                    result.append(res)
        else:
            try:
                sqlstr="insert into delivery(braid,weekdelivery,adddate) values('"+rs[0]+"','"+rs[2]+"','"+adddate+"')"
                confsql.runSql(sqlstr)
                rs[3]=u'插入成功!'
            except:
                rs[3]=u'插入失败!'
            res={}
            res['braid']=rs[0]
            res['braname']=rs[1]
            res['weekdelivery']=rs[2]
            res['adddate']=adddate
            res['info']=rs[3]
            result.append(res)

    jsonres=simplejson.dumps(result)
    return  HttpResponse(jsonres)

def delete_delivery(request):
    '删除配送规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=3)
        rs2,rs1=verifyData(rs1,length=3,required=[0,2],delivery=1)

        html=u"<table width='800'><tr><th>门店代码</th><th>门店名称</th><th>配送日</th></tr>"
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
        t=get_template('mana1/delete_delivery.html')
        html=t.render(Context())
        return HttpResponse(html)


def deleteData_delivery(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],itemlenth=0)
    adddate=datetime.datetime.now().strftime('%Y-%m-%d')
    if len(rs1)>0:
        for rs in rs1:
            if rs[3]<>'': #出错信息的保留
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['weekdelivery']=rs[2]
                res['adddate']=adddate
                res['info']=rs[3]
                result.append(res)
            else:
                try:
                    sqlstr="delete from delivery where braid='"+rs[0]+"' and weekdelivery='"+rs[2]+"'"
                    confsql.runSql(sqlstr)
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['weekdelivery']=rs[2]
                    res['adddate']=adddate
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['weekdelivery']=rs[2]
                    res['adddate']=adddate
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

