#!coding:utf8
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql
from mylog import log
from django.utils import simplejson
from functions import trim_csv,verifyData
confsql=confsql.Confsql()
def import_product_gl_packetqty_rules(request):
    '商品配送规则导入'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=4)
        rs2,rs1=verifyData(rs1,length=4,required=[0,2,3],psrules=1)

        '代码长度检查'
        temp=[]
        for rs in rs1:
            if rs[2]==u"商品代码" or rs[2]==u"小类代码":
                if len(rs[0])<>8:
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
            if rs[2]==u"中类代码":
                if len(rs[0])<>5:
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
            if rs[2]==u"大类代码":
                if len(rs[0])<>2:
                    rs.append(u'代码长度不符！')
                    temp.append(rs)
                    rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        temp=[]
        for rs in rs1:
            excode=rs[2]
            if rs[2]==u'商品代码':
                excode='sp'
                sqlstr="select * from product_all where proid='"+rs[0]+"'"
            if rs[2]==u'小类代码':
                excode='xl'
                sqlstr="select * from product_all where proxl_id='"+rs[0]+"'"
            if rs[2]==u'中类代码':
                sqlstr="select * from product_all where prozl_id='"+rs[0]+"'"
                excode='zl'
            if rs[2]==u'大类代码':
                sqlstr="select * from product_all where prodl_id='"+rs[0]+"'"
                excode='dl'
            '无匹配的代码名称'
            if confsql.checkExist(sqlstr)==0:
                rs.append(u'无匹配的代码名称!')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        temp=[]
        for rs in rs1:
            excode=rs[2]
            if rs[2]==u'商品代码':
                excode='sp'
            if rs[2]==u'小类代码':
                excode='xl'
            if rs[2]==u'中类代码':
                excode='zl'
            if rs[2]==u'大类代码':
                excode='dl'
            '重复项覆盖'
            sqlstr="select * from product_gl_packetqty_rules where xcode='"+rs[0]+"' and excode='"+excode+"'"
            if confsql.checkExist(sqlstr)==1: #检查xcode,excode,packetqty 数据库是否已存在
                rs.append(u'数据库已存在!')
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

        html=u"<table width='800'><tr><th>代码</th><th>名称</th><th>代码说明</th><th>配货单位</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td style='background-color:yellow;'>" + rs[4] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(html)
    else:
        t=get_template('mana1/import_product_gl_packetqty_rules.html')
        html=t.render(Context())
        return HttpResponse(html)

def save_product_gl_packetqty_rules(request):
    '保存商品配货单位规则'
    rs1=[]
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])

    #sp, xl, zl, dl, null
    for rs in rs1:
        excode=rs[2]
        if rs[2]==u'商品代码':
            excode='sp'
        if rs[2]==u'小类代码':
            excode='xl'
        if rs[2]==u'中类代码':
            excode='zl'
        if rs[2]==u'大类代码':
            excode='dl'

        if rs[4]<>'':
            if rs[4]==u'数据库已存在!':
                try:
                    sqlstr="delete from product_gl_packetqty_rules where xcode='"+rs[0]+"' and excode='" + excode + "'"
                    confsql.runSql(sqlstr)
                    sqlstr="insert into product_gl_packetqty_rules (xcode,excode,packetqty1) values('"+rs[0]+"','"+excode+"','"+rs[3]+"')"
                    confsql.runSql(sqlstr)
                    rs[4]='插入成功!'
                except:
                    rs[4]='插入失败!'
                res={}
                res['xcode']=rs[0]
                res['name']=rs[1]
                res['excode']=rs[2]
                res['packetqty1']=rs[3]
                res['info']=rs[4]
                result.append(res)
            else:
                res={}
                res['xcode']=rs[0]
                res['name']=rs[1]
                res['excode']=rs[2]
                res['packetqty1']=rs[3]
                res['info']=rs[4]
                result.append(res)
        else:
            try:
                sqlstr="insert into product_gl_packetqty_rules (xcode,excode,packetqty1) values('"+rs[0]+"','"+excode+"','"+rs[3]+"')"
                confsql.runSql(sqlstr)
                rs[4]='插入成功!'
            except:
                rs[4]='插入失败!'
            res={}
            res['xcode']=rs[0]
            res['name']=rs[1]
            res['excode']=rs[2]
            res['packetqty1']=rs[3]
            res['info']=rs[4]
            result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

def insult_product_gl_packetqty_rules(request):
    '查询商品配送单位规则'
    t=get_template('mana1/insult_product_gl_packetqty_rules.html')
    sqlstr="select t1.xcode,t2.proname,'商品代码',round(t1.packetqty1) from product_gl_packetqty_rules t1,product_all t2 where t1.xcode=t2.proid and excode='sp' group by t1.xcode,t2.proname,t1.packetqty1 union all "
    sqlstr+="select t1.xcode,t2.proxl,'小类代码',round(t1.packetqty1) from product_gl_packetqty_rules t1,product_all t2 where t1.xcode=t2.proxl_id and excode='xl' group by t1.xcode,t2.proxl,t1.packetqty1 union all "
    sqlstr+="select t1.xcode,t2.prozl,'中类代码',round(t1.packetqty1) from product_gl_packetqty_rules t1,product_all t2 where t1.xcode=t2.prozl_id and excode='zl' group by t1.xcode,t2.prozl,t1.packetqty1 union all "
    sqlstr+="select t1.xcode,t2.prodl,'大类代码',round(t1.packetqty1) from product_gl_packetqty_rules t1,product_all t2 where t1.xcode=t2.prodl_id and excode='dl' group by t1.xcode,t2.prodl,t1.packetqty1 "
    result=confsql.runquery(sqlstr)
    html=t.render(Context({'result':result}))
    return HttpResponse(html)

def delete_product_gl_packetqty_rules(request):
    '删除配货规则'
    if request.method=='POST':
        value=request.POST['value']
        rs1=trim_csv(value,itemlenth=4)
        rs2,rs1=verifyData(rs1,length=4,required=[0,2,3],psrules=1)

        html=u"<table width='800'><tr><th>代码</th><th>名称</th><th>代码说明</th><th>配货单位</th></tr>"
        if len(rs2)>0:
            for rs in rs2:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td style='background-color:yellow;'>" + rs[4] + "</td>"
                html+="</tr>"
        if len(rs1)>0:
            for rs in rs1:
                html+="<tr>"
                html+="<td>" + rs[0] + "</td>"
                html+="<td>" + rs[1] + "</td>"
                html+="<td>" + rs[2] + "</td>"
                html+="<td>" + rs[3] + "</td>"
                html+="<td></td>"
                html+="</tr>"
        html+="</table>"
        return HttpResponse(html)
    else:
        t=get_template('mana1/delete_product_gl_packetqty_rules.html')
        html=t.render(Context())
        return HttpResponse(html)

def deleteData_product_gl_packetqty_rules(request):
    '删除数据'
    result=[]
    myjson=simplejson.loads(request.POST["myjson"])
    rs1=trim_csv(myjson["table"])
    #log(rs1)
    if len(rs1)>0:
        for rs in rs1:
            if rs[4]<>'': #出错信息的保留
                res={}
                res['xcode']=rs[0]
                res['name']=rs[1]
                res['excode']=rs[2]
                res['packetqty1']=rs[3]
                res['info']=rs[4]
                result.append(res)
            else:
                try:
                    #sp, xl, zl, dl, null
                    excode=rs[2]
                    if rs[2]==u'商品代码':
                        excode='sp'
                    if rs[2]==u'小类代码':
                        excode='xl'
                    if rs[2]==u'中类代码':
                        excode=u'zl'
                    if rs[2]=='大类代码':
                        excode=u'dl'
                    #log("delete from product_gl_packetqty_rules where xcode='"+rs[0]+"' and excode='"+excode+"'")
                    confsql.runSql("delete from product_gl_packetqty_rules where xcode='"+rs[0]+"' and excode='"+excode+"'")
                    
                    res={}
                    res['xcode']=rs[0]
                    res['name']=rs[1]
                    res['excode']=rs[2]
                    res['packetqty1']=rs[3]
                    res['info']=u'删除成功!'
                    result.append(res)
                except:
                    res={}
                    res['xcode']=rs[0]
                    res['name']=rs[1]
                    res['excode']=rs[2]
                    res['packetqty1']=rs[3]
                    res['info']=u'删除失败!'
                    result.append(res)

    jsonres=simplejson.dumps(result)
    return HttpResponse(jsonres)

if __name__=='__main__':
    import_product_gl_packetqty_rules()

