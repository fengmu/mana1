# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: processdh.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-11-02 10:14:50
#      History:
#=============================================================================
'''
import confsql
import psycopg2
import psycopg2.extensions
import functions

dataserver = {"host":"localhost",
              "port":5432,
              "user":"fengmu",
              "pwd": "zj",
              "database":"yq3"}
logfile="D:/vcms/lib/py/mana1/mylog.log"

def main():
    conn = psycopg2.connect(host=dataserver["host"], port=dataserver["port"],user=dataserver["user"],password=dataserver["pwd"],database=dataserver["database"])
    cur = conn.cursor()

    init(conn,cur)

    sugvalue_moban(conn,cur)

    xiaoshou28_moban(conn,cur)

    cl_moban(conn,cur)

    dhalldata_insert(conn,cur)

    dhalldata_update(conn,cur)

    sp(conn,cur)
    
    mdsp(conn, cur)

    packetqty1(conn,cur)

    yqmaxlimit(conn,cur)

    yqminlimit(conn,cur)

    delivery(conn,cur)

    dhtag(conn,cur)

    cuxiao(conn,cur)

    sugvalue(conn,cur)

    xiaoshou28_res(conn,cur)

    cl(conn,cur)




def init(conn, cur):
    try:
        sqlstr  = " delete from dhalldata_temp; "
        sqlstr += " delete from dhalldata "
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("�������,׼�����ݼӹ�")


def sugvalue_moban(conn,cur):
    #1. ����md,sp
    try:
        sqlstr="""
            insert into dhalldata_temp
            select braid, proid
            from  sugvalue
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("�����ŵ������Ʒ����sugvalue_mobanʧ�ܣ�",logfile)

def xiaoshou28_moban(conn,cur):
    #2. xiaoshou28
    try:
        sqlstr="""
            insert into dhalldata_temp
            select braid, proid
            from xiaoshou28_res
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("�����ŵ������Ʒ����xiaoshou_mobanʧ�ܣ�",logfile)

def cl_moban(conn,cur):
    #3 cl
    try:
        sqlstr="""
            insert into dhalldata_temp
            select mdcode, spcode
            from cl
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("�����ŵ������Ʒ����cl_mobanʧ�ܣ�",logfile)

def dhalldata_insert(conn,cur):
    #4
    try:
        sqlstr="""
            insert into dhalldata
            select mdcode, spcode from dhalldata_temp group by mdcode, spcode
        """
        cur.execute(sqlstr)
        conn.commit()
        
        #*** ������ ��������
        sqlstr = """
                 delete from dhalldata where mdcode not in ('02058','02186', '02203', '02204','02216','02196', '04340')"""
        
        cur.execute(sqlstr)
        conn.commit()
        #*****************
        
    except:
        functions.log("��dhalldata��������ʧ�ܣ�",logfile)


def dhalldata_update(conn,cur):
    #5. mdcode
    try:
        sqlstr="""
            update dhalldata
            set mdname = t.braname
            from branch as t
            where mdcode = t.braid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("��dhalldata��������ʧ�ܣ�",logfile)

def sp(conn,cur):
    #6 sp
    try:
        sqlstr="""
            update dhalldata
            set spname = t.proname,
                proxl_id = t.proxl_id,
                proxl    = t.proxl,
                prozl_id = t.prozl_id,
                prozl    = t.prozl,
                prodl_id = t.prodl_id,
                prodl    = t.prodl,
                braxl_id = t.braxl_id,
                braxl    = t.braxl,
                brazl_id = t.brazl_id,
                brazl    = t.brazl,
                bradl_id = t.bradl_id,
                bradl    = t.bradl,
                normalprice = t.normalprice,
                status   = t.status,
                barcode  = t.barcode,
                packetqty1 = t.packetqty1
            from product_all as t
            where spcode = t.proid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("sp��������ʧ�ܣ�",logfile)
        
def mdsp(conn, cur):
    #6.1 mdsp
    try:
        sqlstr = """
            update dhalldata
            set status = t.status
            from v_com_product as t
            where spcode = t.proid and mdcode = t.braid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("mdsp��������ʧ��")

def packetqty1(conn,cur):
    #7.packetqty1
    try:
        sqlstr="""
            update dhalldata
            set packetqty1 = t.packetqty1
            from product_gl_packetqty as t
            where spcode = t.proid 
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("packetqty1��������ʧ�ܣ�",logfile)


def yqmaxlimit(conn,cur):
    #8. yqmaxlimit
    try:
        sqlstr="""
            update dhalldata
            set yqmaxlimit = t.yqmaxlimit
            from dhrules_today_maxlimit as t
            where spcode = t.proid and mdcode = t.braid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("yqmaxlimit��������ʧ�ܣ�",logfile)


def yqminlimit(conn,cur):
    #9.yqminlimit
    try:
        sqlstr="""
            update dhalldata
            set yqminlimit = t.yqminlimit
            from dhrules_today_minlimit as t
            where spcode = t.proid and mdcode = t.braid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("yqminlimit��������ʧ�ܣ�",logfile)


def delivery(conn,cur):
    #9.1 delivery
    try:
        sqlstr="""
            update dhalldata
            set delivery = 'T'
            from delivery as t
            where mdcode = t.braid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("delivery��������ʧ�ܣ�",logfile)


def dhtag(conn,cur):
    #9.2 dhtag
    try:
        sqlstr="""
            update dhalldata
            set dhtag = 'T'
            from dhpauserules_today as t
            where mdcode = t.braid and spcode = t.proid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("dhtag��������ʧ�ܣ�",logfile)


def cuxiao(conn,cur):
    #9.3 cuxiao
    try:
        sqlstr="""
            update dhalldata
            set cuxiao_1 = 'T'
            from pmt as t
            where mdcode = t.braid and spcode = t.proid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("cuxiao��������ʧ�ܣ�",logfile)


def sugvalue(conn,cur):
    #10. sugvalue
    try:
        sqlstr="""
            update dhalldata
            set suggest     = t.suggest,
            suggestcost = t.suggestcost,
            maxval      = t.maxval,
            minval      = t.minval,
            curqty      = t.curqty,
            allocqty    = t.allocqty
            from sugvalue as t
            where mdcode = t.braid and spcode = t.proid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("sugvalue��������ʧ�ܣ�",logfile)


def xiaoshou28_res(conn,cur):
    #11. xiaoshou28_res
    try:
        sqlstr="""
            update dhalldata
            set week1_qty = t.week1_qty,
            week2_qty = t.week2_qty,
            week3_qty = t.week3_qty,
            week4_qty = t.week4_qty,
            total_qty = t.total_qty,
            week1_amt = t.week1_amt,
            week2_amt = t.week2_amt,
            week3_amt = t.week3_amt,
            week4_amt = t.week4_amt,
            total_amt = t.total_amt
            from  xiaoshou28_res as t
            where  mdcode = t.braid and spcode = t.proid
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("xiaoshou28_res��������ʧ�ܣ�",logfile)


def cl(conn,cur):
    #12. cl
    try:
        sqlstr="""
            update dhalldata
            set  assortment = t.assortment,
            spaceid    = t.spaceid,
            spacename  = t.spacename,
            hjcode     = t.hjcode,
            shelf      = t.shelf,
            drawer     = t.drawer,
            box        = t.box
            from  cl as t
            where dhalldata.mdcode = t.mdcode and dhalldata.spcode = t.spcode
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        functions.log("cl��������ʧ�ܣ�",logfile)
        
        
        
        
        
def setMdTotal(conn,cur):
    """��Ч�ŵ겹���ۺ���Ϣ,����ѯ"""
    sqlstr  = " delete from brainfo "
    sqlstr  = " insert into brainfo "
    sqlstr += " select braid,braname,count(distinct(proid)) ,sum(curqty) ,sum(suggest) ,sum(suggestcost)  "
    sqlstr += " from dhalldata"
    sqlstr += " where deliveryval = 'T' and dhtag = 'T' "
    sqlstr += " and assortment is not null and status < '5' and suggest > 0 and shelf > '-1' "
    sqlstr += " group by braid,braname"
    cur.execute(sqlstr)
    conn.commit()
    
if __name__ == "__main__":
    main()


