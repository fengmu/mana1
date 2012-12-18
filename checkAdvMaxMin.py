# -*- coding: utf-8 -*-


import datetime
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql,datetime,memcache
from django.utils import simplejson

import functions
from mylog import log

confsql=confsql.Confsql()
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def checkAdvMaxMin(request):
    advMaxMinlist = getadvMaxMinfrommc()
    insertAdvMaxMin(advMaxMinlist)
    
    advMaxMinlist2 = confsql.getAllAdvMaxMin()
    advMaxMinlist3 = convertAdvMaxMin(advMaxMinlist2)

    t=get_template('mana1/checkAdvMaxMin.html')

    html=t.render(Context({"MaxMinTable":functions.fmw2Htmltable(advMaxMinlist3)}))
    return HttpResponse(html)

def getadvMaxMinfrommc():
    advMaxMin = mc.get("advMaxMin")
    advMaxMinlist = []
    if advMaxMin:
        advMaxMins = advMaxMin.split(",")
        advMaxMinlist = [  x.split("__") for x in advMaxMins]
    else:
        advMaxMinlist = []
    mc.delete("advMaxMin")
    return advMaxMinlist

def insertAdvMaxMin(advMaxMinlist):
    applyfordate=datetime.datetime.now().strftime('%Y-%m-%d')
    remarks = ''
    verifydate = ''
    if len(advMaxMinlist)>0:
        for line in advMaxMinlist:
            confsql.insertAdvMaxMin(line[0], line[1], line[2], line[3], line[4], line[5], applyfordate, verifydate, remarks)
            
def convertAdvMaxMin(advMaxMinlist):
    if len(advMaxMinlist)>0:
        return [["0", x[0], x[1], x[2], x[3], str(int(x[4])), str(int(x[5])), str(int(x[6])), str(int(x[7])), x[8]] for x in advMaxMinlist ]
    else:
        return []
            

    


def addInfo(advMaxMinlist):
    result = []
    mylen = len(advMaxMinlist)

    if mylen>0:
        for line in advMaxMinlist:
            checktag = '0'
            mdcode = line[0].encode("utf-8")
            try:
                mdname1 = mc.get(mdcode+"__braname")
                mdname = mdname1.encode("utf-8")
            except:
                mdname = "x"
            spcode = line[1].encode("utf-8")
            try:
                spname1 = mc.get(spcode+"__proname")
                spname = spname1.encode("utf-8")
            except:
                spname = "x"
            oldmax = line[2].encode("utf-8")
            oldmin = line[3].encode("utf-8")
            newmax = line[4].encode("utf-8")
            newmin = line[5].encode("utf-8")
            result.append([checktag, mdcode, mdname, spcode, spname, oldmax, oldmin, newmax, newmin])
        return result
    else:
        return result


def save_checkAdvMaxMin(request):

    fmdata = simplejson.loads(request.POST["myjson"])

    fmdatatag = fmdata["tag"]

    fmdatalist= functions.fmwConvertList(fmdata["table"].encode("utf-8"), '\n')

    fmdatalist2 = [ functions.fmwConvertList(x, '\t') for x in fmdatalist]

    fmdatalist2.pop(0)

    tag_fmdata   = [ x for x in fmdatalist2 if x[0] =="1"]

    notag_fmdata = [ x for x in fmdatalist2 if x[0] =="0"]

    if fmdatatag == 'del':

        setadvMaxMin(tag_fmdata)

        myNewValue = functions.fmw2Htmltable(notag_fmdata)

    elif fmdatatag == 'save':
        

        updateMaxMin(tag_fmdata)

        tag_fmdata2 = [ x + ["数据已保存"] for x in tag_fmdata]

        myNewValue = functions.fmw2Htmltable(tag_fmdata2+notag_fmdata)

        #myNewValue = str(tag_fmdata2)

    else:

        myNewValue = functions.fmw2Htmltable([])

    return HttpResponse(myNewValue)


def setadvMaxMin(datalist):
    remarks = 'del'
    verifydate = datetime.datetime.now().strftime('%Y-%m-%d')

    for x in datalist:

        #cachedAdvMaxMin(x[1], x[3], x[5], x[6], x[7], x[8])
        confsql.insertAdvMaxMin(x[1], x[3], x[5], x[6], x[7], x[8], x[9], verifydate, remarks)


def updateMaxMin(datalist):
    remarks = 'save'
    verifydate = datetime.datetime.now().strftime('%Y-%m-%d')

    for x in datalist:        
        confsql.maxmin_update(x[1], x[3], x[5], x[6], x[7], x[8])
        confsql.insertAdvMaxMin(x[1], x[3], x[5], x[6], x[7], x[8], x[9], verifydate, remarks)


def cachedAdvMaxMin(mdcode, spcode, oldmax, oldmin, newmax, newmin):

    advMaxMin = mc.get("advMaxMin")

    myvalue = str(mdcode) +"__"+ spcode + "__" + oldmax + "__" + oldmin +"__"+ newmax +"__"+ newmin  #这里有陷阱，首选必须用str

    if not advMaxMin :

        mc.set("advMaxMin", myvalue)

    else:

        mc.append("advMaxMin", ","+myvalue)
        
        
        
def insult_checkAdvMaxMin(request):
    result=[] #存放初始表头
    sqlstr="select t1.mdcode,t2.braname,t1.spcode,t3.proname,t3.prodl_id||'_'||t3.prodl,t3.prozl_id||'_'||t3.prozl,t3.proxl_id||'_'||t3.proxl,t1.oldmaxval,t1.oldminval,t1.newmaxval,t1.newminval,t1.applyfordate,t1.verifyDate, case when t1.remarks = 'save' then '同意' when t1.remarks = 'del' then '不同意' else '未审核' end  as remarks from advmaxmin t1,branch t2,product_all t3 where t1.mdcode=t2.braid and t1.spcode=t3.proid limit 20000"
    lines=confsql.runquery(sqlstr)
    for rs in lines:
        res={}
        res['mdcode']=rs[0]
        res['braname']=rs[1]
        res['spcode']=rs[2]
        res['proname']=rs[3]
        res['prodl']=rs[4]
        res['prozl']=rs[5]
        res['proxl']=rs[6]
        res['oldmaxval']=rs[7]
        res['oldminval']=rs[8]
        res['newmaxval']=rs[9]
        res['newminval']=rs[10]
        res['applyfordate']=rs[11]
        res['verifyDate']=rs[12]
        res['remarks'] = rs[13]
        result.append(res)
    t=get_template('mana1/insult_checkadvmaxmin.html')
    html=t.render(Context({"result":result}))
    return HttpResponse(html)

