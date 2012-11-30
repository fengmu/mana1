# -*- coding: utf-8 -*-
import time,datetime
import psycopg2
import psycopg2.extensions
import confsql

downloaddir = 'D:/getdata/ftp/'

yqfiles = ['product',
           'product_all',
           'v_allstock',
           'v_com_branch',
           'alloc','pmt',
           'v_sale_daily',
           'v_com_product']

#需要清空的数据表
tables = ["product;",
          "product_all",
          "allstock",
          "branch",
          "maxminval",
          "deliveryval",
          "brainfo",
          "sugvalue",
          "sugvalue_temp",
          "alloc",
          "pmt",
          "v_sale_daily",
          "xiaoshou28_res",
          "xiaoshou28_res_temp",
          "splb",
          "dhalldata_temp",
          "dhalldata",
          "dhpauserules_today",
          "xiaoshou28_maxmin",
          "v_com_product"
          #"dhrules_today_minlimit",
          #"dhrules_today_maxlimit",
          #"product_gl_packetqty"
          ]

qydic = {"product":"product",
         "product_all":"product_all",
         'v_allstock':'allstock',
         'v_com_branch':'branch',
         'alloc':'alloc',
         'pmt':'pmt',
         'v_sale_daily':'v_sale_daily',
         'v_com_product': 'v_com_product'}

dataserver = {"host":"localhost",
              "port":5432,
              "user":"fengmu",
              "pwd": "zj",
              "database":"yq3"}



 
def main():
    conn = psycopg2.connect(host=dataserver["host"], port=dataserver["port"],user=dataserver["user"],password=dataserver["pwd"],database=dataserver["database"])
    cur = conn.cursor(cursor_factory=LoggingCursor)
    doclean = [ cleantable(conn, cur, table) for table in tables]    
    doimport = [importdata(conn, cur, file) for file in yqfiles]
    
    setSplb(conn,cur)
    print " setSplb "+str(time.asctime())
    
    setPacketqty(conn, cur)
    #print " setPacketqty "+str(time.asctime())
    
    setTodayDeliveryMd(conn, cur)
    print " setTodayDeliveryMd "+str(time.asctime())
    
    setTodayMaxMin(conn, cur)
    print " setTodayMaxMin "+str(time.asctime())
    
    setSugvalue(conn, cur)
    print " setSugvalue "+str(time.asctime())
    
    setdhpauserules_today(conn, cur)
    print " setdhpauserules_today "+str(time.asctime())
    
    setDhMaxlimit(conn, cur)
    print " setDhMaxlimit "+str(time.asctime())
    
    setDhMinlimit(conn, cur)
    print " setDhMinlimit "+str(time.asctime())
    
    setXiaoshou(conn, cur)
    print " setXiaoshou "+str(time.asctime())
    
    setTodayPmt(conn, cur)
    print " setTodayPmt "+str(time.asctime())
    

   
    
    
    
    
   
    
    
class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        #logger = logging.getLogger('sql_debug')
        #logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception, exc:
            #logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise
    


def cleantable(conn, cur, table):
    try:
        sqlstr = "TRUNCATE " + table + ";"
        cur.execute(sqlstr)
        conn.commit()
        return "yes"
    except:
        print table
        return "no"
    
    
    
def getcsvfile(file):
    dir = downloaddir
    today=datetime.datetime.now().strftime('%Y-%m-%d')    
    return dir + file + '_' + today + '.csv'
    
def importdata(conn, cur, file):
    table = qydic[file]
    csvfile = getcsvfile(file)
    try:
        sqlstr = "copy " +table +" from '" + csvfile  +"' delimiter as '\t' csv;"
        cur.execute(sqlstr)
        conn.commit()
        return 'yes'
    except:
        return 'no'
    
def setTodayMaxMin(conn, cur):
    """本日有效的上下限,B版本优先"""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    sqlstr = "delete from maxminval;"
    sqlstr = "insert into maxminval"
    sqlstr+=" select braid,proid,maxval,minval from maxmin "
    sqlstr+=" where banben ='A'"
    sqlstr+="    and proid||braid not in("
    sqlstr+="        select proid||braid from maxmin"
    sqlstr+="        where banben ='B'"
    sqlstr+="           and startdate<='"+today+"'"
    sqlstr+="           and '"+today+"'<enddate"
    sqlstr+=" )"
    sqlstr+=" union all"
    sqlstr+=" select braid,proid,maxval,minval from maxmin "
    sqlstr+=" where banben='B'"
    sqlstr+="     and startdate<='"+today+"'"
    sqlstr+="     and '"+today+"'<enddate"
   
    cur.execute(sqlstr)
    conn.commit()
    

    
def setSugvalue(conn, cur):
    """本日补货建议"""
    sqlstr = "delete from sugvalue_temp"
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr="insert into sugvalue_temp"
    sqlstr+=" SELECT  t1.braid, t2.braname,t1.proid, t3.proname,0 AS suggest, 0 AS suggestcost,t1.maxval,t1.minval,0 As curqty,0 As AllocQty"
    sqlstr+=" FROM maxminval t1, branch t2, product t3"   #本日上下限
    sqlstr+=" WHERE t1.braid=t2.braid and t1.proid=t3.proid  "
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr="insert into sugvalue_temp"
    sqlstr+=" SELECT  t1.braid, t2.braname,t1.proid, t3.proname,0 AS suggest, 0 AS suggestcost,0 as maxval,0 as minval ,t1.curqty,0 As AllocQty"
    sqlstr+=" FROM allstock t1, branch t2, product t3"   #库存
    sqlstr+=" WHERE t1.braid=t2.braid and t1.proid=t3.proid  "
    cur.execute(sqlstr)
    conn.commit()
   
           
    sqlstr="insert into sugvalue_temp"
    sqlstr+=" SELECT  t1.braid, t2.braname,t1.proid, t3.proname,0 AS suggest, 0 AS suggestcost,0 as maxval,0 as minval ,0 As curqty,t4.AllocQty As AllocQty"
    sqlstr+=" FROM allstock t1, branch t2, product t3,alloc t4"  #在途
    sqlstr+=" WHERE t1.braid=t2.braid and t1.proid=t3.proid and t1.braid=t4.braid and t1.proid=t4.proid "
    cur.execute(sqlstr)
    conn.commit()
    
    
    sqlstr = "delete from sugvalue"
    cur.execute(sqlstr)
    conn.commit()
    
    
    
    sqlstr="insert into sugvalue "
    sqlstr+=" select braid, braname, proid, proname, sum(suggest) as suggest, sum(suggestcost) as suggestcost, sum(maxval) as maxval, sum(minval) as minval, sum(curqty) as curqty,sum(AllocQty) as AllocQty"
    sqlstr+=" from sugvalue_temp"
    sqlstr+=" group by braid, braname, proid, proname"        
    cur.execute(sqlstr)
    conn.commit()
    
    
    sqlstr =" update sugvalue"
    sqlstr+=" set suggest=maxval-AllocQty "        
    sqlstr+=" where sugvalue.AllocQty < sugvalue.minval "             #负库存作零处理
    sqlstr+=" and sugvalue.maxval > 0 "
    sqlstr+=" and sugvalue.curqty <= 0 "
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr ="update sugvalue"
    sqlstr+=" set suggest=maxval-curqty-AllocQty "        
    sqlstr+=" where (sugvalue.curqty + sugvalue.AllocQty) < sugvalue.minval"             
    sqlstr+=" and sugvalue.maxval > 0"
    sqlstr+=" and sugvalue.curqty > 0"
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr =" update sugvalue "
    sqlstr+=" set suggest=round(suggest/t.packetqty1+0.2)*t.packetqty1"        #按配货单位圆整，２舍３入
    sqlstr+=" from product_gl_packetqty as t"       
    sqlstr+=" where sugvalue.proid= t.proid and t.packetqty1 > 1"
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr =" update sugvalue "
    sqlstr+=" set suggestcost= sugvalue.suggest*t.normalprice"        
    sqlstr+=" from product as t"       
    sqlstr+=" where sugvalue.proid= t.proid "
    cur.execute(sqlstr)
    conn.commit()
    
    
   
    
def setTodayDeliveryMd(conn, cur):
    """本日满足配送规则的有效门店"""
    wd={0:'星期一',1:'星期二',2:'星期三',3:'星期四',4:'星期五',5:'星期六',6:'星期日'}
    w=datetime.datetime.now().weekday()
    sqlt = "delete from deliveryval;"
    sqlstr="insert into deliveryval"
    sqlstr+=" select braid from delivery"
    sqlstr+=" where weekdelivery='"+wd[w]+"'"
    cur.execute(sqlstr)
    conn.commit()
    
    
    
def setMdTotal(conn,cur):
    """有效门店补货综合信息,供查询"""
    sqlstr="insert into brainfo"
    sqlstr+=" select braid,braname,count(distinct(proid)) ,sum(curqty) ,sum(suggest) ,sum(suggestcost)  "
    sqlstr+=" from sugvalue"
    sqlstr+=" where braid in (select braid from deliveryval)"
    sqlstr+=" and suggest>0"
    sqlstr+=" group by braid,braname"
    cur.execute(sqlstr)
    conn.commit()
    
    
    
def setSplb(conn, cur):
    sqlstr =  " delete from splb; "
    sqlstr += " insert into splb "
    sqlstr += " select t1.proid, t1.barcode, t1.proname, t1.prosname, "
    sqlstr += " t2.classid || '_' || t2.classname as spxl, "
    sqlstr += " t3.classid || '_' || t3.classname as spzl, "
    sqlstr += " t4.classid || '_' || t4.classname as spdl  "
    sqlstr += " from product t1, product_class t2, product_class t3, product_class t4 "
    sqlstr += " where t1.classid = t2.id and t2.parentcode = t3.classid and t3.parentcode = t4.classid"
    cur.execute(sqlstr)
    conn.commit()
    
def setSpCategory(conn, cur):
    """商品大中小类"""
    sqlstr = "delete from splb;"
    sqlstr+= "insert into splb "
    sqlstr+= "select t1.proid, t1.barcode, t1.proname, t1.prosname, t2.classid||'_'||t2.classname as spxl, t3.classid||'_'||t3.classname as spzl,  t4.classid||'_'||t4.classname as spdl "
    sqlstr+= " from product t1, product_class t2, product_class t3, product_class t4 "
    sqlstr+= " where t1.classid = t2.id and t2.parentcode = t3.classid and t3.parentcode = t4.classid and t1.status in ('1', '2', '3', '4');"
    cur.execute(sqlstr)
    conn.commit()
    
def setXiaoshou(conn, cur):
    ''' 28天销售 '''
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=28),"%Y-%m-%d")
    sqlstr="delete from xiaoshou28 where saledate<to_date('"+startdate+"', 'YYYY-MM-DD')"
    cur.execute(sqlstr)
    conn.commit()

    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=3),"%Y-%m-%d")
    sqlstr="delete from xiaoshou28 where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr="insert into xiaoshou28 select * from v_sale_daily"    
    cur.execute(sqlstr)
    conn.commit()
    
    #*** 调试用 ××××
    sqlstr = """
                 delete from xiaoshou28 where braid not in ('02058','02186', '02203', '02204','02216','02196', '04340')"""
        
    cur.execute(sqlstr)
    conn.commit()
    #******************

    #第一周
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=7),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_res_temp"
    sqlstr+=" select braid,proid,sum(saleqty) as  week1_qty,sum(saleamt) as  week1_amt,0 as week2_qty,0 as week2_amt,0 as week3_qty,0 as week3_amt,0  as week4_qty,0  as week4_amt,0  as total_qty,0  as total_amt"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')  "
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()

    #第二周
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=14),"%Y-%m-%d")
    enddate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=7),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_res_temp"
    sqlstr+=" select braid,proid,0  as week1_qty,0  as week1_amt,sum(saleqty)  as week2_qty,sum(saleamt)  as week2_amt,0  as week3_qty,0  as week3_amt,0  as week4_qty,0  as week4_amt,0  as total_qty,0  as total_amt"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and saledate<to_date('"+enddate+"', 'YYYY-MM-DD')  "
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()

    #第三周
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=21),"%Y-%m-%d")
    enddate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=14),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_res_temp"
    sqlstr+=" select braid,proid,0  as week1_qty,0  as week1_amt,0  as week2_qty,0  as week2_amt,sum(saleqty)  as week3_qty,sum(saleamt)  as week3_amt,0 as week4_qty,0 as week4_amt,0 as total_qty,0 as total_amt"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and saledate<to_date('"+enddate+"', 'YYYY-MM-DD')  "
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()

    #第四周
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=28),"%Y-%m-%d")
    enddate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=21),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_res_temp"
    sqlstr+=" select braid,proid,0 as week1_qty,0 as week1_amt,0 as week2_qty,0 as week2_amt,0 as week3_qty,0 as week3_amt,sum(saleqty) as week4_qty,sum(saleamt) as week4_amt,0 as total_qty,0 as total_amt"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and saledate<to_date('"+enddate+"', 'YYYY-MM-DD')  "
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()

    #合计
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=28),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_res_temp"
    sqlstr+=" select braid,proid,0 as week1_qty,0 as week1_amt,0 as week2_qty,0 as week2_amt,0 as week3_qty,0 as week3_amt,0 as week4_qty,0 as week4_amt,sum(saleqty) as total_qty,sum(saleamt) as total_amt"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD') "
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()

    #聚集
    sqlstr="insert into xiaoshou28_res"
    sqlstr+=" select braid,proid,sum(week1_qty),sum(week1_amt),sum(week2_qty),sum(week2_amt),sum(week3_qty),sum(week3_amt),sum(week4_qty),sum(week4_amt),sum(total_qty) as total_qty,sum(total_amt) as total_amt"
    sqlstr+=" from xiaoshou28_res_temp"
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()
    

    
def setPacketqty(conn, cur):
    sqlstr = " delete from product_gl_packetqty; "
    sqlstr += " insert into product_gl_packetqty select proid, packetqty1 from product "
    cur.execute(sqlstr)
    conn.commit()
    #--*********************
    
    sqlstr = " update product_gl_packetqty "
    sqlstr += " set packetqty1 = 1 where packetqty1 = 0 or packetqty1 is null "   #x修改配货单位错误的
    cur.execute(sqlstr)
    conn.commit()
    
    
    #--*********大类*************
    sqlstr = " update product_gl_packetqty "
    sqlstr += " set packetqty1 = t.packetqty1 "
    sqlstr += " from (select t1.proid, t2.packetqty1 "
    sqlstr += "         from product_all t1, product_gl_packetqty_rules t2 "
    sqlstr += "         where t1.prodl_id = t2.xcode and t2.excode = 'dl') t "
    sqlstr += " where product_gl_packetqty.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    
    #--*********中类*************
    sqlstr = " update product_gl_packetqty "
    sqlstr += " set packetqty1 = t.packetqty1 "
    sqlstr += " from (select t1.proid, t2.packetqty1 "
    sqlstr += "          from product_all t1, product_gl_packetqty_rules t2 "
    sqlstr += "          where prozl_id = t2.xcode and t2.excode = 'zl') t "
    sqlstr += " where product_gl_packetqty.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    
    #--*********小类*************
    sqlstr = " update product_gl_packetqty "
    sqlstr += " set packetqty1 = t.packetqty1 "
    sqlstr += " from (select t1.proid, t2.packetqty1 "
    sqlstr += "        from product_all t1, product_gl_packetqty_rules t2 "
    sqlstr += "          where proxl_id = t2.xcode and t2.excode = 'xl') t "
    sqlstr += " where product_gl_packetqty.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    
    #--**********单品*************
    sqlstr = " update product_gl_packetqty "
    sqlstr += " set packetqty1 = t.packetqty1 "
    sqlstr += " from (select t1.proid, t2.packetqty1 "
    sqlstr += "       from product_all t1, product_gl_packetqty_rules t2 "
    sqlstr += "         where t1.proid = t2.xcode and t2.excode = 'sp') t "
    sqlstr += " where product_gl_packetqty.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()

def setDhMaxlimit(conn, cur):
    """***********上y阈值************"""
    sqlstr = " delete from dhrules_today_maxlimit; "
    sqlstr += " insert into dhrules_today_maxlimit select braid, proid, suggest from sugvalue "
    cur.execute(sqlstr)
    conn.commit()
    #--**********************
    
    
    #--***********全部***********
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = dhrules.yqrule, yqvalue = dhrules.yqvalue "
    sqlstr += " from dhrules "
    sqlstr += " where dhrules.mdcode ='' and dhrules.xcode ='' and dhrules.excode ='' and dhrules.yqkey = 'maxlimit' "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    #--***********门店***********
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = dhrules.yqrule, yqvalue = dhrules.yqvalue "
    sqlstr += " from dhrules "
    sqlstr += " where dhrules.mdcode = dhrules_today_maxlimit.braid and dhrules.mdcode <>'' and dhrules.xcode ='' and dhrules.excode ='' and dhrules.yqkey = 'maxlimit' "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    #--*********大类*************
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "            from product_all t1, dhrules t2 "
    sqlstr += "              where t1.prodl_id = t2.xcode and t2.excode = 'dl' and t2.mdcode ='' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--**********门店大类************
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.prodl_id = t2.xcode and t2.excode = 'dl' and t2.mdcode <>'' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid and dhrules_today_maxlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    #--**********中类************
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "              where t1.prozl_id = t2.xcode and t2.excode = 'zl' and t2.mdcode ='' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--*********门店中类*************
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.prozl_id = t2.xcode and t2.excode = 'zl' and t2.mdcode <>'' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid and dhrules_today_maxlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    #--**********小类************
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proxl_id = t2.xcode and t2.excode = 'xl' and t2.mdcode ='' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--***********门店小类***********
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proxl_id = t2.xcode and t2.excode = 'xl' and t2.mdcode <>'' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid and dhrules_today_maxlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    #--*************单品*********
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proid = t2.xcode and t2.excode = 'sp' and t2.mdcode ='' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--**************门店单品********
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proid = t2.xcode and t2.excode = 'sp' and t2.mdcode <>'' and t2.yqkey = 'maxlimit') t "
    sqlstr += " where dhrules_today_maxlimit.proid = t.proid and dhrules_today_maxlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqmaxlimit = to_char(suggest + to_number(yqvalue, '999D999S'),'99999999999') "
    sqlstr += " where yqrule = 'jd' "    
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr = " update dhrules_today_maxlimit "
    sqlstr += " set yqmaxlimit = to_char(suggest *(1 + to_number(yqvalue, '999D999S')),'99999999999')"
    sqlstr += " where yqrule = 'xd' "    
    cur.execute(sqlstr)
    conn.commit()
    
    
    
def setDhMinlimit(conn, cur):
    """***********下阈值************"""
    sqlstr = " delete from dhrules_today_minlimit; "
    sqlstr += " insert into dhrules_today_minlimit select braid, proid, suggest from sugvalue "
    cur.execute(sqlstr)
    conn.commit()
    #--**********************
    
    
    #--***********全部***********
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = dhrules.yqrule, yqvalue = dhrules.yqvalue "
    sqlstr += " from dhrules "
    sqlstr += " where dhrules.mdcode ='' and dhrules.xcode ='' and dhrules.excode ='' and dhrules.yqkey = 'minlimit' "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    #--***********门店***********
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = dhrules.yqrule, yqvalue = dhrules.yqvalue "
    sqlstr += " from dhrules "
    sqlstr += " where dhrules.mdcode = dhrules_today_minlimit.braid and dhrules.mdcode <>'' and dhrules.xcode ='' and dhrules.excode ='' and dhrules.yqkey = 'minlimit' "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    #--*********大类*************
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "            from product_all t1, dhrules t2 "
    sqlstr += "              where t1.prodl_id = t2.xcode and t2.excode = 'dl' and t2.mdcode ='' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--**********门店大类************
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.prodl_id = t2.xcode and t2.excode = 'dl' and t2.mdcode <>'' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid and dhrules_today_minlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    #--**********中类************
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "              where t1.prozl_id = t2.xcode and t2.excode = 'zl' and t2.mdcode ='' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--*********门店中类*************
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.prozl_id = t2.xcode and t2.excode = 'zl' and t2.mdcode <>'' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid and dhrules_today_minlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    #--**********小类************
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proxl_id = t2.xcode and t2.excode = 'xl' and t2.mdcode ='' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--***********门店小类***********
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proxl_id = t2.xcode and t2.excode = 'xl' and t2.mdcode <>'' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid and dhrules_today_minlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    #--*************单品*********
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proid = t2.xcode and t2.excode = 'sp' and t2.mdcode ='' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid "
    cur.execute(sqlstr)
    conn.commit()
    #--***************************
    
    
    
    #--**************门店单品********
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqrule = t.yqrule, yqvalue = t.yqvalue "
    sqlstr += " from (select t2.mdcode as braid, t1.proid, t2.yqrule, t2.yqvalue "
    sqlstr += "               from product_all t1, dhrules t2 "
    sqlstr += "               where t1.proid = t2.xcode and t2.excode = 'sp' and t2.mdcode <>'' and t2.yqkey = 'minlimit') t "
    sqlstr += " where dhrules_today_minlimit.proid = t.proid and dhrules_today_minlimit.braid = t.braid "
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqminlimit = to_char(suggest - to_number(yqvalue, '999D999S'),'99999999999') "
    sqlstr += " where yqrule = 'jd' "    
    cur.execute(sqlstr)
    conn.commit()
    
    sqlstr = " update dhrules_today_minlimit "
    sqlstr += " set yqminlimit = to_char(suggest *(1 - to_number(yqvalue, '999D999S')),'99999999999')"
    sqlstr += " where yqrule = 'xd' "    
    cur.execute(sqlstr)
    conn.commit()

def setdhpauserules_today(conn, cur):
    sqlstr = " delete from dhpauserules_today; "
    sqlstr += " insert into dhpauserules_today select braid, proid from sugvalue"
    cur.execute(sqlstr)
    conn.commit()
    
    today = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    sqlstr = "select mdcode, xcode, excode from dhPauserules where startdate<='"+today+"' and enddate>='"+today+"'"
    #print sqlstr
    cur.execute(sqlstr)
    results = cur.fetchall()
    conn.commit()
    for line in results:
        sqlstr = setDelPausedhspSql(line[0], line[1], line[2])
        #print "*************"+sqlstr
        if sqlstr != "":
            cur.execute(sqlstr)
            conn.commit()
    
    
def setDelPausedhspSql(mdcode="", xcode="", excode=""):
    if mdcode=="" and xcode=="" :
        return ""
    if mdcode!= "" and xcode == "":
        return "delete from dhpauserules_today where braid ='"+ mdcode + "'"
    if mdcode == "" and xcode !="" and excode != "":
        if excode == "sp":
            return "delete from dhpauserules_today where proid='" +  xcode + "'"
        if excode == 'xl':
            return "delete from dhpauserules_today where proid in (select proid from product_all where proxl_id='"+xcode+"')"
        if excode == 'zl':
            return "delete from dhpauserules_today where proid in (select proid from product_all where prozl_id='"+xcode+"')"
        if excode == 'dl':
            return "delete from dhpauserules_today where proid in (select proid from product_all where prodl_id='"+xcode+"')"
    if mdcode != "" and xcode !="" and excode != "":
        if excode == "sp":
            return "delete from dhpauserules_today where braid||proid='"+mdcode+xcode+"'"
        if excode == "xl":
            return "delete from dhpauserules_today where braid||proid in (select '"+mdcode+"'||" +"proid from product_all where proxl_id='"+xcode+"')"
        if excode == "zl":
            return "delete from dhpauserules_today where braid||proid in (select '"+mdcode+"'||" +"proid from product_all where prozl_id='"+xcode+"')"
        if excode == "dl":
            return "delete from dhpauserules_today where braid||proid in (select '"+mdcode+"'||" +"proid from product_all where prodl_id='"+xcode+"')"
    return ""

def setTodayPmt(conn, cur):
    #today = datetime.datetime.now().strftime('%Y-%m-%d')
    today = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")  #规则提前一周
    sqlstr = " delete from pmt where enddate < '" + today +"';"
    sqlstr += " delete from pmt where pmtdescription not like '%CU'; "
    sqlstr += " delete from pmt where startdate > '" + today + "'; "  #促销标记
    cur.execute(sqlstr)
    conn.commit()

def setMaxminCuxiaori(conn, cur):
    "每月促销日上下限翻倍处理"
    #--*********商品大类*************
    "把所有A版本中符合条件的翻倍 插入B版本"
    sqlstr=""" insert into maxmin
      select t1.braid,t1.proid,t1.maxval*t3.max_multiple,t1.minval*t3.min_multiple,'B' banben,t3.startdate,t3.enddate,t3.adddate
      from maxmin t1,product_all t2,maxmincuxiaori t3
      where t1.banben='A'
        and t1.proid=t2.proid
        and t3.mdcode=t1.braid
        and t3.excode='prodl'
        and t3.xcode=t2.prodl_id
    """
    cur.execute(sqlstr)
    conn.commit()

    #--*********商品中类*************
    "把所有A版本中符合条件的翻倍 插入B版本"
    sqlstr=""" insert into maxmin
      select t1.braid,t1.proid,t1.maxval*t3.max_multiple,t1.minval*t3.min_multiple,'B' banben,t3.startdate,t3.enddate,t3.adddate
      from maxmin t1,product_all t2,maxmincuxiaori t3
      where t1.banben='A'
        and t1.proid=t2.proid
        and t3.mdcode=t1.braid
        and t3.excode='prozl'
        and t3.xcode=t2.prozl_id
    """
    cur.execute(sqlstr)
    conn.commit()

    #--*********商品小类*************
    "把所有A版本中符合条件的翻倍 插入B版本"
    sqlstr=""" insert into maxmin
      select t1.braid,t1.proid,t1.maxval*t3.max_multiple,t1.minval*t3.min_multiple,'B' banben,t3.startdate,t3.enddate,t3.adddate
      from maxmin t1,product_all t2,maxmincuxiaori t3
      where t1.banben='A'
        and t1.proid=t2.proid
        and t3.mdcode=t1.braid
        and t3.excode='proxl'
        and t3.xcode=t2.proxl_id
    """
    cur.execute(sqlstr)
    conn.commit()

    #--*********品牌小类*************
    "把所有A版本中符合条件的翻倍 插入B版本"
    sqlstr=""" insert into maxmin
      select t1.braid,t1.proid,t1.maxval*t3.max_multiple,t1.minval*t3.min_multiple,'B' banben,t3.startdate,t3.enddate,t3.adddate
      from maxmin t1,product_all t2,maxmincuxiaori t3
      where t1.banben='A'
        and t1.proid=t2.proid
        and t3.mdcode=t1.braid
        and t3.excode='braxl'
        and t3.xcode=t2.braxl_id
    """
    cur.execute(sqlstr)
    conn.commit()

    #--**********单品*************
    "把所有A版本中符合条件的翻倍 插入B版本"
    sqlstr=""" insert into maxmin
      select t1.braid,t1.proid,t1.maxval*t3.max_multiple,t1.minval*t3.min_multiple,'B' banben,t3.startdate,t3.enddate,t3.adddate
      from maxmin t1,product_all t2,maxmincuxiaori t3
      where t1.banben='A'
        and t1.proid=t2.proid
        and t3.mdcode=t1.braid
        and t3.excode='sp'
        and t3.xcode=t1.proid
    """
    cur.execute(sqlstr)
    conn.commit()

if __name__=="__main__":

    main()


