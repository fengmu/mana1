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



settings.configure()              #为使用django的功能需要
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
    
    mdcodes = insult_mdcodes(conn, cur, "delivery")
    setcl(conn, cur, mdcodes )       
        
 

def setcl(conn, cur, mdcodes):
    sqlstr = 'delete from cl'
    cur.execute(sqlstr)
    conn.commit()
    
    for mdcode in mdcodes:
        userid = theFmWebSql.getUserInfo(mdcode)["UserId"]
        spcodes = getallspcode3(userid)        
        insert_cl(conn, cur, mdcode, spcodes)
    

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
    

    
def getallspcode3(userid):
    "为写入yq3"
    allspace_fmunitespace =  theFmWebSql.getAllUniteSpace(userid)
    allspace_fmuspace = theFmWebSql.getAllSpace(userid)
    allspace_fmuspace_T = allspace_fmuspace + allspace_fmunitespace      #有图商品    
    allspace_fmuspace_F = theFmWebSql.getAllSpace(userid, "F")           #无图商品
    
        
    result_T=[]
    result_F=[]
        
    for space in allspace_fmuspace_T:
        SpaceId = space["Id"]
        Version = space["Version"]
        SpaceTitle = space["Title"]
        
        if SpaceId[0] != "U":            
            SpaceData = theFmWebSql.getSpaceData(SpaceId, Version, userid)
        else:
            SpaceData = webUnite.getSpaceData(SpaceId, Version, userid)
            
        newSpaceData = [x + [SpaceId, SpaceTitle, Version, "youtu"]  for x in SpaceData ]       #不去除淘汰商品
        #print str(newSpaceData)
        result_T = result_T + newSpaceData
        
    for space in allspace_fmuspace_F:
        SpaceId = space["Id"]
        Version = space["Version"]
        SpaceTitle = space["Title"]
        
        if SpaceId[0] != "U":            
            SpaceData = theFmWebSql.getSpaceData(SpaceId, Version, userid)
        else:
            SpaceData = webUnite.getSpaceData(SpaceId, Version, userid)
            
        newSpaceData = [x + [SpaceId, SpaceTitle, Version, "wutu"] for x in SpaceData ]       #不去除淘汰商品       
        result_F = result_F + newSpaceData
    
    spcodes_T = [ x[0] for x in result_T]
    spcodes_F = [ x for x in result_F if x[0] not in spcodes_T]
    spcodes = f9(spcodes_F) + f9(result_T)
        
    return spcodes

def insert_cl(conn, cur, mdcode, spcodes):
    
    for x in spcodes:
        #print str(x)
        sqlstr = """insert into cl values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sqlstr, (mdcode, x[0], x[1], x[2], x[3], x[4],x[5], x[6], x[8], x[9], x[10], x[11]))
        conn.commit()


def f8(seq): # Dave Kirby    
    """去重, Order preserving"""    
    seen = set()    
    return [x for x in seq if x not in seen and not seen.add(x)] 
        
def f9(seq): # Dave Kirby    
    """去重, Order preserving"""    
    seen = set()    
    return [x for x in seq if x[0] not in seen and not seen.add(x[0])] 
        
    
#***********************************************************************************************************
def getmdsp_dhamount(md_sp):
    value = mc.get(md_sp)
    bak = """if not value:
        return "0"
    else:
        return value"""
    return value

def deletemdsp_dhamount(md_sp):
    mc.delete(md_sp)

def deletemd_sp(md):
    mc.delete(md)
    
def senddhinfo(request):
    if request.user.is_authenticated():
        #userid = request.POST["userid"]
        #sendto 佳讯
        userid = str(request.user.id)
        spcodes = getallspcode(userid)
        for spcode in spcodes:
            deletemdsp_dhamount(userid+"_"+spcode)
        deletemd_sp(userid)
        return HttpResponse('ok')
        
        
def getallspbyuserid(userid):
    result = []
    allspace_fmunitespace =  theFmWebSql.getAllUniteSpace(userid)
    allspace_fmuspace = theFmWebSql.getAllSpace(userid)
    allspace_fmuspace_F = theFmWebSql.getAllSpace(userid, "F")
    allspace = allspace_fmuspace + allspace_fmunitespace + allspace_fmuspace_F
    #allspace =  allspace_fmuspace_F
    
    for space in allspace:
        SpaceId = space["Id"]
        Version = space["Version"]
        SpaceTitle = space["Title"]
        
        if SpaceId[0] != "U":            
            SpaceData = theFmWebSql.getSpaceData(SpaceId, Version, userid)
        else:
            SpaceData = webUnite.getSpaceData(SpaceId, Version, userid)
            
        
        result = result + SpaceData
    
    return result

def getallSpDhinfo(request):
    Dhinfo = {}
    viewUsername = request.session.get('viewUserCode')
    if request.user.is_authenticated()and request.user.has_perm("auth.can_order_goods") and viewUsername is None:
        userid = request.POST['userid']
        usercode = request.user.username.encode("utf-8")
        allspaceData = getallspbyuserid(userid)
        i = 0
        for line in allspaceData:
            spcode = line[0]
            spname = line[1]
            #logger.debug(str(i))
            #logger.debug(usercode+spcode)
            maxminstock = getmemcache.getmemcache(usercode, spcode, 'maxminval')
            #logger.debug(maxminstock)
            maxstock = maxminstock.split("__")[0]
            minstock = maxminstock.split("__")[1]
            curstock = getmemcache.getmemcache(usercode, spcode,'allstock')
            forecastquantity = str(int(float(getmemcache.getmemcache(usercode, spcode,'sugvalue'))))
            
            bak = """if float(curstock) < float(minstock):
                forecastquantity = str(int(float(maxstock)) - int(float(curstock)))
            else:
                forecastquantity = "0"""""
            
            #info = {}
            info = {"spname":spname, "spcode":spcode, "maxstock":maxstock, "minstock":minstock, "curstock":curstock, "forecastquantity":forecastquantity}
            Dhinfo[spcode]=info
            
            i = i + 1
        
        info = getmemcache.getDelivery(usercode)
        Dhinfo["delivery"] = info
            
        return HttpResponse(json.dumps(Dhinfo))
    else:
        return
    
    

def writemc_dhdata(mc, mdcode, dhdata):
    mc.set(mdcode+"__dhdata", dhdata)
    

def set_dhdata(conn, cur, mdcodes):
    for mdcode in mdcodes:
        #print str(mdcode)
        t = fmWebDh(mdcode)
        gzipt= fmgzip.fmgzip(t.encode('utf-8'))
        #log(t)
        #print len(t)
        #x = t[0:1000000]
        if len(t)>0:        
            writemc_dhdata(mc, mdcode, gzipt)
        else:
            writemc_dhdata(mc, mdcode, "fxfx")
            
def fmWebDh(mdcode):
    result = []   #有图
    result2 = []  #无图
    result3 = []  #物料赠品
    
    usercode = mdcode
    userid = theFmWebSql.getUserInfo(usercode)["UserId"]
    mdname = getmemcache.getMdinfo(usercode, "braname")
    spcodes = getallspcode2(userid)
    totalqty = 0
    for spcode in spcodes['youtu']:
        dhamount = getmdsp_dhamount(usercode+"_"+spcode)
        if dhamount:
            pass
        else:
            dhamount = getmemcache.getmemcache(usercode, spcode,'sugvalue')
            
        
        
        spname = getmemcache.getSpinfo(spcode, "proname")
        spdl = getmemcache.getSpinfo(spcode, "spdl")
        spzl = getmemcache.getSpinfo(spcode, "spzl")
        barcode = getmemcache.getSpinfo(spcode, "barcode")
        prostatus = getmemcache.getSpinfo(spcode, "status")
        propacketqty = getmemcache.getSpinfo(spcode, "packetqty1")
        maxminstock = getmemcache.getmemcache(usercode, spcode, 'maxminval')
        curstock = getmemcache.getmemcache(usercode, spcode,'allstock')
        curalloc = getmemcache.getmemcache(usercode, spcode,'alloc')
        datapic = getmemcache.getmemcache(usercode, spcode,'xiaoshou')
        cuxiao = setcuxiao(usercode, spcode)
        #logger.debug(datapic+"**************")
        datapiclist = datapic.split("__")
        
        saletotal = datapiclist[0]
        saleweek4 = datapiclist[1]
        #logger.debug(datapiclist[1])
        saleweek3 = datapiclist[2]
        saleweek2 = datapiclist[3]
        saleweek1 = datapiclist[4]
        
        
        
        
        if float(dhamount)>0 and prostatus in ("1", "2", "3", "4") :    #过滤停止叫货的商品
        #if float(dhamount)>0 :
            if propacketqty=="1":  #处理配货单位
                totalqty = totalqty + float(dhamount)
                #indhmount = '<input type="text" name="firstname" value="'+dhamount+'">'
                indhamount = dhamount
                indhamount_max = setmaxlimit(dhamount, maxminstock, usercode, spcode)
                indhamount_min = setminlimit(dhamount, maxminstock, usercode, spcode)
                result.append([spdl, spzl, barcode, spcode, spname, dhamount, indhamount, statusconvert(prostatus), propacketqty, maxminstock, curstock, saletotal, indhamount_max, indhamount_min, saleweek1, saleweek2,saleweek3, saleweek4, cuxiao, curalloc])
            else:
                try:
                    x = round(float(dhamount)/float(propacketqty)+0.2,0)*float(propacketqty)   #2舍3入
                    indhamount = '<input type="text" name="firstname" value="'+str(x)+'">'
                    indhamount = str(x)
                    indhamount_max = setmaxlimit(indhamount, maxminstock, usercode, spcode)
                    indhamount_min = setminlimit(indhamount, maxminstock, usercode, spcode)
                except:
                    x = float(dhamount)
                    #indhamount = '<input type="text" name="firstname" value="'+str(x)+'">'
                    indhamount = str(x)
                    indhamount_max = setmaxlimit(indhamount, maxminstock, usercode, spcode)
                    indhamount_min = setminlimit(indhamount, maxminstock, usercode, spcode)
                if x > 0: #配货量大于零
                    totalqty = totalqty + x
                    result.append([spdl, spzl, barcode, spcode, spname, str(x), indhamount, statusconvert(prostatus), propacketqty, maxminstock, curstock, saletotal, indhamount_max, indhamount_min, saleweek1, saleweek2,saleweek3, saleweek4, cuxiao, curalloc])
    
    
    for spcode in spcodes['wutu']:
        dhamount = getmdsp_dhamount(usercode+"_"+spcode)
        if dhamount:
            pass
        else:
            dhamount = getmemcache.getmemcache(usercode, spcode,'sugvalue')
            
        
        
        spname = getmemcache.getSpinfo(spcode, "proname")
        spdl = getmemcache.getSpinfo(spcode, "spdl")
        spzl = getmemcache.getSpinfo(spcode, "spzl")
        barcode = getmemcache.getSpinfo(spcode, "barcode")
        prostatus = getmemcache.getSpinfo(spcode, "status")
        propacketqty = getmemcache.getSpinfo(spcode, "packetqty1")
        maxminstock = getmemcache.getmemcache(usercode, spcode, 'maxminval')
        curstock = getmemcache.getmemcache(usercode, spcode,'allstock')
        curalloc = getmemcache.getmemcache(usercode, spcode,'alloc')
        datapic = getmemcache.getmemcache(usercode, spcode,'xiaoshou')
        cuxiao = setcuxiao(usercode, spcode)
        #logger.debug(datapic+"**************")
        datapiclist = datapic.split("__")
        
        saletotal = datapiclist[0]
        saleweek4 = datapiclist[1]
        #logger.debug(datapiclist[1])
        saleweek3 = datapiclist[2]
        saleweek2 = datapiclist[3]
        saleweek1 = datapiclist[4]
        
        
        
        
        if float(dhamount)>0 and prostatus in ("1", "2", "3", "4")  and saletotal != " " and spdl != '05_物料赠品':    #过滤停止叫货的商品
        #if float(dhamount)>0 :
            if propacketqty=="1":  #处理配货单位
                totalqty = totalqty + float(dhamount)
                #indhmount = '<input type="text" name="firstname" value="'+dhamount+'">'
                indhamount = dhamount
                indhamount_max = setmaxlimit(dhamount, maxminstock, usercode, spcode)
                indhamount_min = setminlimit(dhamount, maxminstock, usercode, spcode)
                result2.append([spdl, spzl, barcode, spcode, spname, dhamount, indhamount, statusconvert(prostatus), propacketqty, maxminstock, curstock, saletotal, indhamount_max, indhamount_min, saleweek1, saleweek2,saleweek3, saleweek4, cuxiao, curalloc])
            else:
                try:
                    x = round(float(dhamount)/float(propacketqty)+0.2,0)*float(propacketqty)   #2舍3入
                    indhamount = '<input type="text" name="firstname" value="'+str(x)+'">'
                    indhamount = str(x)
                    indhamount_max = setmaxlimit(indhamount, maxminstock, usercode, spcode)
                    indhamount_min = setminlimit(indhamount, maxminstock, usercode, spcode)
                except:
                    x = float(dhamount)
                    #indhamount = '<input type="text" name="firstname" value="'+str(x)+'">'
                    indhamount = str(x)
                    indhamount_max = setmaxlimit(indhamount, maxminstock, usercode, spcode)
                    indhamount_min = setminlimit(indhamount, maxminstock, usercode, spcode)
                if x > 0: #配货量大于零
                    totalqty = totalqty + x
                    result2.append([spdl, spzl, barcode, spcode, spname, str(x), indhamount, statusconvert(prostatus), propacketqty, maxminstock, curstock, saletotal, indhamount_max, indhamount_min, saleweek1, saleweek2,saleweek3, saleweek4, cuxiao, curalloc])
    

    
    totalsku = str(len(result)+len(result2))
    
    for spcode in spcodes['wutu']:            #无图商品中的物料赠品
        dhamount = getmdsp_dhamount(usercode+"_"+spcode)
        if dhamount:
            pass
        else:
            dhamount = getmemcache.getmemcache(usercode, spcode,'sugvalue')
            
        
        
        spname = getmemcache.getSpinfo(spcode, "proname")
        spdl = getmemcache.getSpinfo(spcode, "spdl")
        spzl = getmemcache.getSpinfo(spcode, "spzl")
        barcode = getmemcache.getSpinfo(spcode, "barcode")
        prostatus = getmemcache.getSpinfo(spcode, "status")
        propacketqty = getmemcache.getSpinfo(spcode, "packetqty1")
        maxminstock = getmemcache.getmemcache(usercode, spcode, 'maxminval')
        curstock = getmemcache.getmemcache(usercode, spcode,'allstock')
        curalloc = getmemcache.getmemcache(usercode, spcode,'alloc')
        datapic = getmemcache.getmemcache(usercode, spcode,'xiaoshou')
        cuxiao = setcuxiao(usercode, spcode)
        #logger.debug(datapic+"**************")
        datapiclist = datapic.split("__")
        
        saletotal = datapiclist[0]
        saleweek4 = datapiclist[1]
        #logger.debug(datapiclist[1])
        saleweek3 = datapiclist[2]
        saleweek2 = datapiclist[3]
        saleweek1 = datapiclist[4]
        
        
        
        
        if float(dhamount)>0 and prostatus in ("1", "2", "3", "4")  and spdl == '05_物料赠品':    #过滤停止叫货的商品
        #if float(dhamount)>0 :
            if propacketqty=="1":  #处理配货单位
                #totalqty = totalqty + float(dhamount)
                #indhmount = '<input type="text" name="firstname" value="'+dhamount+'">'
                indhamount = dhamount
                indhamount_max = setmaxlimit(dhamount, maxminstock, usercode, spcode)
                indhamount_min = setminlimit(dhamount, maxminstock, usercode, spcode)
                result3.append([spdl, spzl, barcode, spcode, spname, dhamount, indhamount, statusconvert(prostatus), propacketqty, maxminstock, curstock, saletotal, indhamount_max, indhamount_min, saleweek1, saleweek2,saleweek3, saleweek4, cuxiao, curalloc])
            else:
                try:
                    x = round(float(dhamount)/float(propacketqty)+0.2,0)*float(propacketqty)   #2舍3入
                    indhamount = '<input type="text" name="firstname" value="'+str(x)+'">'
                    indhamount = str(x)
                    indhamount_max = setmaxlimit(indhamount, maxminstock, usercode, spcode)
                    indhamount_min = setminlimit(indhamount, maxminstock, usercode, spcode)
                except:
                    x = float(dhamount)
                    #indhamount = '<input type="text" name="firstname" value="'+str(x)+'">'
                    indhamount = str(x)
                    indhamount_max = setmaxlimit(indhamount, maxminstock, usercode, spcode)
                    indhamount_min = setminlimit(indhamount, maxminstock, usercode, spcode)
                if x > 0: #配货量大于零
                    #totalqty = totalqty + x
                    result3.append([spdl, spzl, barcode, spcode, spname, str(x), indhamount, statusconvert(prostatus), propacketqty, maxminstock, curstock, saletotal, indhamount_max, indhamount_min, saleweek1, saleweek2,saleweek3, saleweek4, cuxiao, curalloc])
    
        
        
    fp = open('d:/vcms/lib/py/mana1/templates/mana1/dh.html')
    t = Template(fp.read())
    fp.close()
    
    
    html=t.render(Context({'userid': userid, 'result':result, 'result2':result2, 'result3':result3, 'totalsku':totalsku, 'totalqty':str(totalqty), 'mdname':mdname}))
    return html

        
def setmaxlimit(dhamount, maxminstock, usercode, spcode):
    maxstock = maxminstock.split("__")[0]
    minstock = maxminstock.split("__")[1]
    maxlimit = getmemcache.getmemcache(usercode, spcode,'maxlimit')
    yqrule = maxlimit.split("__")[0]
    yqvalue = maxlimit.split("__")[1]
    if yqrule == 'jd':
        x = int(round(float(dhamount)+float(yqvalue)))
    else:
        x = int(round(float(dhamount)*(1+float(yqvalue))+0.5))
    return str(x)
    
def setminlimit(dhamount, maxminstock, usercode, spcode):
    maxstock = maxminstock.split("__")[0]
    minstock = maxminstock.split("__")[1]
    minlimit = getmemcache.getmemcache(usercode, spcode,'minlimit')
    yqrule = minlimit.split("__")[0]
    yqvalue = minlimit.split("__")[1]
    if yqrule == 'jd':
        x = int(round(float(dhamount)-float(yqvalue)))
    else:
        x = int(round(float(dhamount)*(1-float(yqvalue))))
    if x > 0 :
        return str(x)
    else:
        return "1"
    
def setcuxiao(usercode, spcode):
    x = getmemcache.getmemcache(usercode, spcode, "cuxiao")
    if x == '0':
        return " "
    else:
        return "y"
    
    
        
def getsaledata(mdcode, spcode):
    fmdata = getmemcache.getmemcache(mdcode, spcode,'xiaoshou')
    fmdata1 = fmdata.split("__")
    fmdata2 = ",".join(["1", "2", "3", "4"])
    datapic = '<span class="sparklines">'+fmdata2+'</span>'
    return datapic

def getallspcodebyopen(userid):
    result = []
    spcodestr = mc.get(userid)
    if spcodestr:
        spcodes = spcodestr.split(",")
        spcodes.sort()
    
        thespcode = ""
        for spcode in spcodes:
            if thespcode != spcode:
                thespcode = spcode
                result.append(thespcode)
    
    return result

def getallspcode(userid):
    """不用了"""
    allspace_fmunitespace =  theFmWebSql.getAllUniteSpace(userid)
    allspace_fmuspace = theFmWebSql.getAllSpace(userid)
    allspace_fmuspace_F = theFmWebSql.getAllSpace(userid, "F")           #无图商品
    allspace = allspace_fmuspace + allspace_fmunitespace + allspace_fmuspace_F
        
    result=[]
        
    for space in allspace:
        SpaceId = space["Id"]
        Version = space["Version"]
        SpaceTitle = space["Title"]
        
        if SpaceId[0] != "U":            
            SpaceData = theFmWebSql.getSpaceData(SpaceId, Version, userid)
        else:
            SpaceData = webUnite.getSpaceData(SpaceId, Version, userid)
            
        newSpaceData = [x  for x in SpaceData if int(x[3])>-1]       #去除淘汰商品
        result = result + newSpaceData
    
    spcodes = []    
    for line in result:
        spcodes.append(line[0])
        
    return f8(spcodes)
    
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
    
def getallspcode2(userid):
    "有图无图商品分开"
    allspace_fmunitespace =  theFmWebSql.getAllUniteSpace(userid)
    allspace_fmuspace = theFmWebSql.getAllSpace(userid)
    allspace_fmuspace_T = allspace_fmuspace + allspace_fmunitespace      #有图商品
    
    allspace_fmuspace_F = theFmWebSql.getAllSpace(userid, "F")           #无图商品
    
        
    result_T=[]
    result_F=[]
        
    for space in allspace_fmuspace_T:
        SpaceId = space["Id"]
        Version = space["Version"]
        SpaceTitle = space["Title"]
        
        if SpaceId[0] != "U":            
            SpaceData = theFmWebSql.getSpaceData(SpaceId, Version, userid)
        else:
            SpaceData = webUnite.getSpaceData(SpaceId, Version, userid)
            
        newSpaceData = [x  for x in SpaceData if int(x[3])>-1]       #去除淘汰商品
        result_T = result_T + newSpaceData
        
    for space in allspace_fmuspace_F:
        SpaceId = space["Id"]
        Version = space["Version"]
        SpaceTitle = space["Title"]
        
        if SpaceId[0] != "U":            
            SpaceData = theFmWebSql.getSpaceData(SpaceId, Version, userid)
        else:
            SpaceData = webUnite.getSpaceData(SpaceId, Version, userid)
            
        newSpaceData = [x  for x in SpaceData if int(x[3])>-1]       #去除淘汰商品       
        result_F = result_F + newSpaceData
    
    spcodes_T = [ x[0] for x in result_T]
    spcodes_F = [ x[0] for x in result_F if x[0] not in spcodes_T]
    
        
    return {'youtu':f8(spcodes_T), 'wutu':f8(spcodes_F)}
    


if __name__ == "__main__":
    main()
    
        

    
    


    
    
        
    
    
    



