# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: maxmin.py
#         Desc: 上下限相关
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-24 14:21:51
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql,datetime,memcache
from django.utils import simplejson
from mylog import log
from functions import trim_csv,verifyData
import datetime
import time

confsql=confsql.Confsql()
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def import_maxmin(request):
    ''' 上下限导入界面 '''
    if request.method=='POST':
        '''暂存数据 初步检查'''
        try:
            value=request.POST['value']
            rs1=trim_csv(value,itemlenth=6) #去除行尾多余换行符 rs1存放初始值
            rs2,rs1=verifyData(rs1,length=6,required=[4],maxmin=1)

            html=u"<table width='1000'><tr><th>门店代码</th><th>门店名称</th><th>商品代码</th><th>商品名称</th><th>上限</th><th>下限</th><th></th></tr>"
            if len(rs2)>0:
                for rs in rs2:
                    html+="<tr>"
                    html+="<td>" + rs[0] + "</td>"
                    html+="<td>" + rs[1] + "</td>"
                    html+="<td>" + rs[2] + "</td>"
                    html+="<td>" + rs[3] + "</td>"
                    html+="<td>" + rs[4] + "</td>"
                    html+="<td>" + rs[5] + "</td>"
                    html+="<td style='background-color:yellow'>" + rs[6] + "</td>"
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
                    html+="<td></td>"
                    html+="</tr>"
            html+="</table>"
            return HttpResponse(html)
        except:
            return HttpResponse(0)
    else:
        t=get_template('mana1/import_maxmin.html')
        html=t.render(Context())
        return HttpResponse(html)

def insult_maxmin(request):
    ''' 上下限查询界面 '''
    if request.method=='POST':
        try:
            jlist=simplejson.loads(request.POST["jsonlist"])

            if jlist['proid']<>'' or jlist['proname']<>'' or jlist['braid']<>'' or jlist['braname']<>''  or jlist['banben']<>'' or jlist['prodl']<>'' or jlist['prozl']<>'' or jlist['proxl']<>'' or jlist['barcode']<>'': #不全为空,即按单个或多个条件查询
                sqlstr="select * from (select t1.braid,t2.braname,t3.barcode,t1.proid,t3.proname,t1.maxval,t1.minval,t1.banben,t1.startdate,t1.enddate,t1.adddate ,t3.prodl_id||'_'||t3.prodl as prodl, t3.prozl_id||'_'||t3.prozl as prozl, t3.proxl_id||'_'||t3.proxl as proxl from maxmin t1 left outer join branch t2 on t1.braid=t2.braid left outer join product_all t3 on t1.proid=t3.proid) t1 where "
                for j in jlist:
                    if jlist[j]<>'':
                        li=jlist[j].split(",")
                        if len(li)==1: #一个条件
                            sqlstr+=j+" like '%%"+jlist[j].strip()+"%%' and "
                        else: #逗号分隔的多条件
                            sqlstr+="("
                            for l in li:
                                sqlstr+=j+" like '%%"+l.strip() +"%%' or  "
                            sqlstr=sqlstr[0:-4]+") and "
                sqlstr=sqlstr[0:-4]
                sqlstr+=" limit 20000"
                lines=confsql.runquery(sqlstr)

                result=[] #存放初始表头
                for rs in lines:
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['barcode']=rs[2]
                    res['proid']=rs[3]
                    res['proname']=rs[4]
                    res['maxval']=rs[5]
                    res['minval']=rs[6]
                    res['banben']=rs[7]
                    res['startdate']=rs[8]
                    res['enddate']=rs[9]
                    res['adddate']=rs[10]
                    res['prodl'] = rs[11]
                    res['prozl'] = rs[12]
                    res['proxl'] = rs[13]
                    result.append(res)
                jsonres=simplejson.dumps(result)
                return  HttpResponse(jsonres)
            else: #全为空，查询所有
                sqlstr="select t1.braid,t2.braname,t3.barcode,t1.proid,t3.proname,t1.maxval,t1.minval,t1.banben,t1.startdate,t1.enddate,t1.adddate,t3.prodl_id||'_'||t3.prodl as prodl, t3.prozl_id||'_'||t3.prozl as prozl, t3.proxl_id||'_'||t3.proxl as proxl from maxmin t1 left outer join branch t2 on t1.braid=t2.braid left outer join product_all t3 on t1.proid=t3.proid limit 20000"
                lines=confsql.runquery(sqlstr)
                result=[] #存放初始表头
                for rs in lines:
                    res={}
                    res['braid']=rs[0]
                    res['braname']=rs[1]
                    res['barcode']=rs[2]
                    res['proid']=rs[3]
                    res['proname']=rs[4]
                    res['maxval']=rs[5]
                    res['minval']=rs[6]
                    res['banben']=rs[7]
                    res['startdate']=rs[8]
                    res['enddate']=rs[9]
                    res['adddate']=rs[10]
                    res['prodl'] = rs[11]
                    res['prozl'] = rs[12]
                    res['proxl'] = rs[13]
                    result.append(res)
                jsonres=simplejson.dumps(result)
                log(jsonres)
                return  HttpResponse(jsonres)
        except:
            return HttpResponse(0)
    else:
        t=get_template('mana1/insult_maxmin.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_maxmin(request):
    ' 上下限导入检查 写入数据库 '
    try:
        rs1=[]
        result=[]
        myjson=simplejson.loads(request.POST["myjson"])
        rs1=trim_csv(myjson["table"])
        banben=myjson["banben"]
        startdate=myjson["startdate"]
        enddate=myjson["enddate"]
        #插入数据库
        sqlstr=""
        for rs in rs1:
            if rs[6]=='':
                sqlstr+="delete from maxmin where braid ='" + rs[0] + "' and proid='" + rs[2] + "' and banben='" + banben + "';"
        if sqlstr<>"":
            confsql.runSql(sqlstr)  #数据库
        sqlstr=""
        for rs in rs1:
            if rs[6]=='':
                adddate=datetime.datetime.now().strftime('%Y-%m-%d') #最后追加插入日期
                sqlstr+="insert into maxmin(braid,proid,maxval,minval,banben,startdate,enddate,adddate) values('"+rs[0]+"','"+rs[2]+"','"+rs[4]+"','"+rs[5]+"','"+banben+"','"+startdate+"','"+enddate+"','"+adddate+"');"
                rs[6]='插入成功!'
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['proid']=rs[2]
                res['proname']=rs[3]
                res['maxval']=rs[4]
                res['minval']=rs[5]
                res['info']=rs[6]
                result.append(res)
            else:
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['proid']=rs[2]
                res['proname']=rs[3]
                res['maxval']=rs[4]
                res['minval']=rs[5]
                res['info']=rs[6]
                result.append(res)
        if sqlstr<>"":
            confsql.runSql(sqlstr)  #数据库
        jsonres=simplejson.dumps(result)
        log(jsonres)
        return  HttpResponse(jsonres)
    except:
        return HttpResponse(0)

def backup_maxmin(request):
    '备份上下限'
    if request.method=='POST':
        try:
            jlist=simplejson.loads(request.POST["jsonlist"])
            if jlist['proid']<>'' or jlist['proname']<>'' or jlist['braid']<>'' or jlist['braname']<>'' or jlist['prodl']<>'' or jlist['prozl']<>'' or jlist['proxl']<>'': #不全为空
                sqlstr="""
                    insert into maxmin_bak
                    select braid,proid,maxval,minval,banben,startdate,enddate,adddate,'""" + datetime.date.today().strftime('%Y-%m-%d') + """' from(
                        select * from (
                            select t1.braid,t2.braname,t1.proid,t3.proname,t3.prodl_id||'_'||t3.prodl as prodl,t3.prozl_id||'_'||t3.prozl as prozl,t3.proxl_id||'_'||t3.proxl as proxl,t1.maxval,t1.minval,t1.banben,t1.startdate,t1.enddate,t1.adddate
                            from maxmin t1,branch t2,product_all t3
                            where t1.braid=t2.braid and t1.proid=t3.proid
                        ) t1 where
                """
                for j in jlist:
                    if jlist[j]<>'':
                        li=jlist[j].split(",")
                        if len(li)==1: #一个条件
                            sqlstr+=j+" like '%%"+jlist[j].strip()+"%%' and "
                        else: #逗号分隔的多条件
                            sqlstr+="("
                            for l in li:
                                sqlstr+=j+" like '%%"+l.strip() +"%%' or  "
                            sqlstr=sqlstr[0:-4]+") and "
                sqlstr=sqlstr[0:-4]
                sqlstr+=") tt1"
                confsql.runSql(sqlstr)

                sqlstr="""
                        select count(*) from (
                            select t1.braid,t2.braname,t1.proid,t3.proname,t3.prodl_id||'_'||t3.prodl as prodl,t3.prozl_id||'_'||t3.prozl as prozl,t3.proxl_id||'_'||t3.proxl as proxl,t1.maxval,t1.minval,t1.banben,t1.startdate,t1.enddate,t1.adddate
                            from maxmin t1,branch t2,product_all t3
                            where t1.braid=t2.braid and t1.proid=t3.proid
                        ) t1 where
                """
                for j in jlist:
                    if jlist[j]<>'':
                        li=jlist[j].split(",")
                        if len(li)==1: #一个条件
                            sqlstr+=j+" like '%%"+jlist[j].strip()+"%%' and "
                        else: #逗号分隔的多条件
                            sqlstr+="("
                            for l in li:
                                sqlstr+=j+" like '%%"+l.strip() +"%%' or  "
                            sqlstr=sqlstr[0:-4]+") and "
                sqlstr=sqlstr[0:-4]
                result=confsql.runquery(sqlstr)
                for rs in result:
                    num=rs[0]
                return  HttpResponse(num)
            else: #全为空，查询所有
                sqlstr="""
                    insert into maxmin_bak
                    select braid,proid,maxval,minval,banben,startdate,enddate,adddate,'""" + datetime.date.today().strftime('%Y-%m-%d') + """'
                    from maxmin
                """
                confsql.runSql(sqlstr)
                sqlstr="select count(*) from maxmin"
                result=confsql.runquery(sqlstr)
                for rs in result:
                    num=rs[0]
                return HttpResponse(num)
        except:
            return HttpResponse(0)
    else:
        t=get_template('mana1/backup_maxmin.html')
        html=t.render(Context())
        return HttpResponse(html)

if __name__=='__main__':
    str="中文"
