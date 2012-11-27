# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: basedisplay.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-11-12 10:52:46
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql
from mylog import log
from django.utils import simplejson
from functions import trim_csv,verifyData
confsql=confsql.Confsql()
def import_basedisplay(request):
    '订货量修改规则导入'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=5)
        rs2,rs1=verifyData(rs1,length=5,required=[0,2,4])

        '重复项覆盖'
        temp=[]
        for rs in rs1:
            sqlstr=u"select * from basedisplay where braid='"+rs[0]+"' and proid='"+rs[2]+"'"
            if confsql.checkExist(sqlstr)==1: #检查braid,proid数据库是否已存在
                rs.append(u'数据库已存在!')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='1000'><tr><th>门店代码</th><th>门店名称</th><th>商品代码</th><th>商品名称</th><th>基本陈列量</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[5] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/import_basedisplay.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_basedisplay(request):
    '保存订货量修改规则'
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])

    for rs in rs1:
        if rs[5]<>'':
            if rs[5]==u'数据库已存在!':
                try:
                    confsql.runSql("update basedisplay set basedisplay='"+rs[4]+"' where braid='"+rs[0]+"' and proid='"+rs[2]+"'")
                    rs[5]='插入成功!'
                except:
                    rs[5]='插入失败!'
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['proid']=rs[2]
                res['proname']=rs[3]
                res['basedisplay']=rs[4]
                res['info']=rs[5]
                result.append(res)
            else:
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['proid']=rs[2]
                res['proname']=rs[3]
                res['basedisplay']=rs[4]
                res['info']=rs[5]
                result.append(res)
        else: #无误的
            try:
                confsql.runSql("insert into basedisplay(braid,proid,basedisplay) values('"+rs[0]+"','"+rs[2]+"','"+rs[4]+"')")
                rs[5]='插入成功!'
            except:
                rs[5]='插入失败!'
            res={}
            res['braid']=rs[0]
            res['braname']=rs[1]
            res['proid']=rs[2]
            res['proname']=rs[3]
            res['basedisplay']=rs[4]
            res['info']=rs[5]
            result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_basedisplay(request):
    '查询订货量修改规则'
    t=get_template('mana1/insult_basedisplay.html')
    sqlstr="""
        select t1.braid,t3.braname,t1.proid,t2.proname,t1.basedisplay 
        from basedisplay t1 left join product_all t2 
        on t1.proid=t2.proid left join branch t3 on t1.braid=t3.braid
        group by t1.braid,t3.braname,t1.proid,t2.proname,t1.basedisplay 
    """
    result=confsql.runquery(sqlstr)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

def delete_basedisplay(request):
    '删除订货规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=5)
        rs2,rs1=verifyData(rs1,length=5,required=[0,2,4])

        html=u"<table width='1000'><tr><th>门店代码</th><th>门店名称</th><th>商品代码</th><th>商品名称</th><th>基本陈列量</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[5] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/delete_basedisplay.html')
        html=t.render(Context())
        return HttpResponse(html)


def deleteData_basedisplay(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],itemlenth=0)
    if len(rs1)>0:
        for rs in rs1:
            if rs[5]<>'': #出错信息的保留
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['proid']=rs[2]
                res['proname']=rs[3]
                res['basedisplay']=rs[4]
                res['info']=rs[5]
                result.append(res)
            else:
                try:
                    sqlstr=u"delete from basedisplay where braid='"+rs[0]+"' and proid='"+rs[2]+"'"
                    confsql.runSql(sqlstr)
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['proid']=rs[2]
                    res['proname']=rs[3]
                    res['basedisplay']=rs[4]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['proid']=rs[2]
                    res['proname']=rs[3]
                    res['basedisplay']=rs[4]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

