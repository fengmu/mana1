# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: rewrite.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-28 18:31:07
#      History:
#=============================================================================
'''
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql,datetime,memcache
from django.utils import simplejson
import functions
from mylog import log

confsql=confsql.Confsql()
def rewrite(request):

    if request.method=='POST':

        #检查格式是否正确，并返回检查结果

        rs1=functions.trim_csv(request.POST['value'],itemlenth=7)

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



