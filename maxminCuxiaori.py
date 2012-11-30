# -*- coding: utf-8 -*-
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

def import_maxminCuxiaori(request):
    '暂停补货范围规则导入'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=10)
        rs2,rs1=verifyData(rs1,length=10,required=[0,2,4,5,6,7,8])

        '重复项覆盖'
        temp=[]
        for rs in rs1:
            excode=rs[4]
            if rs[4]==u'商品代码':
                excode='sp'
            if rs[4]==u'品牌小类代码':
                excode='braxl'
            if rs[4]==u'商品大类':
                excode='prodl'
            if rs[4]==u'商品中类':
                excode='prozl'
            if rs[4]==u'商品小类':
                excode='proxl'
            sqlstr=u"select * from maxminCuxiaori where mdcode='"+rs[0]+"' and xcode = '"+ rs[2] +"' and excode='"+excode+"' and startdate='"+rs[7]+"' and enddate = '" + rs[8] + "'"
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
                rs.append(u'门店代码长度必须为5位')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '代码说明 检查'
        temp=[]
        for rs in rs1:
            if rs[4] <>u"商品代码" and rs[4]<>u"品牌小类代码" and rs[4]<>u"商品大类" and rs[4]<>u"商品中类" and rs[4]<>u"商品小类":
                rs.append(u'代码说明不符要求')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '代码 检查'
        temp=[]
        for rs in rs1:
            if len(rs[2])<>8: #商品代码或品牌小类代码 8位
                rs.append(u'商品代码或品牌小类代码长度必须为8位')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '上下限倍数必须是数值'
        temp=[]
        for rs in rs1:
            if type(eval(rs[5]))<>type(1.00) and type(eval(rs[5]))<>type(1):
                rs.append(u'上限倍数必须是数值')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        temp=[]
        for rs in rs1:
            if type(eval(rs[6]))<>type(1.00) and type(eval(rs[6]))<>type(1):
                rs.append(u'下限倍数必须是数值')
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
                rs.append(u'日期格式必须为yyyy-mm-dd')
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
                rs.append(u'日期格式必须为yyyy-mm-dd')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='1200'><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>代码名称</th><th>代码说明</th><th>上限倍数</th><th>下限倍数</th><th>规则开始时间</th><th>规则结束时间</th><th>备注</th></tr>"
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
        t=get_template('mana1/import_maxminCuxiaori.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_maxminCuxiaori(request):
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
        if rs[4]==u'商品大类':
            excode='prodl'
        if rs[4]==u'商品中类':
            excode='prozl'
        if rs[4]==u'商品小类':
            excode='proxl'

        adddate = time.strftime("%Y-%m-%d", time.localtime())

        if rs[10]<>'':
            if rs[10]==u'数据库已存在!':
                try:
                    confsql.runSql("delete from maxminCuxiaori where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and startdate='"+rs[5]+"' and enddate = '" + rs[6] + "'")

                    confsql.runSql("insert into maxminCuxiaori (mdcode,xcode,excode,max_multiple,min_multiple,startdate,enddate,remark,adddate) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+rs[5]+"','"+rs[6]+"','"+rs[7]+"','"+rs[8]+"','"+rs[9]+"','"+adddate+"')")
                    rs[10]='插入成功!'
                except:
                    rs[10]='插入失败!'
            res={}
            res['mdcode']=rs[0]
            res['mdname']=rs[1]
            res['xcode']=rs[2]
            res['name']=rs[3]
            res['excode']=rs[4]
            res['max_multiple']=rs[5]
            res['min_multiple']=rs[6]
            res['startdate']=rs[7]
            res['enddate']=rs[8]
            res['remark']=rs[9]
            res['info']=rs[10]
            result.append(res)
        else: #无误的
            try:
                confsql.runSql("insert into maxminCuxiaori (mdcode,xcode,excode,max_multiple,min_multiple,startdate,enddate,remark,adddate) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+rs[5]+"','"+rs[6]+"','"+rs[7]+"','"+rs[8]+"','"+rs[9]+"','"+adddate+"')")
                rs[10]='插入成功!'
            except:
                rs[10]='插入失败!'
            res={}
            res['mdcode']=rs[0]
            res['mdname']=rs[1]
            res['xcode']=rs[2]
            res['name']=rs[3]
            res['excode']=rs[4]
            res['max_multiple']=rs[5]
            res['min_multiple']=rs[6]
            res['startdate']=rs[7]
            res['enddate']=rs[8]
            res['remark']=rs[9]
            res['info']=rs[10]
            result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_maxminCuxiaori(request):
    '查询每月促销日小下限翻倍'
    t=get_template('mana1/insult_maxminCuxiaori.html')
    sqlstr=""" select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proname as xname,'商品代码' as excode,max_multiple,min_multiple,t1.startdate, t1.enddate,remark 
        from (select * from maxminCuxiaori where excode='sp') as t1 left outer join branch as t3 
        on (t1.mdcode=t3.braid) left outer join product_all t2 
        on t1.xcode=t2.proid 
    union all
        select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.braxl as xname,'品牌小类代码' as excode,max_multiple,min_multiple,t1.startdate, t1.enddate,remark 
        from (select * from maxminCuxiaori where excode='braxl') as t1 left outer join branch as t3 
        on (t1.mdcode=t3.braid) left outer join (select braxl_id, braxl from product_all group by braxl_id, braxl) t2 
        on t1.xcode=t2.braxl_id and t1.excode='braxl'
    union all
        select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proxl as xname,'小类代码' as excode,max_multiple,min_multiple,t1.startdate, t1.enddate,remark 
        from (select * from maxminCuxiaori where excode='proxl') as t1 left outer join branch as t3 
        on (t1.mdcode=t3.braid) left outer join (select proxl_id, proxl from product_all group by proxl_id, proxl) t2 
        on t1.xcode=t2.proxl_id and t1.excode='proxl'
    union all
        select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prozl as xname,'中类代码' as excode,max_multiple,min_multiple,t1.startdate, t1.enddate,remark 
        from (select * from maxminCuxiaori where excode='prozl') as t1 left outer join branch as t3 
        on (t1.mdcode=t3.braid) left outer join (select prozl_id, prozl from product_all group by prozl_id, prozl) t2 
        on t1.xcode=t2.prozl_id and t1.excode='prozl'
    union all
        select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prodl as xname,'大类代码' as excode,max_multiple,min_multiple,t1.startdate, t1.enddate,remark 
        from (select * from maxminCuxiaori where excode='prodl') as t1 left outer join branch as t3 
        on (t1.mdcode=t3.braid) left outer join (select prodl_id, prodl from product_all group by prodl_id, prodl) t2 
        on t1.xcode=t2.prodl_id and t1.excode='prodl'
    """
    result=confsql.runquery(sqlstr)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

def delete_maxminCuxiaori(request):
    '删除暂停订货范围规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=10)
        rs2,rs1=verifyData(rs1,length=10,required=[0,2,4,5,6,7,8])

        '重复项覆盖'
        temp=[]
        for rs in rs1:
            excode=rs[4]
            if rs[4]==u'商品代码':
                excode='sp'
            if rs[4]==u'品牌小类代码':
                excode='braxl'
            if rs[4]==u'商品大类':
                excode='prodl'
            if rs[4]==u'商品中类':
                excode='prozl'
            if rs[4]==u'商品小类':
                excode='proxl'
            sqlstr=u"select * from maxminCuxiaori where mdcode='"+rs[0]+"' and xcode = '"+ rs[2] +"' and excode='"+excode+"' and startdate='"+rs[7]+"' and enddate = '" + rs[8] + "'"
            if confsql.checkExist(sqlstr)<>1: #检查mdcode,excode,yqkey数据库是否已存在
                rs.append(u'数据库中不存在!')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '门店代码商品代码 长度检查'
        temp=[]
        for rs in rs1:
            if len(rs[0])<>5: #门店代码 5位
                rs.append(u'门店代码长度必须为5位')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '代码说明 检查'
        temp=[]
        for rs in rs1:
            if rs[4] <>u"商品代码" and rs[4]<>u"品牌小类代码" and rs[4]<>u"商品大类" and rs[4]<>u"商品中类" and rs[4]<>u"商品小类":
                rs.append(u'代码说明不符要求')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '代码 检查'
        temp=[]
        for rs in rs1:
            if len(rs[2])<>8: #商品代码或品牌小类代码 8位
                rs.append(u'商品代码或品牌小类代码长度必须为8位')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        '上下限倍数必须是数值'
        temp=[]
        for rs in rs1:
            if type(eval(rs[5]))<>type(1.00) and type(eval(rs[5]))<>type(1):
                rs.append(u'上限倍数必须是数值')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        temp=[]
        for rs in rs1:
            if type(eval(rs[6]))<>type(1.00) and type(eval(rs[6]))<>type(1):
                rs.append(u'下限倍数必须是数值')
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
                rs.append(u'日期格式必须为yyyy-mm-dd')
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
                rs.append(u'日期格式必须为yyyy-mm-dd')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='1200'><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>代码名称</th><th>代码说明</th><th>上限倍数</th><th>下限倍数</th><th>规则开始时间</th><th>规则结束时间</th><th>备注</th></tr>"
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
        t=get_template('mana1/delete_maxminCuxiaori.html')
        html=t.render(Context())
        return HttpResponse(html)

def deleteData_maxminCuxiaori(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])
    if len(rs1)>0:
        for rs in rs1:
            if rs[10]<>'': #出错信息的保留
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['max_multiple']=rs[5]
                res['min_multiple']=rs[6]
                res['startdate']=rs[7]
                res['enddate']=rs[8]
                res['remark']=rs[9]
                res['info']=rs[10]
                result.append(res)
            else:
                try:
                    #sp, xl, zl, dl, null
                    excode=rs[4]
                    if rs[4]==u'商品代码':
                        excode='sp'
                    if rs[4]==u'品牌小类代码':
                        excode='braxl'
                    if rs[4]==u'商品大类':
                        excode='prodl'
                    if rs[4]==u'商品中类':
                        excode='prozl'
                    if rs[4]==u'商品小类':
                        excode='proxl'
                    confsql.runSql("delete from maxminCuxiaori where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and startdate='"+rs[7]+"' and enddate = '" + rs[8] + "'")
                    res={}
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['max_multiple']=rs[5]
                    res['min_multiple']=rs[6]
                    res['startdate']=rs[7]
                    res['enddate']=rs[8]
                    res['remark']=rs[9]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['max_multiple']=rs[5]
                    res['min_multiple']=rs[6]
                    res['startdate']=rs[7]
                    res['enddate']=rs[8]
                    res['remark']=rs[9]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

