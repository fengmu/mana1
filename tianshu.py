# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: tianshu.py
#         Desc: 配货天数
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-11-16 09:29:19
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql
import datetime
from mylog import log
from django.utils import simplejson
from functions import trim_csv,verifyData
confsql=confsql.Confsql()

def save_tianshu(request):
    '保存拳头产品'
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])

    for rs in rs1:
        if rs[4]==u'数据库已存在!':
            try:
                confsql.runSql("delete from tianshu where braid='"+rs[0]+"'")
            except:
                rs[4]=u'删除失败!'
        try:
            confsql.runSql("insert into tianshu values('"+rs[0]+"','"+rs[2]+"','"+rs[3]+"','"+datetime.date.today().strftime("%Y-%m-%d")+"')")
            rs[4]=u'插入成功!'
        except:
            rs[4]=u'插入失败!'
        res={}
        res['braid']=rs[0]
        res['braname']=rs[1]
        res['anquankucun']=rs[2]
        res['peisongzhouqi']=rs[3]
        res['info']=rs[4]
        result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_tianshu(request):
    '查询拳头商品'
    t=get_template('mana1/insult_tianshu.html')
    sqlstr='select t1.braid,t2.braname,t1.anquankucun,t1.peisongzhouqi,t1.adddate from tianshu t1 left join branch t2 on t1.braid=t2.braid'
    result=confsql.runquery(sqlstr)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

def import_tianshu(request):
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=4)
        rs2,rs1=verifyData(rs1,length=4,required=[0,2,3])

        '重复项覆盖'
        temp=[]
        if len(rs1)>0:
            for rs in rs1:
                if confsql.checkExist("select * from tianshu where braid='"+rs[0]+"'")==1: #检查数据库是否已存在
                    temp.append(rs)
                    rs.append(u'数据库已存在!')
                    rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='800'><tr><th>门店代码</th><th>门店名称</th><th>安全库存天数</th><th>送货周期天数</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[4] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/import_tianshu.html')
        html=t.render(Context())
        return HttpResponse(html)


def delete_tianshu(request):
    '删除订货规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=4)
        rs2,rs1=verifyData(rs1,length=4,required=[0,2,3])

        html=u"<table width='800'><tr><th>门店代码</th><th>门店名称</th><th>安全库存天数</th><th>配送周期天数</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[4] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/delete_tianshu.html')
        html=t.render(Context())
        return HttpResponse(html)

def deleteData_tianshu(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],itemlenth=0)
    if len(rs1)>0:
        for rs in rs1:
            if rs[4]<>'': #出错信息的保留
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['anquankucun']=rs[2]
                res['peisongzhouqi']=rs[3]
                res['info']=rs[4]
                result.append(res)
            else:
                try:
                    res={}
                    sqlstr=u"delete from tianshu where braid='"+rs[0]+"'"
                    confsql.runSql(sqlstr)
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['anquankucun']=rs[2]
                    res['peisongzhouqi']=rs[3]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res={}
                    res['proid']=rs[0]
                    res['proname']=rs[1]
                    res['anquankucun']=rs[2]
                    res['peisongzhouqi']=rs[3]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)


