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
logfile="D:/vcms/lib/py/mana1/processdh.py"

def main():
    conn = psycopg2.connect(host=dataserver["host"], port=dataserver["port"],user=dataserver["user"],password=dataserver["pwd"],database=dataserver["database"])
    cur = conn.cursor()

    setMdTotal(conn, cur)





        
        
        
        
def setMdTotal(conn,cur):
    """有效门店补货综合信息,供查询"""
    sqlstr  = " delete from brainfo "
    sqlstr  = " insert into brainfo "
    sqlstr += " select mdcode, mdname ,count(spcode) ,sum(curqty) ,sum(suggest) ,sum(suggestcost)  "
    sqlstr += " from dhalldata"
    sqlstr += " where delivery = 'T' and dhtag = 'T' "
    sqlstr += " and assortment is not null and status < '5' and suggest > 0 and shelf > '-1' "
    sqlstr += " and total_qty > 0"
    sqlstr += " group by mdcode, mdname"
    cur.execute(sqlstr)
    conn.commit()


if __name__=="__main__":
    
    main()

