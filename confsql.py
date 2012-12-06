# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: confsql.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-08-09 09:19:25
#      History:
#=============================================================================
'''
import memcache,time,datetime
from mylog import log
import logging
import psycopg2
import psycopg2.extensions
import sqlite3

class Confsql:
    #def __init__(self,mchost="127.0.0.1:11211",sqlstr=""):
    #def __init__(self,mchost="127.0.0.1:11211",sqlstr=""):
    def __init__(self,mchost="127.0.0.1:11211",dbstr="postgres://fengmu:zj@localhost/yq3",sqlstr=""):
        self.mchost=mchost
        self.dbstr=dbstr
        self.mc=memcache.Client([self.mchost],debug=0)        
        self.today=datetime.datetime.now().strftime('%Y-%m-%d')
        self.conn = psycopg2.connect(host='localhost',port=5432,user='fengmu',password='zj',database='yq3')
        self.cur = self.conn.cursor(cursor_factory=LoggingCursor)

    def checkExist(self,sqlstr): #数据库表中是否能查出sqlstr语句
        self.cur.execute(sqlstr)
        result=self.cur.fetchall()
        self.conn.commit()
        if len(result)>0:
            return 1
        else:
            return 0

    def runquery(self,sqlstr):
        self.cur.execute(sqlstr)
        result=self.cur.fetchall()
        self.conn.commit()
        return result

    def runSql(self,sqlstr):
        self.cur.execute(sqlstr)
        self.conn.commit()

    '''
    def maxmin_del(self, proid, braid, banben):
        #dels = self.maxmin.delete(and_(self.maxmin.c.proid==proid, self.maxmin.c.braid==braid, self.maxmin.c.banben == banben))
        self.cur.execute("delete from maxmin where proid=%s and braid=%s and banben=%s;",(proid,braid,banben))
        self.conn.commit()

    def maxmin_insert(self,braid,proid,maxval,minval,banben,startdate,enddate,adddate):
        插入上下限
        self.maxmin_del(proid,braid,banben)
        if startdate=="" or enddate=="": #A版本
            #ins=self.maxmin.insert().values(braid=braid,proid=proid,maxval=int(maxval),minval=int(minval),banben=banben,adddate=adddate)
            self.cur.execute("insert into maxmin (braid,proid,maxval,minval,banben,adddate) values(%s,%s,%s,%s,%s,%s);",(braid,proid,int(maxval),int(minval),banben,adddate))
            self.conn.commit()
        else: #B版本
            #ins=self.maxmin.insert().values(braid=braid,proid=proid,maxval=int(maxval),minval=int(minval),banben=banben,startdate=startdate,enddate=enddate,adddate=adddate)
            self.cur.execute("insert into maxmin (braid,proid,maxval,minval,banben,startdate,enddate,adddate) values(%s,%s,%s,%s,%s,%s,%s,%s);",(braid,proid,int(maxval),int(minval),banben,startdate,enddate,adddate))
            self.conn.commit()
    
    def delivery_del(self, braid):
        #dels = self.delivery.delete(self.delivery.c.braid==braid)
        self.cur.execute("delete from delivery where braid=%s;"),(braid,)
        self.conn.commit()
        
    

    def delivery_insert(self,braid,weekdelivery,adddate):
        插入配送规则
        self.cur.execute("insert into delivery(braid,weekdelivery,adddate) values(%s,%s)",(braid,weekdelivery,adddate))
        self.conn.commit()
    '''

    def getpronamefrommc(self,proid):
        '''从内存中读取商品名称'''
        return self.mc.get(str(proid)+"__proname")

    def getbranamefrommc(self,braid):
        '''从内存中读取门店名称'''
        return self.mc.get(str(braid)+"__braname")

    def insult_kdCabinet(self): #查询货架
        sqlstr="SELECT CabinetNum,CabinetType, CabinetCode,CabinetName,Width,ShelfType,ShelfHeight FROM kdCabinet where flag=0 and CabinetType<>'U'"
        sqlitedb="D:/vcms/data/db/sqlite3/yq2.db"
        sqlite_conn= sqlite3.connect(sqlitedb)
        c=sqlite_conn.cursor()
        result=c.execute(sqlstr)
        c.close
        return result

    def delete_kdCabinet(self,CabinetNum): #删除货架
        sqlstr="update kdCabinet set flag=1 where CabinetNum="+CabinetNum
        log(sqlstr)
        sqlitedb="D:/vcms/data/db/sqlite3/yq2.db"
        sqlite_conn= sqlite3.connect(sqlitedb)
        c=sqlite_conn.cursor()
        c.execute(sqlstr)
        sqlite_conn.commit()
        c.close

    def insult_kdsp(self):
        sqlstr="select spcode,spname,height,width,thickness,barcode from kdsp where sp='201205'"
        sqlitedb="D:/vcms/data/db/sqlite3/yq2.db"
        sqlite_conn= sqlite3.connect(sqlitedb)
        c=sqlite_conn.cursor()
        result=c.execute(sqlstr)
        c.close
        return result 

    def check_dhrules(self,mdcode,xcode,excode,yqkey,yqrule,yqvalue):
        self.cur.execute(sqlstr)        
        result=self.cur.fetchall()
        self.conn.commit()
        if len(result)>0:
            return 1
        else:
            return 0

    def check_product_gl_packetqty_rules(self,xcode,excode,packetqty1):
        sqlstr=""
        self.cur.execute(sqlstr)        
        result=self.cur.fetchall()
        self.conn.commit()
        if len(result)>0:
            return 1
        else:
            return 0

    def update_dhrules(self,mdcode,xcode,excode,yqkey,yqrule,yqvalue):
        sqlstr="delete from dhrules where mdcode='"+mdcode+"' and excode='"+excode+"' and xoode='"+xcode+"'"
        self.cur.execute(sqlstr)
        self.conn.commit()
        sqlstr="insert into dhrules (mdcode,xcode,excode,yqkey,yqrule,yqvalue) values('"+mdcode+"','"+xcode+"','"+excode+"','"+yqkey+"','"+yqrule+"','"+yqvalue+"')"
        self.cur.execute(sqlstr)
        self.conn.commit()
        
    def update_product_gl_packetqty_rules(self,xcode,excode,packetqty1):
        sqlstr="delete from product_gl_packetqty_rules where xcode='"+xcode+"' and excode='" + excode+ "'"
        self.cur.execute(sqlstr)
        self.conn.commit()
        sqlstr="insert into product_gl_packetqty_rules (xcode,excode,packetqty1) values('"+xcode+"','"+excode+"','"+packetqty1+"')"
        self.cur.execute(sqlstr)
        self.conn.commit()

    def insult_product_gl_packetqty_rules(self):
        sqlstr=" select t2.proid, t2.proname, '商品代码' as excode, t1.packetqty1 from product_gl_packetqty_rules t1, product_all t2 where t1.excode='sp' and t1.xcode = t2.proid "
        sqlstr += " union "
        sqlstr += " select t2.proxl_id, t2.proxl, '小类代码' as excode, t1.packetqty1 from product_gl_packetqty_rules t1, product_all t2 where t1.excode='xl' and t1.xcode = t2.proxl "
        sqlstr += " union "
        sqlstr += " select t2.prozl_id, t2.prozl, '中类代码' as excode, t1.packetqty1 from product_gl_packetqty_rules t1, product_all t2 where t1.excode='zl' and t1.xcode = t2.prozl "
        sqlstr += " union "
        sqlstr += " select t2.prodl_id, t2.prodl, '大类代码' as excode, t1.packetqty1 from product_gl_packetqty_rules t1, product_all t2 where t1.excode='dl' and t1.xcode = t2.prodl "

        self.cur.execute(sqlstr)
        result=self.cur.fetchall()
        self.conn.commit()
        return result

    def insult_dhrules(self):
        sqlstr="select * from dhrules"
        self.cur.execute(sqlstr)
        result=self.cur.fetchall()
        self.conn.commit()
        return result

    def check_dhPauserules(self,mdcode,xcode,excode):
        sqlstr="select * from dhPauserules where mdcode='"+mdcode+"' and excode='"+excode+"' and xcode='"+xcode+"'"
        self.cur.execute(sqlstr)
        result=self.cur.fetchall()
        self.conn.commit()
        if len(result)>0:
            return 1
        else:
            return 0

    def update_dhPauserules(self,mdcode,xcode,excode):
        sqlstr="delete from dhPauserules where mdcode='"+mdcode+"' and excode='"+excode+"' and xcode='"+xcode+"'"
        self.cur.execute(sqlstr)
        self.conn.commit()
        sqlstr="insert into dhPauserules (mdcode,xcode,excode) values('"+mdcode+"','"+xcode+"','"+excode+"')"
        self.cur.execute(sqlstr)
        self.conn.commit()
        
    def getAllPauseMdSp(self):
        sqlstr = "select mdcode, xcode, excode from dhPauserules"
        self.cur.execute(sqlstr)
        result=self.cur.fetchall()
        self.conn.commit()
        return result
    
    def deleteAdvMaxMin(self, mdcode, spcode, oldmaxval, oldminval):
        sqlstr = "delete from advmaxmin where mdcode ='" + mdcode + "' and  spcode='" + spcode + "' and oldmaxval=" + oldmaxval + " and oldminval =" + oldminval
        self.cur.execute(sqlstr)
        self.conn.commit()
        
    def insertAdvMaxMin(self, mdcode, spcode, oldmaxval, oldminval, newmaxval, newminval, applyfordate, verifydate, remarks):
        self.deleteAdvMaxMin(mdcode, spcode, oldmaxval, oldminval)
        
        sqlstr  = "insert into advmaxmin values("
        sqlstr += "'" + mdcode + "',"
        sqlstr += "'" + spcode + "',"
        sqlstr += oldmaxval + ","
        sqlstr += oldminval + ","
        sqlstr += newmaxval + ","
        sqlstr += newminval + ","
        sqlstr += "'" + applyfordate + "',"
        sqlstr += "'" + verifydate + "',"
        sqlstr += "'" + remarks + "')"
        
        self.cur.execute(sqlstr)
        self.conn.commit()
        
    def getAllAdvMaxMin(self):
        sqlstr = "select t1.mdcode, t2.braname, t1.spcode, t3.proname, t1.oldmaxval, t1.oldminval, t1.newmaxval, t1.newminval, t1.applyfordate "
        sqlstr += " from advmaxmin as t1, branch as t2, product_all as t3 "
        sqlstr += " where t1.mdcode = t2.braid and t1.spcode = t3.proid "
        sqlstr += " and t1.verifydate=''"
        
        self.cur.execute(sqlstr)
        result=self.cur.fetchall()
        self.conn.commit()
        return result
    
    def maxmin_update(self, braid, proid, oldmax, oldmin, newmax, newmin):
        #s = sqlalchemy.select([self.maxmin.c.braid, self.maxmin.c.proid, self.maxmin.c.maxval, self.maxmin.c.minval, self.maxmin.c.banben], sqlalchemy.and_(self.maxmin.c.braid==braid, self.maxmin.c.proid == proid, self.maxmin.c.maxval==float(oldmax), self.maxmin.c.minval==float(oldmin)))
        adddate=datetime.datetime.now().strftime('%Y-%m-%d')
        
        self.cur.execute("select braid,proid,maxval,minval,banben from maxmin where braid=%s and proid=%s and maxval=%s and minval=%s;",(braid,proid,float(oldmax),float(oldmin)))
        self.conn.commit()
        lines = self.cur.fetchall()
        #log("l"+str(lines))
        if len(lines)>0:
            for line in lines:
                #ups = self.maxmin.update().where(sqlalchemy.and_(self.maxmin.c.braid==line[0], self.maxmin.c.proid == line[1], self.maxmin.c.banben==line[4])).values(maxval = float(newmax), minval=float(newmin))
                self.cur.execute("update maxmin set maxval=%s,minval=%s where braid=%s and proid=%s and banben=%s;",(float(newmax),float(newmin),line[0],line[1],line[4]))
                self.conn.commit()
        else:
            #ins=self.maxmin.insert().values(proid=proid,braid=braid,maxval=float(newmax),minval=float(newmin),banben="A")
            self.cur.execute("insert into maxmin(proid,braid,maxval,minval,banben, adddate) values(%s,%s,%s,%s,%s,%s);",(proid,braid,float(newmax),float(newmin),"A", adddate))
            self.conn.commit()
        

class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        #logger = logging.getLogger('sql_debug')
        #logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception, exc:
            #logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise


if __name__=='__main__':
    con=Confsql()
    s="select braid,proid,allocqty from alloc"
    con.writemc_alloc(s)
