## -*- coding: utf-8 -*-


import memcache,time,datetime
import psycopg2
import psycopg2.extensions


mchost="127.0.0.1:11211"

dataserver = {"host":"localhost",
              "port":5432,
              "user":"fengmu",
              "pwd": "zj",
              "database":"yq3"}



class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        #logger = logging.getLogger('sql_debug')
        #logger.info(mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception, exc:
            #logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise
        
conn = psycopg2.connect(host=dataserver["host"], port=dataserver["port"],user=dataserver["user"],password=dataserver["pwd"],database=dataserver["database"])
cur = conn.cursor(cursor_factory=LoggingCursor)
mc=memcache.Client([mchost],debug=0)
    
    
def main(mdscopesql):
    
    
    if mdscopesql == "":
        mc.flush_all()
    
    writemc_allstock(conn, cur, mc, mdscopesql)
    writemc_branch(conn, cur, mc, mdscopesql)
    writemc_product(conn, cur, mc, mdscopesql)
    writemc_product_status(conn, cur, mc, mdscopesql)
    writemc_product_packetqty(conn, cur, mc, mdscopesql)
    writemc_product_barcode(conn, cur, mc, mdscopesql)
    writemc_product_spzl(conn, cur, mc, mdscopesql)
    writemc_product_spdl(conn, cur, mc, mdscopesql)
    writemc_maxminval(conn, cur, mc, mdscopesql)
    writemc_sugvalue(conn, cur, mc, mdscopesql)
    writemc_deliveryval(conn, cur, mc, mdscopesql)
    writemc_xiaoshou(conn, cur, mc, mdscopesql)
    writemc_dhrules_maxlimit(conn, cur, mc, mdscopesql)
    writemc_dhrules_minlimit(conn, cur, mc, mdscopesql)
    writemc_alloc(conn, cur, mc, mdscopesql)
    writemc_pmt(conn, cur, mc, mdscopesql)

def writemc_allstock(conn, cur, mc, mdscopesql):
    """库存表写内存"""    
    if mdscopesql == "":
        sqlstr = "select braid,proid,curqty from allstock"
    else:
        sqlstr = "select braid,proid,curqty from allstock where braid in (" + mdscopesql + ")"    
    cur.execute(sqlstr)
    for rs in cur.fetchall():       
        mc.set(str(rs[0])+"__"+str(rs[1])+"__allstock",int(float(rs[2])))
        
def writemc_branch(conn, cur, mc, mdscopesql):
    '''门店名称写内存'''
    if mdscopesql == "":
        sqlstr = "select braid,braname from branch"
    else:
        sqlstr = "select braid,braname from branch where braid in (" +mdscopesql+")" 
    cur.execute(sqlstr)
    for rs in cur.fetchall():
        #mc.set(str(rs["braid"])+"__braname",rs["braname"].encode("utf-8"))
        mc.set(str(rs[0])+"__braname",str(rs[1]))

def writemc_product(conn, cur, mc, mdscopesql):
    '''商品名称写内存'''
    
    sqlstr = "select proid,proname from product"      
    cur.execute(sqlstr)
    for rs in cur.fetchall():        
        mc.set(str(rs[0])+"__proname",str(rs[1]))
        
def writemc_product_status(conn, cur, mc, mdscopesql):
    """商品状态"""
    sqlstr = "select proid, status from product"
    cur.execute(sqlstr)
    for rs in cur.fetchall(): 
        mc.set(str(rs[0])+"__status",str(rs[1]))
        #print self.mc.get(str(rs[0])+"__proname")
    
        
def writemc_product_packetqty(conn, cur, mc, mdscopesql):
    """商品配货包装单位"""
               
    sqlstr = "select proid, packetqty1 from product_gl_packetqty"   #供应链管理
    cur.execute(sqlstr)
    for rs in cur.fetchall(): 
        mc.set(str(rs[0])+"__packetqty1",str(int(float(rs[1]))))
    
        
def writemc_product_barcode(conn, cur, mc, mdscopesql):
    '''条形码'''
    sqlstr = "select proid, barcode from splb"
    cur.execute(sqlstr)
    for rs in cur.fetchall():        
        mc.set(str(rs[0])+"__barcode",str(rs[1]))

def writemc_product_spzl(conn, cur, mc, mdscopesql):
    '''商品中类'''
    sqlstr = "select proid, spzl from splb"
    cur.execute(sqlstr)
    for rs in cur.fetchall():        
        mc.set(str(rs[0])+"__spzl",str(rs[1]))
        
def writemc_product_spdl(conn, cur, mc, mdscopesql):
    '''商品大类'''
    sqlstr = "select proid, spdl from splb"
    cur.execute(sqlstr)
    for rs in cur.fetchall():        
        mc.set(str(rs[0])+"__spdl",str(rs[1]))
    

def writemc_maxminval(conn, cur, mc, mdscopesql):
    '''上下限写内存'''
    if mdscopesql == "":
        sqlstr = "select braid,proid,maxval,minval from maxminval"
    else:
        sqlstr = "select braid,proid,maxval,minval from maxminval where braid in(" +mdscopesql+")"  
    cur.execute(sqlstr)
    for rs in cur.fetchall():        
        mc.set(str(rs[0])+"__"+str(rs[1])+"__maxminval",str(rs[2])+"__"+str(rs[3]))

def writemc_sugvalue(conn, cur, mc, mdscopesql):
    '''建议值写内存'''
    if mdscopesql == "":
        sqlstr = "select braid,proid,suggest from sugvalue"
    else:
        sqlstr = "select braid,proid,suggest from sugvalue where braid in (" +mdscopesql+")"
        print sqlstr
    cur.execute(sqlstr)
    for rs in cur.fetchall():
        #mc.set(str(rs["braid"])+"__"+str(rs["proid"])+"__sugvalue",str(rs["suggest"])+"__"+str(rs["suggestcost"]))
        mc.set(str(rs[0])+"__"+str(rs[1])+"__sugvalue",str(int(float(rs[2]))))

def writemc_deliveryval(conn, cur, mc, mdscopesql):
    '''本日配货门店写内存'''
    if mdscopesql == "":
        sqlstr = "select braid from delivery"
    else:
        sqlstr = "select braid from delivery where braid in (" +mdscopesql+")"   
    cur.execute(sqlstr)
    for rs in cur.fetchall():
        #mc.set(str(rs["braid"])+"__delivery","1")
        mc.set(str(rs[0])+"__delivery","1")

def writemc_xiaoshou(conn, cur, mc, mdscopesql):
    '''销售数据写内存'''
    if mdscopesql == "":
        sqlstr = "select braid, proid,total_qty, week4_qty, week3_qty, week2_qty, week1_qty from xiaoshou28_res"
    else:
        sqlstr = "select braid, proid,total_qty, week4_qty, week3_qty, week2_qty, week1_qty from xiaoshou28_res where braid in (" + mdscopesql + ")"    
    cur.execute(sqlstr)
    for rs in cur.fetchall():        
        #mc.set(str(rs[0])+"__"+str(rs[1])+"__xiaoshou",str(int(float(rs[2])))+"  ("+str(int(float(rs[3])))+", "+str(int(float(rs[4])))+", "+str(int(float(rs[5])))+", "+str(int(float(rs[6])))+")")
        mc.set(str(rs[0])+"__"+str(rs[1])+"__xiaoshou",str(int(float(rs[2])))+"__"+str(int(float(rs[3])))+"__"+str(int(float(rs[4])))+"__"+str(int(float(rs[5])))+"__"+str(int(float(rs[6]))))

def writemc_alloc(conn, cur, mc, mdscopesql):
    '''在途'''
    if mdscopesql == "":
        sqlstr = "select braid,proid,allocqty from alloc"
    else:
        sqlstr = "select braid,proid,allocqty from alloc where braid in(" +mdscopesql+")"
    cur.execute(sqlstr)
    for rs in cur.fetchall():        
        mc.set(str(rs[0])+"__"+str(rs[1])+"__alloc",str(rs[2]))
        

def writemc_pmt(conn, cur, mc, mdscopesql):
    '''促销数据写内存'''
    if mdscopesql == "":
        sqlstr = "select braid,proid,startdate,enddate from pmt"
    else:
        sqlstr = "select braid,proid,startdate,enddate from pmt where braid in(" +mdscopesql+")"   
    cur.execute(sqlstr)
    for rs in cur.fetchall():
        #mc.set(str(rs["braid"])+"__"+str(rs["proid"])+"__cuxiao",str(rs["startdate"])+"__"+str(rs["enddate"]))
        mc.set(str(rs[0])+"__"+str(rs[1])+"__cuxiao",str(rs[2])+"__"+str(rs[3]))
        
def writemc_dhrules_maxlimit(conn, cur, mc, mdscopesql):
    '''上阈值规则'''
    if mdscopesql == "":
        sqlstr = "select braid,proid,yqrule,yqvalue from dhrules_today_maxlimit"
    else:
        sqlstr = "select braid,proid,yqrule,yqvalue from dhrules_today_maxlimit where braid in(" +mdscopesql+")"   
    cur.execute(sqlstr)
    for rs in cur.fetchall():
        #mc.set(str(rs["braid"])+"__"+str(rs["proid"])+"__cuxiao",str(rs["startdate"])+"__"+str(rs["enddate"]))
        mc.set(str(rs[0])+"__"+str(rs[1])+"__maxlimit",str(rs[2])+"__"+str(rs[3]))
        
def writemc_dhrules_minlimit(conn, cur, mc, mdscopesql):
    '''下阈值规则'''
    if mdscopesql == "":
        sqlstr = "select braid,proid,yqrule,yqvalue from dhrules_today_minlimit"
    else:
        sqlstr = "select braid,proid,yqrule,yqvalue from dhrules_today_minlimit where braid in(" +mdscopesql+")"   
    cur.execute(sqlstr)
    for rs in cur.fetchall():
        #mc.set(str(rs["braid"])+"__"+str(rs["proid"])+"__cuxiao",str(rs["startdate"])+"__"+str(rs["enddate"]))
        mc.set(str(rs[0])+"__"+str(rs[1])+"__minlimit",str(rs[2])+"__"+str(rs[3]))
        


if __name__=="__main__":
    main("select braid from branch where braid = '02058'")
    #main("")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            