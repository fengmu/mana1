#encoding:utf-8
'''
#=============================================================================
#     FileName: views.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-08-24 11:55:10
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql,datetime,memcache
from django.utils import simplejson
import writemc
from mylog import log

confsql=confsql.Confsql()
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def delivery(request):
    ''' 配送规则导入界面 '''
    result=[] #存放初始表头
    t=get_template('mana1/delivery.html')
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

def insult_delivery(request):
    ''' 配送规则查询界面 '''
    result=[] #存放初始表头
    if request.method=='POST':
        jlist=simplejson.loads(request.POST["jsonlist"])
        if jlist['braid']<>'' or jlist['weekdelivery']<>'' or jlist['braname']<>'': #不全为空
            sqlstr='select * from (select t1.braid,t2.braname,t1.weekdelivery,t1.adddate from delivery t1,branch t2 where t1.braid=t2.braid) t1 where '
            for j in jlist:
                if jlist[j]<>'':
                    li=jlist[j].split(",")
                    if len(li)==1:
                        sqlstr+=j+" like '%%"+jlist[j].strip()+"%%' and "
                    else:
                        sqlstr+="("
                        for l in li:
                            sqlstr+=j+" like '%%"+l.strip() +"%%' or  "
                        sqlstr=sqlstr[0:-4]+") and "
            sqlstr=sqlstr[0:-4] #去除最后多余的and
            lines=confsql.runquery(sqlstr)
            for rs in lines:
                res={}
                res['braid']=rs[0]
                res['braname']=rs[1]
                res['weekdelivery']=rs[2]
                res['adddate']=rs[3]
                result.append(res)
            jsonres=simplejson.dumps(result)
            return  HttpResponse(jsonres)
        else: #全为空，查询所有
            sqlstr='select * from delivery'
            lines=confsql.runquery(sqlstr)
            for rs in lines:
                res={}
                res['braid']=rs[0]
                res['braname']=confsql.getbranamefrommc(rs[0])
                res['weekdelivery']=rs[1]
                res['adddate']=rs[2]
                result.append(res)
            jsonres=simplejson.dumps(result)
            return  HttpResponse(jsonres)
    else:
        t=get_template('mana1/insult_delivery.html')
        html=t.render(Context({'result':result}))
        return HttpResponse(html)

def check_delivery(request):
    '''配送规则导入检查并插入数据库'''
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"], itemlenth=3)
    #每做一次检查，从rs1中去除检查项
    #判断字段数是否符合
    rs2=[] #存放最终结果
    rs3=[] #存放临时数据
    for rs in rs1:
        if len(rs)<3:
            rs3.append(rs)
            rs.append(u'格式不对')
            rs2.append(rs)
    if len(rs3)>0:
        for rs in rs3:
            rs1.remove(rs)

    #必填项检查
    rs3=[]
    flag=True
    for rs in rs1:
        for res in rs:
            if res=='':
                flag=False
        if flag==False:
            rs3.append(rs)
            rs.append(u'必填字段不能为空')
            rs2.append(rs)
            flag=True
    if len(rs3)>0:
        for rs in rs3:
            rs1.remove(rs)

    #配送周格式不对
    myweek=[u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日']
    rs3=[]
    for rs in rs1:
        if rs[2] in myweek:
            pass
        else:
            rs3.append(rs)
            rs.append(u'日期格式应为：星期X')
            rs2.append(rs)
    if len(rs3)>0:
        for rs in rs3:
            rs1.remove(rs)

    rs3=[]
    for rs in rs1:
        if confsql.verify("select * from delivery where braid='"+rs[0]+"'"): #数据库已存在则覆盖
            confsql.delivery_del(braid=rs[0])
    
    for rs in rs1:        
        rs.append(datetime.datetime.now().strftime('%Y-%m-%d')) #最后追加插入日期
        confsql.delivery_insert(braid=rs[0],weekdelivery=rs[2],adddate=rs[3])
        rs3=[rs[0],rs[1],rs[2]]
        rs3.append('保存成功！')
        rs2.append(rs3)

    for rs in rs2:
        res={}
        res['braid']=rs[0]
        res['braname'] = rs[1]
        res['weekdelivery']=rs[2]
        res['info']=rs[3] #导入情况
        result.append(res)
    jsonres=simplejson.dumps(result)
    return  HttpResponse(jsonres)


def save_delivery(request):
    value=request.POST['value'].encode("utf-8")
    rs1=[]
    result=[]
    rs1=trim_csv(value, itemlenth=3) #去除行尾多余换行符 rs1存放初始值
    #每做一次检查，从rs1中去除检查项
    #判断字段数是否符合
    rs2=[] #存放最终结果
    rs3=[] #存放临时数据
    for rs in rs1:
        if len(rs)<3:
            rs3.append(rs)
            rs.append('格式不对')
            rs2.append(rs)
    if len(rs3)>0:
        for rs in rs3:
            rs1.remove(rs)
    #必填项检查
    rs3=[]
    flag=True
    for rs in rs1:
        for res in rs:
            if res=='':
                flag=False
        if flag==False:
            rs3.append(rs)
            rs.append('必填字段不能为空')
            rs2.append(rs)
            flag=True
    if len(rs3)>0:
        for rs in rs3:
            rs1.remove(rs)

    #配送周格式不对
    myweek=['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    rs3=[]
    for rs in rs1:
        if rs[2] in myweek:
            pass
        else:
            rs3.append(rs)
            rs.append('日期格式应为：星期X')
            rs2.append(rs)
    if len(rs3)>0:
        for rs in rs3:
            rs1.remove(rs)

    #数据库已存在给予提示
    rs3=[]
    for rs in rs1:
        if confsql.verify("select * from delivery where braid='"+rs[0]+"'"):
            rs3.append(rs)
            rs.append('')
            rs2.append(rs)
    if len(rs3)>0:
        for rs in rs3:
            rs1.remove(rs)

    for rs in rs1:
        rs.append('')
        rs2.append(rs)

    html="<table width='800'><tr><th>门店代码</th><th>门店名称</th><th>配送周</th></tr>"
    for rs in rs2:
        html+="<tr>"
        html+="<td>" + rs[0] + "</td>"
        html+="<td>" + rs[1] + "</td>"
        html+="<td>" + rs[2] + "</td>"
        if rs[3]=="":
            html+="<td>" + rs[3] + "</td>"
        else:
            html+="<td style='background-color:yellow;'>" + rs[3] + "</td>"
        html+="</tr>"
    html+="</table>"
    return HttpResponse(html)

def insult_sugvalue(request):
    ''' 建议值查询界面 '''
    result=[] #存放初始表头
    if request.method=='POST':
        jlist=simplejson.loads(request.POST["jsonlist"])
        ty=request.POST["ty"]
        if ty=="sub": #非聚集
            if jlist['proid']<>'' or jlist['proname']<>'' or jlist['braid']<>'' or jlist['braname']<>'': #不全为空
                sqlstr='select * from sugvalue where suggest>0 and '
                for j in jlist:
                    if jlist[j]<>'':
                        li=jlist[j].split(",")
                        if len(li)==1:
                            sqlstr+=j+" like '%%"+jlist[j].strip()+"%%' and "
                        else:
                            sqlstr+="("
                            for l in li:
                                sqlstr+=j+" like '%%"+l.strip() +"%%' or  "
                            sqlstr=sqlstr[0:-4]+") and "
                sqlstr=sqlstr[0:-4] #去除最后多余的and
                #sqlstr += " suggest>0 "
                lines=confsql.runquery(sqlstr)
                for rs in lines:
                    res={}
                    res['门店代码']=rs[0]
                    res['门店名称']=rs[1]
                    res['商品代码']=rs[2]
                    res['商品名称']=rs[3]
                    res['建议配货量']=rs[4]
                    res['配货总金额']=rs[5]
                    result.append(res)
                jsonres=simplejson.dumps(result)
                return  HttpResponse(jsonres)
            else:
                #sqlstr='select * from sugvalue'
                sqlstr='select * from sugvalue where suggest>0 '
                lines=confsql.runquery(sqlstr)
                for rs in lines:
                    res={}
                    res['门店代码']=rs[0]
                    res['门店名称']=rs[1]
                    res['商品代码']=rs[2]
                    res['商品名称']=rs[3]
                    res['建议配货量']=rs[4]
                    res['配货总金额']=rs[5]
                    result.append(res)
                jsonres=simplejson.dumps(result)
                return  HttpResponse(jsonres)
        else: #聚集结果
            if jlist['proid']<>'' or jlist['proname']<>'' or jlist['braid']<>'' or jlist['braname']<>'': #不全为空
                items=""
                dic={'proid':'商品代码','proname':'商品名称','braid':'门店代码','braname':'门店名称'}
                for j in jlist:
                    if jlist[j]<>'':
                        items+=j+","
                items=items[0:-1]
                sqlstr='select '+items+',sum(suggest) as suggest,sum(suggestcost) as suggestcost from sugvalue where suggest>0 and '
                for j in jlist:
                    if jlist[j]<>'':
                        sqlstr+=j+" like '%%"+jlist[j].strip() +"%%' and "
                sqlstr=sqlstr[0:-4] #去除最后多余的and
                #sqlstr += " suggest>0 "
                sqlstr+="group by "+items
                lines=confsql.runquery(sqlstr)
                for rs in lines:
                    i=0
                    res={}
                    for j in jlist:
                        if jlist[j]<>'':
                            res={}
                            res[dic[j]]=rs[i]
                            i+=1
                    res['建议配货量']=rs[i]
                    res['配货总金额']=rs[i+1]
                    result.append(res)
                jsonres=simplejson.dumps(result)
                return  HttpResponse(jsonres)
            else:
                #sqlstr='select * from sugvalue'
                sqlstr='select * from sugvalue where suggest>0 '
                lines=confsql.runquery(sqlstr)
                for rs in lines:
                    res={}
                    res['门店代码']=rs[0]
                    res['门店名称']=rs[1]
                    res['商品代码']=rs[2]
                    res['商品名称']=rs[3]
                    res['建议配货量']=rs[4]
                    res['配货总金额']=rs[5]
                    result.append(res)
                jsonres=simplejson.dumps(result)
                return  HttpResponse(jsonres)
    else:
        t=get_template('mana1/insult_sugvalue.html')
        html=t.render(Context({'result':result}))
        return HttpResponse(html)

def checkAdvMaxMin(request):
    advMaxMin = getadvMaxMinfrommc()

    advMaxMinlist = []
    if advMaxMin:
        advMaxMins = advMaxMin.split(",")
        advMaxMinlist = [  x.split("__") for x in advMaxMins]
    else:
        advMaxMinlist = []

    t=get_template('mana1/checkAdvMaxMin.html')

    html=t.render(Context({"MaxMinTable":fmw2Htmltable(addInfo(advMaxMinlist))}))
    return HttpResponse(html)

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

def fmw2Htmltable(infolist):

    Htmltable = "<table>"
    reader =[["标记", "门店代码", "门店名称", "商品代码", "商品名称", "原上限", "原下限", "新上限", "新下限"]] + infolist

    j = 0
    for row in reader: # Read a single row from the CSV file
        if (j == 0 and len(row) > 0):             # 第一行是表头
            Htmltable = Htmltable +'<thead><tr class="'+row[1]+'" >'  # Create a new row in the table
            i = 0
            for column in row: # For each column..
                Htmltable = Htmltable  + '<th class="FmCol' +str(i) +'" >'+ column + '</th>'
                i = i + 1
            Htmltable = Htmltable + '</tr></thead><tbody>'
        if (j>0 and len(row)>0):
            Htmltable = Htmltable +'<tr class="'+row[1]+'" >'  # Create a new row in the table
            i = 0
            for column in row: # For each column..
                if i == 0:
                    if column == "0" :
                        Htmltable = Htmltable  + '<td class="FmCol' +str(i) +'" ><input id="a' + str(j) +'"  type="checkbox" style="" ></td>'
                    else:
                        Htmltable = Htmltable  + '<td class="FmCol' +str(i) +'" ><input id="a' + str(j) +'"  type="checkbox" style="" checked="checked"></td>'
                elif i == 7 or i== 8:
                    Htmltable = Htmltable  + '<td class="FmCol' +str(i) +'" ><input id="a' + str(j) +'"  type="text" style="width:50px;border-bottom-style:none;border-top-style:none;border-left-style:none;border-right-style:none;color:red;background:#e5f1f4;font:120%" value="'+column+'"></td>'
                else:
                    Htmltable = Htmltable  + '<td class="FmCol' +str(i) +'" >'+ column + '</td>'
                i = i + 1
            Htmltable = Htmltable + '</tr>'
        j = j + 1

    Htmltable = Htmltable + '</tbody></table>'
    return Htmltable

def tranedit(request):
    myValue = request.POST["value"].encode("utf-8")
    myValuelist = fmwConvertList(myValue, '\n')
    myValuelist2 = [ fmwConvertList(x, '\t') for x in myValuelist]
    myValuelist2.pop(0)    #标题
    myNewValue =  fmw2Htmltable(myValuelist2)
    return HttpResponse(myNewValue)

def fmwConvertList(str, split):
    strlist = []
    if len(str)>0:
        strlist = str.split(split)
    return strlist

def check_advmaxmin(request):
    fmdata = simplejson.loads(request.POST["myjson"])
    fmdatatag = fmdata["tag"]
    fmdatalist= fmwConvertList(fmdata["table"].encode("utf-8"), '\n')
    fmdatalist2 = [ fmwConvertList(x, '\t') for x in fmdatalist]
    fmdatalist2.pop(0)
    tag_fmdata   = [ x for x in fmdatalist2 if x[0] =="1"]
    notag_fmdata = [ x for x in fmdatalist2 if x[0] =="0"]
    if fmdatatag == 'del':
        setadvMaxMin(notag_fmdata)
        myNewValue = fmw2Htmltable(notag_fmdata)
    elif fmdatatag == 'save':
        setadvMaxMin(notag_fmdata)
        updateMaxMin(tag_fmdata)
        tag_fmdata2 = [ x + ["数据已保存"] for x in tag_fmdata]
        myNewValue = fmw2Htmltable(tag_fmdata2+notag_fmdata)
        #myNewValue = str(tag_fmdata2)
    else:
        myNewValue = fmw2Htmltable([])
    return HttpResponse(myNewValue)

def setadvMaxMin(datalist):
    for x in datalist:
        cachedAdvMaxMin(x[1], x[3], x[5], x[6], x[7], x[8])

def getadvMaxMinfrommc():
    advMaxMin = mc.get("advMaxMin")
    mc.delete("advMaxMin")
    return advMaxMin

def cachedAdvMaxMin(mdcode, spcode, oldmax, oldmin, newmax, newmin):
    advMaxMin = mc.get("advMaxMin")
    myvalue = str(mdcode) +"__"+ spcode + "__" + oldmax + "__" + oldmin +"__"+ newmax +"__"+ newmin  #这里有陷阱，首选必须用str
    if not advMaxMin :
        mc.set("advMaxMin", myvalue)
    else:
        mc.append("advMaxMin", ","+myvalue)

def updateMaxMin(datalist):
    for x in datalist:
        confsql.maxmin_update(x[1], x[3], x[5], x[6], x[7], x[8])

def rewrite_verify(request): #审核处理重写
    #os.system("cmd /c D:/django/mysite/mana1/writemc.py")
    myjson = simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],7)
    s="" #存放门店名单
    for rs in rs1:
        if rs[0]=="1": #勾选的门店
            s+="'"+rs[1]+"',"
    s=s[0:-1]
    #os.system('cmd.exe /c c:/ZSW/memcached/memcached.exe -m 256 -p 11211') #开启内存服务
    html=""
    if s<>"":
        writemc.Writemc(sqlstr=s)
        result=confsql.runquery(u"select * from brainfo where 门店代码 in("+s+")") #获取门店综合信息 供门店审核是否需要重写
        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"
        for rs in result:
            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"
        return HttpResponse(html)
    else:
        writemc.Writemc() #全部重写
        result=confsql.runquery("select * from brainfo") #获取门店综合信息 供门店审核是否需要重写
        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"
        for rs in result:
            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"
        return HttpResponse(html)

def rewrite(request):
    if request.method=='POST':
        #检查格式是否正确，并返回检查结果
        rs1=trim_csv(request.POST['value'],itemlenth=7)
        rs2=[] #存放最终结果
        rs_temp=[] #存放临时数据
        #不能有空
        for rs in rs1:
            if rs[0]=="" or rs[1]=="" or rs[2]==""  or rs[3]=="" or rs[4]=="" or rs[5]=="" or rs[6]=="":
                rs_temp.append(rs)
                rs.append("不能有为空的项")
                rs2.append(rs)
        if len(rs_temp)>0:
            for rs in rs_temp:
                rs1.remove(rs)

        rs_temp=[] #存放临时数据
        #门店代码为五位码
        for rs in rs1:
            if len(rs[1])<>5:
                rs_temp.append(rs)
                rs.append("门店代码应为五位码")
                rs2.append(rs)
        if len(rs_temp)>0:
            for rs in rs_temp:
                rs1.remove(rs)

        #没有问题的数据
        for rs in rs1:
            rs.append("")
            rs2.append(rs)

        s="<table width='800'><tr><th>审核</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th><th>说明</th></tr>"
        for rs in rs2:
            if rs[0]=='0':
                s+="<tr><td><input type='checkbox'></td>"
            else:
                s+="<tr><td><input type='checkbox' checked='checked'></td>"
            s+="<td>"+rs[1]+"</td><td>"+rs[2]+"</td><td>"+rs[3]+"</td><td>"+rs[4]+"</td><td>"+rs[5]+"</td><td>"+rs[6]+"</td>"
            if rs[7]=="":
                s+="<td>"+rs[7]+"</td></tr>"
            else:
                s+="<td style='background-color:yellow'>"+rs[7]+"</td></tr>"
        s+="</table>"
        return HttpResponse(s)
    else:
        t=get_template("mana1/rewrite.html")
        #result=[{"门店代码":"00001","品项数":3500,"库存数量":23340,"库存金额":4337979.32,"建议订货总量":2344,"建议订货总额":34345434},{"门店代码":"00002","品项数":3500,"库存数量":23340,"库存金额":4337979.32,"建议订货总量":2344,"建议订货总额":34345434},{"门店代码":"00003","品项数":3500,"库存数量":23340,"库存金额":4337979.32,"建议订货总量":2344,"建议订货总额":34345434}]
        result=confsql.runquery("select 门店代码, 门店名称, 品项数, 库存数量, 建议订货总量, 建议订货总额 from brainfo") #获取门店综合信息 供门店审核是否需要重写
        html=t.render(Context({'result':result}))
        return  HttpResponse(html)

def cleanmc_verify(request): #审核处理清空内存建议值
    #os.system("cmd /c D:/django/mysite/mana1/writemc.py")
    myjson = simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"],7)
    s=[] #存放门店名单
    for rs in rs1:
        if rs[0]=="1": #勾选的门店
            s.append(rs[1])
    html=""
    if len(s)>0:
        for rs in s:
            #清空数据库指定建议值及内存指定建议值
            result=confsql.runquery("select * from sugvalue where braid='"+str(rs)+"'")
            for rs in result:
                mc.delete(str(rs['braid'])+"__"+str(rs['proid'])+"__sugvalue") #先根据数据库清内存
                confsql.runquery("delete from sugvalue where braid='"+str(rs['braid'])+"'") #后清数据库
                confsql.runquery("delete from brainfo where 门店代码='"+str(rs['braid'])+"'") 
        result=confsql.runquery("select * from brainfo") #获取门店综合信息 供门店审核是否需要重写
        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"
        for rs in result:
            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"
        return HttpResponse(html)
    else:
        #全部重写
        result=confsql.runquery("select * from sugvalue")
        for rs in result:
            mc.delete(str(rs['braid'])+"__"+str(rs['proid'])+"__sugvalue")
        confsql.runquery("delete from sugvalue")
        confsql.runquery("delete from brainfo")
        result=confsql.runquery("select * from brainfo") #获取门店综合信息 供门店审核是否需要重写
        html="<tr><th>重算</th><th>门店代码</th><th>门店名称</th><th>品项数</th><th>库存数量</th><th>建议订货总量</th><th>建议订货总额</th></tr>"
        for rs in result:
            html+="<tr><td><input type='checkbox'></td><td>"+str(rs[0])+"</td><td>"+str(rs[1].encode("utf8"))+"</td><td>"+str(rs[2])+"</td><td>"+str(rs[3])+"</td><td>"+str(rs[4])+"</td><td>"+str(rs[5])+"</td></tr>"
        return HttpResponse(html)




