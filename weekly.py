# -*- coding: utf-8 -*-
import datetime
import psycopg2
import psycopg2.extensions
import logging

dataserver = {"host":"localhost",
              "port":5432,
              "user":"fengmu",
              "pwd": "zj",
              "database":"yq3"
              }
conn = psycopg2.connect(host=dataserver["host"], port=dataserver["port"],user=dataserver["user"],password=dataserver["pwd"],database=dataserver["database"])

class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        logger = logging.getLogger('')
        logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception, exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

def log(request):
    logging.basicConfig(filename='./mylog.log',level=logging.INFO)
    logging.info(request)

cur = conn.cursor(cursor_factory=LoggingCursor)

''' 28天销售 '''
'删除28天前的'
print "28"
try:
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=28),"%Y-%m-%d")
    sqlstr="delete from xiaoshou28 where saledate<to_date('"+startdate+"', 'YYYY-MM-DD')"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("删除28天销售失败！")


print "3"
'删除倒推3天的'
try:
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=3),"%Y-%m-%d")
    sqlstr="delete from xiaoshou28 where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("删除倒推3天的数据失败！")

print "insert"
'插入新3天数据'
try:
    sqlstr="insert into xiaoshou28 select * from v_sale_daily"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("插入新3天的数据失败！")

print "truncate temp"
'清空xiaoshou28_maxmin_temp'
try:
    sqlstr="truncate table xiaoshou28_maxmin_temp"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("清空xiaoshou28_maxmin_temp失败！")

print "truncate"
'清空xiaoshou28_maxmin'
try:
    sqlstr="truncate table xiaoshou28_maxmin"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("清空xiaoshou28_maxmin失败！")

print "yi"
#第一周
try:
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=7),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_maxmin_temp"
    sqlstr+=" select braid,proid,sum(saleqty) week1_qty,sum(saleamt) week1_amt,0 week2_qty,0 week2_amt,0 week3_qty,0 week3_amt,0 week4_qty,0 week4_amt,0 total_qty,0 total_amt,'' prodl,'' prozl,'' proxl,'' bradl,'' brazl,'' braxl,0 price,'' status,0 basedisplay,0 maxval,0 minval"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and braid='02058'"
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("插入第一周数据失败！")

print "er"
#第二周
try:
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=14),"%Y-%m-%d")
    enddate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=7),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_maxmin_temp"
    sqlstr+=" select braid,proid,0 week1_qty,0 week1_amt,sum(saleqty) week2_qty,sum(saleamt) week2_amt,0 week3_qty,0 week3_amt,0 week4_qty,0 week4_amt,0 total_qty,0 total_amt,'' prodl,'' prozl,'' proxl,'' bradl,'' brazl,'' braxl,0 price,'' status,0 basedisplay,0 maxval,0 minval"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and saledate<to_date('"+enddate+"', 'YYYY-MM-DD')"
    sqlstr+=" and braid='02058'"
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("插入第二周数据失败！")

print "san"
#第三周
try:
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=21),"%Y-%m-%d")
    enddate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=14),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_maxmin_temp"
    sqlstr+=" select braid,proid,0 week1_qty,0 week1_amt,0 week2_qty,0 week2_amt,sum(saleqty) week3_qty,sum(saleamt) week3_amt,0 week4_qty,0 week4_amt,0 total_qty,0 total_amt,'' prodl,'' prozl,'' proxl,'' bradl,'' brazl,'' braxl,0 price,'' status,0 basedisplay,0 maxval,0 minval"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and saledate<to_date('"+enddate+"', 'YYYY-MM-DD')"
    sqlstr+=" and braid='02058'"
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("插入第三周数据失败！")

print "si"
#第四周
try:
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=28),"%Y-%m-%d")
    enddate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=21),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_maxmin_temp"
    sqlstr+=" select braid,proid,0 week1_qty,0 week1_amt,0 week2_qty,0 week2_amt,0 week3_qty,0 week3_amt,sum(saleqty) week4_qty,sum(saleamt) week4_amt,0 total_qty,0 total_amt,'' prodl,'' prozl,'' proxl,'' bradl,'' brazl,'' braxl,0 price,'' status,0 basedisplay,0 maxval,0 minval"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and saledate<to_date('"+enddate+"', 'YYYY-MM-DD')"
    sqlstr+=" and braid='02058'"
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("插入第四周数据失败！")

print "heji"
#合计
try:
    startdate = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=28),"%Y-%m-%d")
    sqlstr="insert into xiaoshou28_maxmin_temp"
    sqlstr+=" select braid,proid,0 week1_qty,0 week1_amt,0 week2_qty,0 week2_amt,0 week3_qty,0 week3_amt,0 week4_qty,0 week4_amt,sum(saleqty) total_qty,sum(saleamt) total_amt,'' prodl,'' prozl,'' proxl,'' bradl,'' brazl,'' braxl,0 price,'' status,0 basedisplay,0 maxval,0 minval"
    sqlstr+=" from xiaoshou28 "
    sqlstr+=" where saledate>=to_date('"+startdate+"', 'YYYY-MM-DD')"
    sqlstr+=" and braid='02058'"
    sqlstr+=" group by braid,proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("插入合计数据失败！")

print "juji"
#聚集
try:
    sqlstr="insert into xiaoshou28_maxmin"
    sqlstr+=" select braid,proid,sum(week1_qty),sum(week1_amt),sum(week2_qty),sum(week2_amt),sum(week3_qty),sum(week3_amt),sum(week4_qty),sum(week4_amt),sum(total_qty) total_qty,sum(total_amt) total_amt,prodl,prozl,proxl,bradl,brazl,braxl,price,status,basedisplay,maxval,minval"
    sqlstr+=" from xiaoshou28_maxmin_temp"
    sqlstr+=" group by braid,proid,prodl,prozl, proxl,bradl,brazl,braxl,price,status,basedisplay,maxval,minval"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("聚集数据失败！")

print "dazhongxiao"
#更新商品大中小类与品牌大中小类
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set braxl=t2.braxl,brazl=t2.brazl,bradl=t2.bradl,proxl=t2.proxl,prozl=t2.prozl,prodl=t2.prodl"
    sqlstr+=" from product_all t2"
    sqlstr+=" where xiaoshou28_maxmin.proid=t2.proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新商品大中小类与品牌大中小类失败！")

print "price"
#更新价格
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set price=t2.normalprice"
    sqlstr+=" from product_all t2"
    sqlstr+=" where xiaoshou28_maxmin.proid=t2.proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新价格信息失败！")

print "basedisplay"
#基本陈列量算法：
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set basedisplay=4"
    sqlstr+=" where price<15"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新<15基本陈列量失败！")

try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set basedisplay=3"
    sqlstr+=" where price>=15 and price<30"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新>=15基本陈列量失败！")

try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set basedisplay=2.5"
    sqlstr+=" where price>=30 and price<50"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新>=30基本陈列量失败！")

try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set basedisplay=2"
    sqlstr+=" where price>=50 and price<100"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新>=50基本陈列量失败！")

try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set basedisplay=1.5"
    sqlstr+=" where price>=100 and price<200"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新>=100基本陈列量失败！")

try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set basedisplay=1"
    sqlstr+=" where price>=200 "
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新>=200基本陈列量失败！")

'挂带 基本陈列面数量都设为6'
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set basedisplay=6"
    sqlstr+=" from product_all t2"
    sqlstr+=" where t2.prodl like '%工具%' and xiaoshou28_maxmin.proid=t2.proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新挂带基本陈列量失败！")

#所有商品
#下限=基本陈列面数量+安全库存（2天）+送货周期（3天）
#上限=基本陈列面数量+安全库存（2天）+送货周期（6天）
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set minval=basedisplay+total_qty/28*2+total_qty/28*3,"
    sqlstr+=" maxval=basedisplay+total_qty/28*2+total_qty/28*6"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("对所有商品套用基本计算公式失败！")

print "status"
#商品状态
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set status=t2.status"
    sqlstr+=" from product_all t2"
    sqlstr+=" where xiaoshou28_maxmin.proid=t2.proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新商品状态失败！")

print "jianyizhi"
#上下限建议值
#男士护理品下限=基本陈列面数量+安全库存（2天）+送货周期（2天）；
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set minval=basedisplay+total_qty/28*2+total_qty/28*2"
    sqlstr+=" from product_all t2"
    sqlstr+=" where t2.prodl like '%男士%' and xiaoshou28_maxmin.proid=t2.proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新上下限建议值失败！")

print "quantou"
#自有品牌拳头产品 价格低于20元的,下限数量设为40个，上限数量设为60个；价格大于等于20元的，下限数量设为4个，上限数量设为5个；
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set minval=40,maxval=60"
    sqlstr+=" where price<20 and proid in("
    sqlstr+=" '00098571',	'00098588',	'00110280',	'00316248',	'00316262',	'00583602',	'00583619',	'00583626',	'00600651',	'00604352',	'00606646'"
    sqlstr+=" )"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set minval=4,maxval=5"
    sqlstr+=" where price>=20 and proid in("
    sqlstr+=" '00098571',	'00098588',	'00110280',	'00316248',	'00316262',	'00583602',	'00583619',	'00583626',	'00600651',	'00604352',	'00606646'"
    sqlstr+=" )"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新拳头产品失败！")

#夏季 类别小类里有杀虫剂（指蚊香跟花露水）、脱毛、止汗、面部保湿喷雾、防晒字眼的。上下限数量设置为2，只保证了基本陈列面需求；
print "xiaji"
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set maxval=2,minval=2"
    sqlstr+=" from product_all t2"
    sqlstr+=" where xiaoshou28_maxmin.proid=t2.proid and (t2.proxl like '%杀虫剂%'"
    sqlstr+=" or t2.proxl like '%蚊香%'"
    sqlstr+=" or t2.proxl like '%花露水%'"
    sqlstr+=" or t2.proxl like '%脱毛%'"
    sqlstr+=" or t2.proxl like '%止汗%'"
    sqlstr+=" or t2.proxl like '%面部保湿喷雾%'"
    sqlstr+=" or t2.proxl like '%防晒%'"
    sqlstr+=")"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新夏季产品失败！")

#护手霜。价格低于15元的，下限数量设为20，上限数量设为40；价格大于等于15元的下限数量设为10， 上限数量设为15；唇膏。价格低于35元的，下限数量设为9，上限数量设为12；价格大于等于35元的下限数量设为6，上限数量设为9；
print "dongji"
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set maxval=40,minval=20"
    sqlstr+=" where price<15 and proxl='护手霜'"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=15,minval=10"
    sqlstr+=" where price>=15 and proxl='护手霜'"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=12,minval=9"
    sqlstr+=" where price<35 and proxl='唇膏'"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=12,minval=9"
    sqlstr+=" where price<35 and proxl='唇彩'"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=12,minval=9"
    sqlstr+=" where price<35 and proxl='唇蜜'"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=9,minval=6"
    sqlstr+=" where price>=35 and proxl='唇膏'"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=9,minval=6"
    sqlstr+=" where price>=35 and proxl='唇彩'"
    cur.execute(sqlstr)
    conn.commit()

    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=9,minval=6"
    sqlstr+=" where price>=35 and proxl='唇蜜'"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新冬季商品失败！")

#高价位商品 销售大于120以上的下上限都设为2；
print "gaojiawei"
try:
    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=2,minval=2"
    sqlstr+=" where price>120"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新高价位商品失败！")

#部分无销售的香水数量设为1,护肤套装下限数量设为1，其它商品的下限数量都设为2以上(遵循基本公式)，保留了最低陈列面；
#香水
print "xiangshui"
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set minval=1"
    sqlstr+=" from product_all t2"
    sqlstr+=" where xiaoshou28_maxmin.proid=t2.proid and t2.prozl like '%香水%'"
    sqlstr+=" and xiaoshou28_maxmin.total_qty=0"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新香水失败！")

#有销售香水 基本公式算出下限<2的 设为2
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set minval=2"
    sqlstr+=" from product_all t2"
    sqlstr+=" where xiaoshou28_maxmin.proid=t2.proid and t2.prozl like '%香水%'"
    sqlstr+=" and xiaoshou28_maxmin.total_qty>0 and minval<2"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新香水<2的失败！")

#护肤套装
print "hufu"
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set minval=1"
    sqlstr+=" from product_all t2"
    sqlstr+=" where t2.prodl like '%护肤%' and t2.proname like '%套%' and xiaoshou28_maxmin.proid=t2.proid"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新护肤套装失败！")

#店用塑料袋 小的下限设为500个，上限设为1000个；大的下限设为300个，上限设为500个；
print "suliaodai"
#小塑料袋 00452564
try:
    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=1000,minval=500"
    sqlstr+=" where proid='00452564'"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新小塑料袋失败！")

#大塑料袋 00452540
try:
    sqlstr=" update xiaoshou28_maxmin"
    sqlstr+=" set maxval=500,minval=300"
    sqlstr+=" where proid='00452540'"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新大塑料袋失败！")

print "cuxiao"
#促销商品
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr+=" set maxval=xiaoshou28_maxmin.maxval*1.2,minval=xiaoshou28_maxmin.minval*1.2"
    sqlstr+=" from pmt t2"
    sqlstr+=" where xiaoshou28_maxmin.proid=t2.proid and t2.braid='02058' and (pmtdescription like '%1214%'"
    sqlstr+=" or pmtdescription like '%1215%')"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("更新促销商品失败！")

print "yuanzheng"
#上下限圆整
try:
    sqlstr="update xiaoshou28_maxmin"
    sqlstr=" set maxval=round(maxval),minval=round(minval);"
    cur.execute(sqlstr)
    conn.commit()
except:
    log("上下限圆整失败！")


