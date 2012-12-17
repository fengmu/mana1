# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql
from mylog import log
from django.utils import simplejson
from functions import trim_csv,verifyData

import time
confsql=confsql.Confsql()

def import_dhPauserules(request):
    '暂停补货范围规则导入'
    if request.method=='POST':
        value=request.POST['value']        
        rs1=trim_csv(value,itemlenth=7)
        rs2,rs1=verifyData(rs1,length=7,required=[5, 6],dhpauserules=1)
        
        '重复项覆盖'
        temp=[]
        for rs in rs1:
            excode=rs[4]
            if rs[4]==u'商品代码':
                excode='sp'
            if rs[4]==u'小类代码':
                excode='xl'
            if rs[4]==u'中类代码':
                excode='zl'
            if rs[4]==u'大类代码':
                excode='dl'

            sqlstr=u"select * from dhpauserules where mdcode='"+rs[0]+"' and xcode = '"+ rs[2] +"' and excode='"+excode+"' and startdate='"+rs[5]+"' and enddate = '" + rs[6] + "'"
            if confsql.checkExist(sqlstr)==1: #检查mdcode,excode,yqkey数据库是否已存在
                rs.append(u'数据库已存在!')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='1000'><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>代码名称</th><th>代码说明</th><th>规则开始时间</th><th>规则结束时间</th></tr>"
            
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
                html+="<td style='background-color:yellow'>" + rs[7] + "</td>"
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
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))

    else:
        t=get_template('mana1/import_dhPauserules.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_dhPauserules(request):
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"].encode('utf8'))
    rs1=trim_csv(myjson["table"])
    
    for rs in rs1:
        excode=rs[4]
        if rs[4]==u'商品代码':
            excode='sp'
        if rs[4]==u'小类代码':
            excode='xl'
        if rs[4]==u'中类代码':
            excode='zl'
        if rs[4]==u'大类代码':
            excode='dl'
            
        adddate = time.strftime("%Y-%m-%d", time.localtime())

        if rs[7]<>'':
            if rs[7]==u'数据库已存在!':
                try:
                    
                    #confsql.runSql("update dhrules set yqrule='"+yqrule+"',yqvalue='"+rs[7]+"' where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and yqkey='"+yqkey+"'")
                    #log("delete from dhpauserules where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and startdate='"+rs[5]+"' and enddate = '" + rs[6] + "'")
                    confsql.runSql("delete from dhpauserules where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and startdate='"+rs[5]+"' and enddate = '" + rs[6] + "'")
                    
                    confsql.runSql("insert into dhpauserules (mdcode,xcode,excode,startdate, enddate, adddate) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+rs[5]+"','"+rs[6]+"','"+adddate+"')")
                    rs[7]='插入成功!'
                except:
                    rs[7]='插入失败!'
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['startdate']=rs[5]
                res['enddate']=rs[6]                
                res['info']=rs[7]
                result.append(res)
            else:
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['startdate']=rs[5]
                res['enddate']=rs[6]                
                res['info']=rs[7]
                result.append(res)
        else: #无误的
            try:
                confsql.runSql("insert into dhpauserules (mdcode,xcode,excode,startdate, enddate, adddate) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+rs[5]+"','"+rs[6]+"','"+adddate+"')")
                rs[7]='插入成功!'
            except:
                rs[7]='插入失败!'
            res={}
            res['mdcode']=rs[0]
            res['mdname']=rs[1]
            res['xcode']=rs[2]
            res['name']=rs[3]
            res['excode']=rs[4]
            res['startdate']=rs[5]
            res['enddate']=rs[6]                
            res['info']=rs[7]
            result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_dhPauserules(request):
    '查询暂停补货范围规则'
    result=[]
    sqlstr=u""" select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proname as xname,'商品代码' as excode,  t1.startdate, t1.enddate from (select * from dhpauserules where excode='sp') t1 left outer join branch as t3 on (t1.mdcode=t3.braid) left outer join  product_all t2 on t1.xcode=t2.proid  union all 
    select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proxl as xname,'小类代码' as excode,   t1.startdate, t1.enddate from( select * from dhpauserules where excode='xl') t1 left outer join branch as t3 on (t1.mdcode=t3.braid) left outer join (select proxl_id, proxl from product_all group by proxl_id, proxl) t2 on t1.xcode=t2.proxl_id union all 
    select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prozl as xname,'中类代码' as excode,   t1.startdate, t1.enddate from (select * from dhpauserules where excode='zl') t1 left outer join branch as t3 on (t1.mdcode=t3.braid) left outer join (select prozl_id, prozl from product_all group by prozl_id, prozl) t2 on t1.xcode=t2.prozl_id union all 
    select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prodl as xname,'大类代码' as excode,   t1.startdate, t1.enddate from (select * from dhpauserules where excode='dl') t1 left outer join branch as t3 on (t1.mdcode=t3.braid) left outer join (select prodl_id, prodl from product_all group by prodl_id, prodl) t2 on t1.xcode=t2.prodl_id union all
    select t1.mdcode, case when t3.braname is null then '' else t3.braname end, t1.xcode, '' as xname, '' as excode ,  t1.startdate, t1.enddate from (select * from dhpauserules where xcode ='') t1 left outer join branch as t3 on (t1.mdcode=t3.braid) """
    log(sqlstr)
    result=confsql.runquery(sqlstr)
    rec=[]
    for rs in result:
        res={}
        res['braid']=rs[0]
        res['braname']=rs[1]
        res['xcode']=rs[2]
        res['xname']=rs[3]
        res['excode']=rs[4]
        res['startdate']=rs[5]
        res['enddate']=rs[6]
        rec.append(res)
    t=get_template('mana1/insult_dhPauserules.html')
    html=t.render(Context({"rec":rec}))
    return HttpResponse(html)

def delete_dhPauserules(request):
    '删除暂停订货范围规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=7)
        rs2,rs1=verifyData(rs1,length=7,required=[5,6],dhpauserules=1)

        html=u"<table width='1000'><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>代码名称</th><th>代码说明</th><th>规则开始时间</th><th>规则结束时间</th></tr>"
            
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
                html+="<td style='background-color:yellow'>" + rs[7] + "</td>"
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
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/delete_dhpauserules.html')
        html=t.render(Context())
        return HttpResponse(html)
    
    
def deleteData_dhPauserules(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],itemlenth=0)
    if len(rs1)>0:
        for rs in rs1:
            if rs[7]<>'': #出错信息的保留
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['startdate']=rs[5]
                res['enddate']=rs[6]
               
                res['info']=rs[7]
                result.append(res)
            else:
                try:
                    #sp, xl, zl, dl, null
                    res={}
                    excode=rs[4]
                    if rs[4]==u'商品代码':
                        excode='sp'
                    if rs[4]==u'小类代码':
                        excode='xl'
                    if rs[4]==u'中类代码':
                        excode='zl'
                    if rs[4]==u'大类代码':
                        excode='dl'
                    confsql.runSql("delete from dhpauserules where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and startdate='"+rs[5]+"' and enddate = '" + rs[6] + "'")
                    res={}
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['startdate']=rs[5]
                    res['enddate']=rs[6]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['startdate']=rs[5]
                    res['enddate']=rs[6]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

