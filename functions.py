# -*- coding: utf-8 -*-

#=============================================================================
#     FileName: functions.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-10-24 11:10:25
#      History:
#=============================================================================


from mylog import log
import time
import confsql

confsql=confsql.Confsql()

def getspaceinfo(xcode, excode):
    "根据各类代码,取得对应的货架信息"
    if excode == 'sp':
        sqlstr="select spaceid,spacename,assortment from dhalldata where spcode='"+xcode+"' and spaceid is not null group by spaceid,spacename,assortment"
        result=confsql.runquery(sqlstr)
        res=[]
        for rs in result:
            items={}
            items['spaceid']=rs[0]
            items['spacename']=rs[1]
            items['assortment']=rs[2]
            res.append(items)
        if len(res) > 0:
            return res
        else:
            sqlstr = "select braxl_id from product_all where proid='"+xcode+"'"
            result=confsql.runquery(sqlstr)
            if len(result) == 0:
                return []
            else:
                xcode = result[0][0]
                excode = 'pbxl'
                return getspaceinfo(xcode, excode)
    if excode == 'pbxl':
        sqlstr="select spaceid,spacename,assortment from dhalldata where braxl_id='"+xcode+"' and spaceid is not null group by spaceid,spacename,assortment"
        result=confsql.runquery(sqlstr)
        res=[]
        for rs in result:
            items={}
            items['spaceid']=rs[0]
            items['spacename']=rs[1]
            items['assortment']=rs[2]
            res.append(items)
        if len(res) > 0:
            return res
        else:
            sqlstr = "select proxl_id from product_all where braxl_id='"+xcode+"'"
            result=confsql.runquery(sqlstr)
            if len(result) == 0:
                return []
            else:
                xcode = result[0][0]
                excode = 'xl'
                return getspaceinfo(xcode, excode)
    if excode == 'xl':
        sqlstr="select spaceid,spacename,assortment from dhalldata where proxl_id='"+xcode+"' and spaceid is not null group by spaceid,spacename,assortment"
        result=confsql.runquery(sqlstr)
        res=[]
        for rs in result:
            items={}
            items['spaceid']=rs[0]
            items['spacename']=rs[1]
            items['assortment']=rs[2]
            res.append(items)
        if len(res) > 0:
            return res
        else:
            sqlstr = "select prozl_id from product_all where proxl_id='"+xcode+"'"
            result=confsql.runquery(sqlstr)
            if len(result) == 0:
                return []
            else:
                xcode = result[0][0]
                excode = 'zl'
                return getspaceinfo(xcode, excode)
    if excode == 'zl':
        sqlstr="select spaceid,spacename,assortment from dhalldata where prozl_id='"+xcode+"' and spaceid is not null group by spaceid,spacename,assortment"
        result=confsql.runquery(sqlstr)
        res=[]
        for rs in result:
            items={}
            items['spaceid']=rs[0]
            items['spacename']=rs[1]
            items['assortment']=rs[2]
            res.append(items)
        if len(res) > 0:
            return res
        else:
            sqlstr = "select prodl_id from product_all where prozl_id='"+xcode+"'"
            result=confsql.runquery(sqlstr)
            if len(result) == 0:
                return []
            else:
                xcode = result[0][0]
                excode = 'dl'
                return getspaceinfo(xcode, excode)
    if excode == 'dl':
        sqlstr="select spaceid,spacename,assortment from dhalldata where prodl_id='"+xcode+"' and spaceid is not null group by spaceid,spacename,assortment"
        result=confsql.runquery(sqlstr)
        res=[]
        for rs in result:
            items={}
            items['spaceid']=rs[0]
            items['spacename']=rs[1]
            items['assortment']=rs[2]
            res.append(items)
        if len(res) > 0:
            return res
        else:
            return []
                
    
    



def fmwConvertList(str, split):
    strlist = []
    if len(str)>0:
        strlist = str.split(split)
    return strlist


def fmw2Htmltable(infolist):

    Htmltable = "<table>"
    reader =[["标记", "门店代码", "门店名称", "商品代码", "商品名称", "原上限", "原下限", "新上限", "新下限", "申请日期"]] + infolist

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

                    Htmltable = Htmltable  + '<td class="FmCol' +str(i) +'" >'+ str(column) + '</td>'

                i = i + 1

            Htmltable = Htmltable + '</tr>'

        j = j + 1



    Htmltable = Htmltable + '</tbody></table>'

    return Htmltable



def trim_csv(value, itemlenth=0):
    ' 去除csv标题及每行行尾的回车换行符 转换为列表 '
    rs1=[] #存放容器
    i=0
    lines=value.split('\n')
    for line in lines:
        i=i+1
        if i>1 and len(line)>0: #不含首行表头字段
            rs=line.split('\t')
            if itemlenth>0 and len(rs)>itemlenth:
                rs1.append(rs[0:itemlenth]) #超长的给予截取
            else:
                rs1.append(rs) #原样输出
    return rs1

'''
数据有效性检查
传入值:rs1源数据,length长度,required必填项（必填项的序号填在列表中,如[0,1,2],第0列第1列第2列必填）,special特殊规则（通过固定关键字区分,如:psrules=1）
返回值:rs1无误结果，rs2包含错误信息结果

'''
def verifyData(rs1,length=0,required=[],**special):
    #长度检查
    rs2=[] #存放最终结果
    temp=[] #为了能清除上步已检查项需要个临时列表
    if length>0:
        for rs in rs1:
            if(len(rs)<length):
                for i in range(length-len(rs)): #缺的列补齐长度
                    rs.append(u"")
                rs.append(u"数据长度不符！")
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

    #必填项检查
    temp=[]
    if len(required)>0:
        for rs in rs1:
            flag=False
            for re in required:
                if rs[re]=='':
                    flag=True
            if flag==True:
                rs.append(u"必填项不能为空！")
                temp.append(rs)
                rs2.append(rs)
        if len(temp)>0:
            for rs in temp:
                rs1.remove(rs)

    #************特殊项检查****************
    for sp in special:
        if sp=='maxmin': #字符类型检查
            temp=[]
            for rs in rs1:
                if len(rs[0])<>5:
                    rs.append(u"门店代码长度应为5位!")
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)
            temp=[]
            for rs in rs1:
                if len(rs[2])<>8:
                    rs.append(u"商品代码长度应为8位!")
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)
            temp=[]
            for rs in rs1:
                if rs[4].isdigit()==False or rs[5].isdigit()==False:
                    rs.append(u"上下限数据必须是整数!")
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)
            temp=[]
            for rs in rs1: #上限必须大于下限
                if int(rs[4])<int(rs[5]):
                    rs.append(u"上限必须大于下限!")
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

        if special[sp]=='B': #版本选B日期必须填写
            temp=[]
            if special["startdate"]=="" or special["enddate"]=="":
                for rs in rs1:
                    rs.append(u'版本开始结束日期不能为空!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

        if sp=='psrules': #配送规则
            '代码说明：excode值为sp,xl,zl,dl,null'
            temp=[]
            for rs in rs1:
                if rs[2]<>u'商品代码' and rs[2]<>u'小类代码' and rs[2]<>u'中类代码' and rs[2]<>u'大类代码' and rs[2]<>'':
                    rs.append(u'代码说明不符要求!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            '配货单位'
            temp=[]
            for rs in rs1:
                if type(eval(rs[3]))<>type(1) or eval(rs[3])<=1:
                    rs.append(u'规则值应为大于1的整数')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)
        if sp=='delivery':
            #配送周格式不对
            myweek=[u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日']
            temp=[]
            for rs in rs1:
                if rs[2] in myweek:
                    pass
                else:
                    temp.append(rs)
                    rs.append(u'日期格式应为：星期X')
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            temp=[]
            for rs in rs1:
                if len(rs[0])<>5:
                    temp.append(rs)
                    rs.append(u'门店代码应为5位！')
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

        if sp=='dhrules':
            '门店代码:mdcode 5位代码或""'
            temp=[]
            for rs in rs1:
                if len(rs[0])<>5 and rs[0]<>"":
                    rs.append(u'门店代码应为5位')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            '代码长度检查'
            temp=[]
            for rs in rs1:
                if rs[4]==u"商品代码" or rs[4]==u"小类代码":
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

            '代码说明:excode值为sp,xl,zl,dl,""'
            temp=[]
            for rs in rs1:
                if rs[4]<>u'商品代码' and rs[4]<>u'小类代码' and rs[4]<>u'中类代码' and rs[4]<>u'大类代码' and rs[4]<>'':
                    rs.append(u'代码说明不符要求!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            '规则对象:yqkey maxlimit,minlimit'
            temp=[]
            for rs in rs1:
                if rs[5]<>u'上阈值' and rs[5]<>u'下阈值':
                    rs.append(u'规则对象不符!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            '规则说明yqrule jd,xd'
            temp=[]
            for rs in rs1:
                if rs[6]<>u'绝对值' and rs[6]<>u'相对值':
                    rs.append(u'规则说明不符!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            '规则值yqvalue 规则值为jd时整数，为xd时小数'
            temp=[]
            for rs in rs1:
                if (type(eval(rs[7]))<>type(1.00)) and (type(eval(rs[7]))<>type(1)):
                    rs.append(u'规则值应为数值!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

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
                yqkey = rs[5]
                if rs[5]==u'上阈值':
                    yqkey='maxlimit'
                if rs[5]==u'下阈值':
                    yqkey='minlimit'
                sqlstr=u"select * from dhrules where mdcode='"+rs[0]+"' and xcode = '"+ rs[2] +"' and excode='"+excode+"' and yqkey='"+yqkey+"'"
                if confsql.checkExist(sqlstr)==1: #检查mdcode,excode,yqkey数据库是否已存在
                    rs.append(u'数据库已存在!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

        if sp=='dhpauserules':
            '门店代码:mdcode 五位代码或""'
            temp=[]
            for rs in rs1:
                if len(rs[0])<>5 and rs[0]<>"":
                    rs.append(u'门店代码应为五位')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            '代码说明:excode值为sp,xl,zl,dl,""'
            temp=[]
            for rs in rs1:
                if rs[4]<>u'商品代码' and rs[4]<>u'小类代码' and rs[4]<>u'中类代码' and rs[4]<>u'大类代码' and rs[4]<>'':
                    rs.append(u'代码说明不符要求!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

            'startdata, enddate'
            temp=[]
            for rs in rs1:
                startdatestr = rs[5]
                enddatestr = rs[6]
                try:
                    startdate = time.strptime(startdatestr, "%Y-%m-%d")
                    enddate =   time.strptime(enddatestr, "%Y-%m-%d")
                    rs[5] = time.strftime("%Y-%m-%d", startdate)
                    rs[6] = time.strftime("%Y-%m-%d", enddate)
                    #if startdate > enddate :
                        #rs.append(u'错误:开始时间大于结束时间')
                        #temp.append(rs)
                        #rs2.append(rs)

                except:
                    rs.append(u'时间格式不对!')
                    temp.append(rs)
                    rs2.append(rs)
            if len(temp)>0:
                for rs in temp:
                    rs1.remove(rs)

    return (rs2,rs1) #返回不符合规则的和符合规则的

if __name__=='__main__':
    x = getspaceinfo('test', 'sp')
    print str(x)

