# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: dhrulesYuzhi.py
#         Desc: 
#       Author: solomon
#        Email: 253376634[at]qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-11-29 14:10:38
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from mylog import log
from django.utils import simplejson
from functions import trim_csv,verifyData
import confsql
import time
import re
confsql=confsql.Confsql()

def import_dhrulesYuzhi(request):
    '订货阈值翻倍情况导入'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=10)
        rs2,rs1=verifyData(rs1,length=10,required=[5,6,7,8])

        '重复项覆盖'
        temp=[]
        for rs in rs1:
            excode=rs[4]
            if rs[4]==u'商品代码':
                excode='sp'
            if rs[4]==u'品牌小类代码':
                excode='braxl'
            if rs[4]==u'大类代码':
                excode='prodl'
            if rs[4]==u'中类代码':
                excode='prozl'
            if rs[4]==u'小类代码':
                excode='proxl'
            sqlstr=u"select * from dhrulesYuzhi where mdcode='"+rs[0]+"' and xcode = '"+ rs[2] +"' and excode='"+excode+"' and startdate='"+rs[7]+"' and enddate = '" + rs[8] + "'"
            if confsql.checkExist(sqlstr)==1: #检查mdcode,excode,yqkey数据库是否已存在
                rs.append(u'数据库已存在!')
                temp.append(rs)
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

        '代码说明 检查'
        temp=[]
        for rs in rs1:
            if rs[4] <>u"商品代码" and rs[4]<>u"品牌小类代码" and rs[4]<>u"大类代码" and rs[4]<>u"中类代码" and rs[4]<>u"小类代码":
                rs.append(u'代码说明不符要求！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '代码 检查'
        temp=[]
        for rs in rs1:
            if rs[4]==u"商品代码" or rs[4]==u"品牌小类代码" or rs[4]==u"小类代码":
                if len(rs[2])<>8: #商品代码或品牌小类代码 8位
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
            if rs[4]==u"中类代码":
                if len(rs[2])<>5:
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
            if rs[4]==u"大类代码":
                if len(rs[2])<>2:
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)
        """
        '规则说明只能填相对值（即放大倍数）'
        temp=[]
        for rs in rs1:
            if rs[6]<>'相对值':
                rs.append(u'规则说明只能填“相对值”！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)
        """

        '规则值为百分比格式且大于0'
        temp=[]
        for rs in rs1:
            if type(eval(rs[6]))<>type(1.00) or eval(rs[6])<0:
                rs.append(u'规则值必须为正百分比格式！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '开始日期格式检查'
        temp=[]
        for rs in rs1:
            m=re.match(r'^\w\w\w\w-\w\w-\w\w$',rs[7])
            if m==None: #日期格式 yyyy-mm-dd
                rs.append(u'日期格式必须为yyyy-mm-dd！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '结束日期格式检查'
        temp=[]
        for rs in rs1:
            m=re.match(r'^\w\w\w\w-\w\w-\w\w$',rs[8])
            if m==None: #日期格式 yyyy-mm-dd
                rs.append(u'日期格式必须为yyyy-mm-dd！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='1200'><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>名称</th><th>代码说明</th><th>规则对象</th><th>倍数</th><th>开始日期</th><th>结束日期</th><th>备注</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td>" + rs[5] + "</td>"
                html+="<td>" + rs[6] + "</td>"
                html+="<td>" + rs[7] + "</td>"
                html+="<td>" + rs[8] + "</td>"
                html+="<td>" + rs[9] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[10] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td>" + rs[5] + "</td>"
                html+="<td>" + rs[6] + "</td>"
                html+="<td>" + rs[7] + "</td>"
                html+="<td>" + rs[8] + "</td>"
                html+="<td>" + rs[9] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/import_dhrulesYuzhi.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_dhrulesYuzhi(request):
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])

    for rs in rs1:
        excode=rs[4]
        if rs[4]==u'商品代码':
            excode='sp'
        if rs[4]==u'品牌小类代码':
            excode='braxl'
        if rs[4]==u'大类代码':
            excode='prodl'
        if rs[4]==u'中类代码':
            excode='prozl'
        if rs[4]==u'小类代码':
            excode='proxl'
        adddate = time.strftime("%Y-%m-%d", time.localtime())

        if rs[10]<>'':
            if rs[10]==u'数据库已存在!':
                    sqlstr=u"delete from dhrulesYuzhi where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and startdate='"+rs[7]+"' and enddate = '" + rs[8] + "';"
                    sqlstr+="insert into dhrulesYuzhi (mdcode,xcode,excode,yqkey,yqrule,yqvalue,startdate,enddate,remark,adddate) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+rs[5]+"','"+u"相对值"+"','"+rs[6]+"','"+rs[7]+"','"+rs[8]+"','"+rs[9]+"','"+adddate+"');"
                    confsql.runSql(sqlstr)
                    rs[10]=u'插入成功!'
            res={}
            res['mdcode']=rs[0]
            res['mdname']=rs[1]
            res['xcode']=rs[2]
            res['name']=rs[3]
            res['excode']=rs[4]
            res['yqkey']=rs[5]
            res['yqvalue']=rs[6]
            res['startdate']=rs[7]
            res['enddate']=rs[8]
            res['remark']=rs[9]
            res['info']=rs[10]
            result.append(res)
        else: #无误的
            try:
                sqlstr=u"insert into dhrulesYuzhi (mdcode,xcode,excode,yqkey,yqrule,yqvalue,startdate,enddate,remark,adddate) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+rs[5]+"','"+u"相对值"+"','"+rs[6]+"','"+rs[7]+"','"+rs[8]+"','"+rs[9]+"','"+adddate+"')"
                confsql.runSql(sqlstr)
                rs[10]=u'插入成功!'
            except:
                rs[10]=u'插入失败!'
            res={}
            res['mdcode']=rs[0]
            res['mdname']=rs[1]
            res['xcode']=rs[2]
            res['name']=rs[3]
            res['excode']=rs[4]
            res['yqkey']=rs[5]
            res['yqvalue']=rs[6]
            res['startdate']=rs[7]
            res['enddate']=rs[8]
            res['remark']=rs[9]
            res['info']=rs[10]
            result.append(res)
    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_dhrulesYuzhi(request):
    '查询暂停补货范围规则'
    t=get_template('mana1/insult_dhrulesYuzhi.html')
    sqlstr=u""" select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proname as xname,'商品代码' as excode,t1.yqkey,t1.yqrule,t1.yqvalue,t1.startdate, t1.enddate,t1.remark,t1.adddate from dhrulesYuzhi as t1 left outer join branch as t3 on (t1.mdcode=t3.braid), product_all t2 where t1.xcode=t2.proid and t1.excode='sp'
    union all
    select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.braxl as xname,'品牌小类代码' as excode,t1.yqkey,t1.yqrule,t1.yqvalue,t1.startdate, t1.enddate,t1.remark,t1.adddate from dhrulesYuzhi as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) ,(select braxl_id, braxl from product_all group by braxl_id, braxl) t2 where t1.xcode=t2.braxl_id and t1.excode='braxl'
    union all
    select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proxl as xname,'小类代码' as excode,t1.yqkey,t1.yqrule,t1.yqvalue,t1.startdate, t1.enddate,t1.remark,t1.adddate from dhrulesYuzhi as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) ,(select proxl_id, proxl from product_all group by proxl_id, proxl) t2 where t1.xcode=t2.proxl_id and t1.excode='proxl'
    union all
    select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prozl as xname,'中类代码' as excode,t1.yqkey,t1.yqrule,t1.yqvalue,t1.startdate, t1.enddate,t1.remark,t1.adddate from dhrulesYuzhi as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) ,(select prozl_id, prozl from product_all group by prozl_id, prozl) t2 where t1.xcode=t2.prozl_id and t1.excode='prozl'
    union all
    select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prodl as xname,'大类代码' as excode,t1.yqkey,t1.yqrule,t1.yqvalue,t1.startdate, t1.enddate,t1.remark,t1.adddate from dhrulesYuzhi as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) ,(select prodl_id, prodl from product_all group by prodl_id, prodl) t2 where t1.xcode=t2.prodl_id and t1.excode='prodl'
    """
    result=confsql.runquery(sqlstr)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

def delete_dhrulesYuzhi(request):
    '删除暂停订货范围规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=12)
        rs2,rs1=verifyData(rs1,length=12,required=[5,6,7,8,9])

        '是否重复'
        temp=[]
        for rs in rs1:
            excode=rs[4]
            if rs[4]==u'商品代码':
                excode='sp'
            if rs[4]==u'品牌小类代码':
                excode='braxl'
            if rs[4]==u'大类代码':
                excode='prodl'
            if rs[4]==u'中类代码':
                excode='prozl'
            if rs[4]==u'小类代码':
                excode='proxl'
            sqlstr=u"select * from dhrulesYuzhi where mdcode='"+rs[0]+"' and xcode = '"+ rs[2] +"' and excode='"+excode+"' and startdate='"+rs[8]+"' and enddate = '" + rs[9] + "'"
            if confsql.checkExist(sqlstr)<>1: #检查mdcode,excode,yqkey数据库是否已存在
                rs.append(u'数据库不存在!')
                temp.append(rs)
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

        '代码说明 检查'
        temp=[]
        for rs in rs1:
            if rs[4] <>u"商品代码" and rs[4]<>u"品牌小类代码" and rs[4]<>u"大类代码" and rs[4]<>u"中类代码" and rs[4]<>u"小类代码":
                rs.append(u'代码说明不符要求！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '代码 检查'
        temp=[]
        for rs in rs1:
            if rs[4]==u"商品代码" or rs[4]==u"品牌小类代码" or rs[4]==u"小类代码":
                if len(rs[2])<>8: #商品代码或品牌小类代码 8位
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
            if rs[4]==u"中类代码":
                if len(rs[2])<>5:
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
            if rs[4]==u"大类代码":
                if len(rs[2])<>2:
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '规则说明只能填相对值'
        temp=[]
        for rs in rs1:
            if rs[6]<>u'相对值':
                rs.append(u'规则说明只能填“相对值”！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '规则值为百分比格式且大于0'
        temp=[]
        for rs in rs1:
            if type(eval(rs[7]))<>type(1.00) or eval(rs[7])<0:
                rs.append(u'规则值必须为正百分比格式！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '开始日期格式检查'
        temp=[]
        for rs in rs1:
            m=re.match(r'^\w\w\w\w-\w\w-\w\w$',rs[8])
            if m==None: #日期格式 yyyy-mm-dd
                rs.append(u'日期格式必须为yyyy-mm-dd！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '结束日期格式检查'
        temp=[]
        for rs in rs1:
            m=re.match(r'^\w\w\w\w-\w\w-\w\w$',rs[9])
            if m==None: #日期格式 yyyy-mm-dd
                rs.append(u'日期格式必须为yyyy-mm-dd！')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)


        html=u"<table width='1200'><thead><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>代码名称</th><th>代码说明</th><th>规则对象</th><th>规则说明</th><th>规则值</th><th>开始日期</th><th>结束日期</th><th>备注</th><th>添加日期</th></tr></thead><tbody>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td>" + rs[5] + "</td>"
                html+="<td>" + rs[6] + "</td>"
                html+="<td>" + rs[7] + "</td>"
                html+="<td>" + rs[8] + "</td>"
                html+="<td>" + rs[9] + "</td>"
                html+="<td>" + rs[10] + "</td>"
                html+="<td>" + rs[11] + "</td>"
                html+="<td style='background-color:yellow'>" + rs[12] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td>" + rs[4] + "</td>"
                html+="<td>" + rs[5] + "</td>"
                html+="<td>" + rs[6] + "</td>"
                html+="<td>" + rs[7] + "</td>"
                html+="<td>" + rs[8] + "</td>"
                html+="<td>" + rs[9] + "</td>"
                html+="<td>" + rs[10] + "</td>"
                html+="<td>" + rs[11] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</tbody></table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/delete_dhrulesYuzhi.html')
        html=t.render(Context())
        return HttpResponse(html)

def deleteData_dhrulesYuzhi(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])
    if len(rs1)>0:
        for rs in rs1:
            if rs[12]<>'': #出错信息的保留
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['yqkey']=rs[5]
                res['yqrule']=rs[6]
                res['yqvalue']=rs[7]
                res['startdate']=rs[8]
                res['enddate']=rs[9]
                res['remark']=rs[10]
                res['adddate']=rs[11]
                res['info']=rs[12]
                result.append(res)
            else: #无出错信息的执行删除
                try:
                    excode=rs[4]
                    if rs[4]==u'商品代码':
                        excode='sp'
                    if rs[4]==u'品牌小类代码':
                        excode='braxl'
                    if rs[4]==u'大类代码':
                        excode='prodl'
                    if rs[4]==u'中类代码':
                        excode='prozl'
                    if rs[4]==u'小类代码':
                        excode='proxl'
                    confsql.runSql("delete from dhrulesYuzhi where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and startdate='"+rs[8]+"' and enddate = '" + rs[9] + "'")
                    res={}
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['yqkey']=rs[5]
                    res['yqrule']=rs[6]
                    res['yqvalue']=rs[7]
                    res['startdate']=rs[8]
                    res['enddate']=rs[9]
                    res['remark']=rs[10]
                    res['adddate']=rs[11]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['yqkey']=rs[5]
                    res['yqrule']=rs[6]
                    res['yqvalue']=rs[7]
                    res['startdate']=rs[8]
                    res['enddate']=rs[9]
                    res['remark']=rs[10]
                    res['adddate']=rs[11]
                    res['info']=u'删除失败!'
                    result.append(res)
    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

