#!coding:utf8
'''
#=============================================================================
#     FileName: quantou.py
#         Desc: 拳头商品
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-22 14:36:27
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

def save_quantou(request):
    '保存拳头产品'
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])

    for rs in rs1:
        if rs[2]==u'数据库已存在!':
            try:
                confsql.runSql("delete from quantou where proid='"+rs[0]+"'")
            except:
                rs[2]=u'删除失败!'
        try:
            confsql.runSql("insert into quantou values('"+rs[0]+"','"+datetime.date.today().strftime("%Y-%m-%d")+"')")
            rs[2]=u'插入成功!'
        except:
            rs[2]=u'插入失败!'
        res={}
        res['proid']=rs[0]
        res['proname']=rs[1]
        res['info']=rs[2]
        result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_quantou(request):
    '查询拳头商品'
    t=get_template('mana1/insult_quantou.html')
    sqlstr='select t1.proid,t2.proname,t1.adddate from quantou t1 left join product_all t2 on t1.proid=t2.proid'
    result=confsql.runquery(sqlstr)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

def import_quantou(request):
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=2)
        rs2,rs1=verifyData(rs1,length=2,required=[0])

        '重复项覆盖'
        temp=[]
        if len(rs1)>0:
            for rs in rs1:
                if confsql.checkExist("select * from quantou where proid='"+rs[0]+"'")==1: #检查数据库是否已存在
                    temp.append(rs)
                    rs.append(u'数据库已存在!')
                    rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='400'><tr><th>商品代码</th><th>商品名称</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[2] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/import_quantou.html')
        html=t.render(Context())
        return HttpResponse(html)


def delete_quantou(request):
    '删除订货规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=2)
        rs2,rs1=verifyData(rs1,length=2,required=[0])

        html=u"<table width='400'><tr><th>商品代码</th><th>商品名称</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[2] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/delete_quantou.html')
        html=t.render(Context())
        return HttpResponse(html)

def deleteData_quantou(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],itemlenth=0)
    if len(rs1)>0:
        for rs in rs1:
            if rs[2]<>'': #出错信息的保留
                res={}
                res['proid']=rs[0]
                res['proname']=rs[1]
                res['info']=rs[2]
                result.append(res)
            else:
                try:
                    res={}
                    sqlstr=u"delete from quantou where proid='"+rs[0]+"'"
                    confsql.runSql(sqlstr)
                    res={}
                    res['proid']=rs[0]
                    res['proname']=rs[1]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res={}
                    res['proid']=rs[0]
                    res['proname']=rs[1]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

