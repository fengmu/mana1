# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql
from mylog import log
from django.utils import simplejson
from functions import trim_csv,verifyData
confsql=confsql.Confsql()

def import_dhrules(request):
    '订货量修改规则导入'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=8)
        rs2,rs1=verifyData(rs1,length=8,required=[5,6,7],dhrules=1)

        html=u"<table width='1000'><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>名称</th><th>代码说明</th><th>规则对象</th><th>规则说明</th><th>规则值</th></tr>"
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
                html+="<td style='background-color:yellow'>" + rs[8] + "</td>"
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
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/import_dhrules.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_dhrules(request):
    '保存订货量修改规则'
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
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
            
        yqkey = rs[5]
        if rs[5]==u'上阈值':
            yqkey='maxlimit'
        if rs[5]==u'下阈值':
            yqkey='minlimit'
            
        yqrule = rs[6]
        if rs[6]==u'绝对值':
            yqrule='jd'
        if rs[6]==u'相对值':
            yqrule='xd'
            
        

        if rs[8]<>'':
            if rs[8]==u'数据库已存在!':
                try:
                    #confsql.runSql("update dhrules set yqrule='"+yqrule+"',yqvalue='"+rs[7]+"' where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and yqkey='"+yqkey+"'")
                    confsql.runSql("delete from dhrules where mdcode='"+rs[0]+"' and xcode='" +rs[2]+ "' and excode='"+excode+"' and yqkey='"+yqkey+"'")
                    confsql.runSql("insert into dhrules (mdcode,xcode,excode,yqkey,yqrule,yqvalue) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+yqkey+"','"+yqrule+"','"+rs[7]+"')")
                    rs[8]='插入成功!'
                except:
                    rs[8]='插入失败!'
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['yqkey']=rs[5]
                res['yqrule']=rs[6]
                res['yqvalue']=rs[7]
                res['info']=rs[8]
                result.append(res)
            else:
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['yqkey']=rs[5]
                res['yqrule']=rs[6]
                res['yqvalue']=rs[7]
                res['info']=rs[8]
                result.append(res)
        else: #无误的
            try:
                confsql.runSql("insert into dhrules (mdcode,xcode,excode,yqkey,yqrule,yqvalue) values('"+rs[0]+"','"+rs[2]+"','"+excode+"','"+yqkey+"','"+yqrule+"','"+rs[7]+"')")
                rs[8]='插入成功!'
            except:
                rs[8]='插入失败!'
            res={}
            res['mdcode']=rs[0]
            res['mdname']=rs[1]
            res['xcode']=rs[2]
            res['name']=rs[3]
            res['excode']=rs[4]
            res['yqkey']=rs[5]
            res['yqrule']=rs[6]
            res['yqvalue']=rs[7]
            res['info']=rs[8]
            result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_dhrules(request):
    '查询订货量修改规则'
    t=get_template('mana1/insult_dhrules.html')
    sqlstr=" select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proname as xname,'商品代码',case when t1.yqkey = 'maxlimit' then '上阈值' when t1.yqkey = 'minlimit' then '下阈值' end , case when t1.yqrule='jd' then '绝对值' when t1.yqrule='xd' then '相对值' end ,t1.yqvalue from dhrules as t1 left outer join branch as t3 on (t1.mdcode=t3.braid), product_all t2 where t1.xcode=t2.proid and t1.excode='sp'  union all "
    sqlstr+=" select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.proxl as xname,'小类代码',case when t1.yqkey = 'maxlimit' then '上阈值' when t1.yqkey = 'minlimit' then '下阈值' end , case when t1.yqrule='jd' then '绝对值' when t1.yqrule='xd' then '相对值' end ,t1.yqvalue from dhrules as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) ,(select proxl_id, proxl from product_all group by proxl_id, proxl) t2 where t1.xcode=t2.proxl_id and t1.excode='xl'  union all "
    sqlstr+=" select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prozl as xname,'中类代码',case when t1.yqkey = 'maxlimit' then '上阈值' when t1.yqkey = 'minlimit' then '下阈值' end , case when t1.yqrule='jd' then '绝对值' when t1.yqrule='xd' then '相对值' end ,t1.yqvalue from dhrules as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) ,(select prozl_id, prozl from product_all group by prozl_id, prozl) t2 where t1.xcode=t2.prozl_id and t1.excode='zl' union all "
    sqlstr+=" select t1.mdcode,case when t3.braname is null then '' else t3.braname end,t1.xcode,t2.prodl as xname,'大类代码',case when t1.yqkey = 'maxlimit' then '上阈值' when t1.yqkey = 'minlimit' then '下阈值' end , case when t1.yqrule='jd' then '绝对值' when t1.yqrule='xd' then '相对值' end ,t1.yqvalue from dhrules as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) ,(select prodl_id, prodl from product_all group by prodl_id, prodl) t2 where t1.xcode=t2.prodl_id and t1.excode='dl'  union all"
    sqlstr+=" select t1.mdcode, case when t3.braname is null then '' else t3.braname end, t1.xcode, '' as xname, '' as excode , case when t1.yqkey = 'maxlimit' then '上阈值' when t1.yqkey = 'minlimit' then '下阈值' end , case when t1.yqrule='jd' then '绝对值' when t1.yqrule='xd' then '相对值' end , t1.yqvalue from dhrules as t1 left outer join branch as t3 on (t1.mdcode=t3.braid) where t1.xcode =''"
    result=confsql.runquery(sqlstr)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)



def delete_dhrules(request):
    '删除订货规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=8)
        rs2,rs1=verifyData(rs1,length=8,required=[5,6,7],dhrules=1)

        html=u"<table width='1000'><tr><th>门店代码</th><th>门店名称</th><th>代码</th><th>名称</th><th>代码说明</th><th>规则对象</th><th>规则说明</th><th>规则值</th></tr>"
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
                html+="<td style='background-color:yellow'>" + rs[8] + "</td>"
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
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(Context(html))
    else:
        t=get_template('mana1/delete_dhrules.html')
        html=t.render(Context())
        return HttpResponse(html)


def deleteData_dhrules(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],itemlenth=0)
    if len(rs1)>0:
        for rs in rs1:
            if rs[8]<>'': #出错信息的保留
                res={}
                res['mdcode']=rs[0]
                res['mdname']=rs[1]
                res['xcode']=rs[2]
                res['name']=rs[3]
                res['excode']=rs[4]
                res['yqkey']=rs[5]
                res['yqrule']=rs[6]
                res['yqvalue']=rs[7]
                res['info']=rs[8]
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
                        
                    yqkey = rs[5]
                    if rs[5]==u'上阈值':
                        yqkey='maxlimit'
                    if rs[5]==u'下阈值':
                        yqkey='minlimit'
                        
                        
                        
                    sqlstr=u"delete from dhrules where mdcode='"+rs[0]+"' and xcode ='"+rs[2] +"' and excode='"+excode+"' and yqkey='"+yqkey+"'"
                    #log(sqlstr)
                    confsql.runSql(sqlstr)
                    res={}
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['yqkey']=rs[5]
                    res['yqrule']=rs[6]
                    res['yqvalue']=rs[7]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res={}
                    res['mdcode']=rs[0]
                    res['mdname']=rs[1]
                    res['xcode']=rs[2]
                    res['name']=rs[3]
                    res['excode']=rs[4]
                    res['yqkey']=rs[5]
                    res['yqrule']=rs[6]
                    res['yqvalue']=rs[7]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

