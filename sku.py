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
import psycopg2
import datetime
import os,sys,gzip
from ftplib import FTP

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
if __name__=='__main__':
    ftpinfo = {"ip":'211.147.235.194', "port":'15443', "user":'ftpcl', "pwd":'ftpcl'}
    conn=psycopg2.connect(host='localhost',port=5432,user='postgres',password='zcbdcyj123',database='yq3')
    cur=conn.cursor()
    lastmonth=str(datetime.datetime.today().year)+str(datetime.datetime.today().month-1)
    zipfile='stock_monthly_'+lastmonth+'.csv.zip'
    ftpdir='D:/getdata/ftp/'
    """
    #下载数据
    try:
        cmdstr='del /Q '+ftpdir+'stock_monthly*'
        os.system(cmdstr)
    except:
        print "0"
    ftp=FTP()
    ftp.connect(ftpinfo["ip"],ftpinfo["port"])
    ftp.login(ftpinfo["user"],ftpinfo["pwd"])
    ftp.retrbinary('RETR '+zipfile,open(ftpdir+zipfile,'wb').write)
    ftp.quit()
    """
    g = gzip.GzipFile(mode='rb', fileobj=open(r""+ftpdir+zipfile+"",'rb'))
    open(r""+ftpdir+zipfile[0:-4]+"",'wb').write(g.read())

    #导数据
    """
    create table stock_monthly
    (
    braid character varying(5) NOT NULL,
    proid character varying(13),
    classid  character varying(13) NOT NULL,
    brandid character varying(13) NOT NULL,
    initqty numeric (13,3) NULL,
    curqty numeric (13,3) NULL,
    msaleqty numeric (13,3) NULL,
    msaleamt numeric (13,3) NULL
    );
    """
    sqlstr="truncate table stock_monthly;"
    sqlstr+="copy stock_monthly from '"+ftpdir+zipfile[0:-4]+"' delimiter as E'\t' csv;"
    print sqlstr
    cur.execute(sqlstr)
    conn.commit()

    #数据加工
    sqlstr="""
    delete from stock_monthly where initqty is NULL and curqty is NULL ;
    delete from stock_monthly where initqty<=0 and curqty<=0 and msaleqty <=0 ;
    delete from stock_monthly where initqty is NULL and curqty <=0 and msaleqty<=0;
    delete from stock_monthly where initqty is NULL and curqty <=0 and msaleqty is NULL;

    --create table sku(门店代码 varchar(255),门店名称 varchar(255),店面面积 numeric(18,0),SKU总数 numeric(18,0),流通品牌 numeric(18,0),自有品牌 numeric(18,0),彩妆L numeric(18,0),彩妆Z numeric(18,0),护肤L numeric(18,0),护肤Z numeric(18,0),化妆工具L numeric(18,0),化妆工具Z numeric(18,0),美发护理L numeric(18,0),美发护理Z numeric(18,0),男士护理L numeric(18,0),男士护理Z numeric(18,0),日用品L numeric(18,0),日用品Z numeric(18,0),身体护理L numeric(18,0),身体护理Z numeric(18,0),婴童护理L numeric(18,0),婴童护理Z numeric(18,0),食品L numeric(18,0),食品Z numeric(18,0))

    update sku
    set SKU总数=0,流通品牌=0,自有品牌=0,彩妆L=0,彩妆Z=0,护肤L=0,护肤Z=0,化妆工具L=0,化妆工具Z=0,美发护理L=0,美发护理Z=0,男士护理L=0,男士护理Z=0,日用品L=0,日用品Z=0,身体护理L=0,身体护理Z=0,婴童护理L=0,婴童护理Z=0,食品L=0,食品Z=0;


    --更新流通品牌
    update sku
    set 流通品牌=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl<>'物料赠品' 	
        and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格'))
        and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;


    --更新SKU总数
    update sku
    set SKU总数=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl<>'物料赠品' 
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;


    --更新自有品牌
    update sku
    set 自有品牌=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl<>'物料赠品' 
        and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格')
        and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;



    --更新彩妆L
    update sku
    set 彩妆L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl<>'物料赠品'
    and t2.prodl='彩妆' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格'))
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;




    --更新彩妆Z 
    update sku
    set 彩妆Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl<>'物料赠品'
    and t2.prodl='彩妆' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格')
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;


    --更新护肤L
    update sku
    set 护肤L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='护肤品(脸部)' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新护肤Z
    update sku
    set 护肤Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='护肤品(脸部)' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新化妆工具L
    update sku
    set 化妆工具L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='化妆工具' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新化妆工具Z
    update sku
    set 化妆工具Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='化妆工具' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新美发护理L
    update sku
    set 美发护理L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='美发护理品' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新美发护理Z
    update sku
    set 美发护理Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='美发护理品' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新男士护理L
    update sku
    set 男士护理L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='男士护理品' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新男士护理Z
    update sku
    set 男士护理Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='男士护理品' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新日用品L
    update sku
    set 日用品L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='日用品' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新日用品Z
    update sku
    set 日用品Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='日用品' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新身体护理L
    update sku
    set 身体护理L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='身体护理品' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新身体护理Z
    update sku
    set 身体护理Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='身体护理品' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t1.proid=t2.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新婴童护理L
    update sku
    set 婴童护理L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='婴童护理品' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t1.proid=t2.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新婴童护理Z
    update sku
    set 婴童护理Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='婴童护理品' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新食品L
    update sku
    set 食品L=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='食品' and (t2.bradl<>'自有品牌' or t2.braxl in('碧优然','优丽格')) and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;

    --更新食品Z
    update sku
    set 食品Z=t2.num
    from (
    select t1.braid,COUNT(*) num
    from stock_monthly t1,product_all t2
    where t2.prodl='食品' and t2.bradl='自有品牌' and t2.braxl not in('碧优然','优丽格') and t2.prodl<>'物料赠品'
    and t2.proid=t1.proid
    group by t1.braid
    ) t2
    where sku.门店代码=t2.braid;
    """
    cur.execute(sqlstr)
    conn.commit()

    #最终结果
    """
    CREATE TABLE skuVal
    (
      "月度" character varying(10),
      "门店代码" character varying(255),
      "门店名称" character varying(255),
      "店面面积" numeric(18,0),
      "sku总数" numeric(18,0),
      "流通品牌" numeric(18,0),
      "自有品牌" numeric(18,0),
      "彩妆l" numeric(18,0),
      "彩妆z" numeric(18,0),
      "护肤l" numeric(18,0),
      "护肤z" numeric(18,0),
      "化妆工具l" numeric(18,0),
      "化妆工具z" numeric(18,0),
      "美发护理l" numeric(18,0),
      "美发护理z" numeric(18,0),
      "男士护理l" numeric(18,0),
      "男士护理z" numeric(18,0),
      "日用品l" numeric(18,0),
      "日用品z" numeric(18,0),
      "身体护理l" numeric(18,0),
      "身体护理z" numeric(18,0),
      "婴童护理l" numeric(18,0),
      "婴童护理z" numeric(18,0),
      "食品l" numeric(18,0),
      "食品z" numeric(18,0)
    );
    """
    sqlstr="delete from skuVal where 月度='"+lastmonth+"';"
    sqlstr+="insert into skuVal"
    sqlstr+="select '"+lastmonth+"' 月度,t1.* from sku t1;"

