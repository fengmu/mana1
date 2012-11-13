# -*- coding: utf-8 -*-



from django.conf import settings 
from django.template import Context, Template

import simplejson as json

import psycopg2
import psycopg2.extensions
import memcache

import cm.pc.webUnite as webUnite, cm.pc.getmemcache as getmemcache
from cm.fmsettings import *
from  mylog import log
import fmgzip



#
mchost="127.0.0.1:11211"
dataserver = {"host":"localhost",
              "port":5432,
              "user":"fengmu",
              "pwd": "zj",
              "database":"yq3"}


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        #logger = logging.getLogger('sql_debug')
        #logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception, exc:
            #logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise


def main():
    mc=memcache.Client([mchost],debug=0)
    conn = psycopg2.connect(host=dataserver["host"], port=dataserver["port"],user=dataserver["user"],password=dataserver["pwd"],database=dataserver["database"])
    cur = conn.cursor(cursor_factory=LoggingCursor)
    
   
    
    mdcodes = insult_mdcodes(conn, cur, "deliveryval")
    set_dhdata(conn, cur, mdcodes)
    
    mdcodes = insult_mdcodes(conn, cur, "deliveryval")
    set_allSpDhinfo(conn, cur, mdcodes)
    
            
        
        
def insult_mdcodes(conn, cur, tag):
    if tag=='delivery':
        sqlstr = "select braid from delivery group by braid"
    if tag=='deliveryval':
        sqlstr = "select braid from deliveryval group by braid"
        
    cur.execute(sqlstr)
    result=cur.fetchall()
    conn.commit()
    mdcodes = [x[0] for x in result]
    return mdcodes    
    

        
def writemc_dhdata(mc, mdcode, dhdata):
    mc.set(mdcode+"__dhdata", dhdata)
    

    

def set_dhdata(conn, cur, mdcodes):
    for mdcode in mdcodes:
        #print str(mdcode)
        t = fmWebDh(conn, cur, mdcode)
        gzipt= fmgzip.fmgzip(t.encode('utf-8'))
        #log(t)
        #print len(t)
        #x = t[0:1000000]
        if len(t)>0:        
            writemc_dhdata(mc, mdcode, gzipt)
        else:
            writemc_dhdata(mc, mdcode, "fxfx")
    
        


    



def fmWebDh(conn, cur, mdcode):
    """spdl, spzl, barcode, spcode, spname, dhamount, indhamount, statusconvert(prostatus), propacketqty, maxminstock, curstock, saletotal, indhamount_max, indhamount_min, saleweek1, saleweek2,saleweek3, saleweek4, cuxiao, curalloc]"""
    
    usercode = mdcode
    userid = theFmWebSql.getUserInfo(usercode)["UserId"]
    
    
    sqlstr = "select mdcode, mdname, prodl_id, prodl, prozl_id, prozl, spcode, spname, suggest, suggest, status, packetqty1, maxval, minval, curqty, total_qty, yqmaxlimit, yqminlimit, week1_qty, week2_qty, week3_qty, week4_qty, cuxiao_1, allocqty, normalprice, assortment, barcode from dhalldata where assortment is not null and status < '5' and suggest > 0 and shelf > '-1' and dhtag='T' and mdcode='"+mdcode+"'"    
    cur.execute(sqlstr)
    result=cur.fetchall()
    conn.commit()
    
    result1 = [ x for x in result if x[25] == 'youtu']
    result2 = [ x for x in result if x[25] == 'wutu' and x[2] != '05']
    result3 = [ x for x in result if x[25] == 'wutu' and x[2] == '05']
    
    mdname =  result1[0][1]
    
    result1_a = [ [x[2]+'_'+x[3], x[4]+'_'+x[5], x[26], x[6], x[7], str(convert(x[8])), str(convert(x[9])), statusconvert(x[10]), str(convert(x[11])),str(convert(x[12]))+'__'+str(convert(x[13])), str(convert(x[14])), str(convert(x[15])), x[16].strip(), x[17].strip(), str(convert(x[18])), str(convert(x[19])), str(convert(x[20])), str(convert(x[21])), x[22], str(convert(x[23]))] for x in result1]
    
    result2_a = [ [x[2]+'_'+x[3], x[4]+'_'+x[5], x[26], x[6], x[7], str(convert(x[8])), str(convert(x[9])), statusconvert(x[10]), str(convert(x[11])),str(convert(x[12]))+'__'+str(convert(x[13])), str(convert(x[14])), str(convert(x[15])), x[16].strip(), x[17].strip(), str(convert(x[18])), str(convert(x[19])), str(convert(x[20])), str(convert(x[21])), x[22], str(convert(x[23]))] for x in result2]
    
    result3_a =[ [x[2]+'_'+x[3], x[4]+'_'+x[5], x[26], x[6], x[7], str(convert(x[8])), str(convert(x[9])), statusconvert(x[10]), str(convert(x[11])),str(convert(x[12]))+'__'+str(convert(x[13])), str(convert(x[14])), str(convert(x[15])), x[16].strip(), x[17].strip(), str(convert(x[18])), str(convert(x[19])), str(convert(x[20])), str(convert(x[21])), x[22], str(convert(x[23]))] for x in result3]
    
    result12 = result1+ result2
    suggestlist = [x[8] for x in result12]
    
    totalsku = len(result1_a + result2_a)
    totalqty = reduce(lambda x, y: x+y, suggestlist)
    
    
    fp = open('d:/vcms/lib/py/mana1/templates/mana1/dh.html')
    t = Template(fp.read())
    fp.close()
    
    
    html=t.render(Context({'userid': userid, 'result':result1_a, 'result2':result2_a, 'result3':result3_a, 'totalsku':totalsku, 'totalqty':str(totalqty), 'mdname':mdname}))
    return html

def convert(x):
    try:
        return int(x)
    except:
        return ''



def setcuxiao(usercode, spcode):
    x = getmemcache.getmemcache(usercode, spcode, "cuxiao")
    if x == '0':
        return " "
    else:
        return "y"
    

def statusconvert(status):
    if status == "1":
        return "1-新品"
    elif status == "2":
        return "2-正常"
    elif status == "3":
        return "3-季节性禁止采购"
    elif status == "4":
        return "4-停止采购"
    elif status == "5":
        return "5-停止要货"
    elif status == "8":
        return "8-停止销售"
    elif status == "9":
        return "9-完全停用"
    else:
        return "其他"



def writemc_spdhinfodata(mc, mdcode, spdhinfo):
    mc.set(mdcode+"__spdhinfo", spdhinfo)


def set_allSpDhinfo(conn, cur, mdcodes):
    for mdcode in mdcodes:
        t = fmWebAllsp(conn, cur, mdcode)
        if len(t)>0:
            jsont = json.dumps(t)
            writemc_spdhinfodata(mc, mdcode, jsont)
        else:
            print "xx"
            
def fmWebAllsp(conn, cur, mdcode):
    usercode = mdcode
    userid = theFmWebSql.getUserInfo(usercode)["UserId"]
    
    sqlstr = "select mdcode, mdname, prodl_id, prodl, prozl_id, prozl, spcode, spname, suggest, suggest, status, packetqty1, maxval, minval, curqty, total_qty, yqmaxlimit, yqminlimit, week1_qty, week2_qty, week3_qty, week4_qty, cuxiao_1, allocqty, normalprice, assortment, barcode from dhalldata where assortment is not null  and shelf > '-' and mdcode='"+mdcode+"'"    
    cur.execute(sqlstr)
    result=cur.fetchall()
    conn.commit()
    
    Dhinfo = {'delivery':'今天不是订货日', 'spcode':''}
    
    if len(result)>0:    
        for x in result:
            spcode = x[6]
            info = {"spname":x[7], "spcode":x[6], "maxstock":convert(x[12]), "minstock":convert(x[13]), "curstock":str(convert(x[14])), "forecastquantity":str(convert(x[8]))}
            Dhinfo[spcode]=info
        
        Dhinfo["delivery"]='今天是订货日'
    
    return Dhinfo
        
    
    

if __name__ == "__main__":
    settings.configure()
    main()
    
        

    
    


    
    
        
    
    
    



