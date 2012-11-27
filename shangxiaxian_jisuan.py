# -*- coding: utf-8 -*-
import datetime
import psycopg2
import psycopg2.extensions
import logging

def log(request):
    logging.basicConfig(filename='./mylog.log',level=logging.INFO)
    logging.info(request)

def main():
    dataserver = {"host":"localhost",
                  "port":5432,
                  "user":"fengmu",
                  "pwd": "zj",
                  "database":"yq3"
    }
    conn = psycopg2.connect(host=dataserver["host"], port=dataserver["port"],user=dataserver["user"],password=dataserver["pwd"],database=dataserver["database"])
    cur = conn.cursor()
    dhalldatainit(conn,cur)
    basedisplay(conn,cur)
    allproduct(conn,cur)
    manuse(conn,cur)
    quantou(conn,cur)
    xiaji(conn,cur)
    dongji(conn,cur)
    gaojiawei(conn,cur)
    xiangshui(conn,cur)
    hufu(conn,cur)
    suliaodai(conn,cur)
    cuxiao(conn,cur)
    yuanzheng(conn,cur)

def dhalldatainit(conn,cur):
    #从dhalldata中取初始数据初始化
    try:
        sqlstr="""
        delete from xiaoshou28_maxmin
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr="""
        insert into xiaoshou28_maxmin
        select mdcode,spcode,mdname,spname,week1_qty,week1_amt,week2_qty,week2_amt,week3_qty,week3_amt,week4_qty,week4_amt,total_qty,total_amt,prodl_id,prodl,prozl_id,prozl,proxl_id,proxl,bradl_id,bradl,brazl_id,brazl,braxl_id,braxl,normalprice,cuxiao_1,status,0,0 as maxval,0 as minval,maxval as oldmaxval,minval as oldminval
        from dhalldata
        where assortment is not null
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("从dhalldata中取初始数据初始化失败！")

def basedisplay(conn,cur):
    #基本陈列量算法：
    '''
    normalprice<30 3
    normalprice>=30 and normalprice<50 2.5
    normalprice>=50 and normalprice<100 2
    normalprice>=100 and normalprice<200 1.5
    normalprice>=200 1
    挂件 6
    '''
    try:
        sqlstr="""update xiaoshou28_maxmin
        set basedisplay=3
        where price<30
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新<30基本陈列量失败！")

    try:
        sqlstr="""update xiaoshou28_maxmin
        set basedisplay=2.5
        where price>=30 and price<50
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新>=30基本陈列量失败！")

    try:
        sqlstr="""update xiaoshou28_maxmin
        set basedisplay=2
        where price>=50 and price<100
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新>=50基本陈列量失败！")

    try:
        sqlstr="""update xiaoshou28_maxmin
        set basedisplay=1.5
        where price>=100 and price<200
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新>=100基本陈列量失败！")

    try:
        sqlstr="""update xiaoshou28_maxmin
        set basedisplay=1
        where price>=200
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新>=200基本陈列量失败！")

    '挂带 基本陈列面数量都设为6'
    try:
        sqlstr="""update xiaoshou28_maxmin
        set basedisplay=6
        where prodl like '%工具%'
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新挂带基本陈列量失败！")

def allproduct(conn,cur):
    #所有商品
    #下限=基本陈列面数量+安全库存（2天）+送货周期（3天）
    #上限=基本陈列面数量+安全库存（2天）+送货周期（6天）
    #假设所有商品销售为零的
    try:
        sqlstr="""update xiaoshou28_maxmin
        set minval=basedisplay,
        maxval=basedisplay
        where total_qty is null or total_qty=0
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("所有商品销售为零套用基本计算公式失败！")

    #有销售商品
    try:
        sqlstr="""update xiaoshou28_maxmin
        set minval=basedisplay+total_qty/28*2+total_qty/28*3,
        maxval=basedisplay+total_qty/28*2+total_qty/28*6
        where total_qty!=0 and total_qty is not null
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("对所有商品套用基本计算公式失败！")

def manuse(conn,cur):
    #男士护理品下限=基本陈列面数量+安全库存（2天）+送货周期（2天）；
    try:
        sqlstr=""" update xiaoshou28_maxmin
        set minval=basedisplay+COALESCE(total_qty, 0)/28*2+COALESCE(total_qty, 0)/28*2
        where prodl like '%男士%'
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新男士上下限建议值失败！")

def quantou(conn,cur):
    #自有品牌拳头产品 价格低于20元的,下限数量设为40个，上限数量设为60个；价格大于等于20元的，下限数量设为4个，上限数量设为5个；
    try:
        sqlstr="""update xiaoshou28_maxmin
        set minval=40,maxval=60
        where price<20 and proid in(
        '00098571',	'00098588',	'00110280',	'00316248',	'00316262',	'00583602',	'00583619',	'00583626',	'00600651',	'00604352',	'00606646')
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr="""update xiaoshou28_maxmin
        set minval=4,maxval=5
        where price>=20 and proid in(
        '00098571',	'00098588',	'00110280',	'00316248',	'00316262',	'00583602',	'00583619',	'00583626',	'00600651',	'00604352',	'00606646')
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新拳头产品失败！")

def xiaji(conn,cur):
    #夏季 类别小类里有杀虫剂（指蚊香跟花露水）、脱毛、止汗、面部保湿喷雾、防晒字眼的。上下限数量设置为2，只保证了基本陈列面需求；
    try:
        sqlstr="""
            update xiaoshou28_maxmin
            set maxval=2,minval=2
            where proxl like '%杀虫剂%'
            or proxl like '%蚊香%'
            or proxl like '%花露水%'
            or proxl like '%脱毛%'
            or proxl like '%止汗%'
            or proxl like '%面部保湿喷雾%'
            or proxl like '%防晒%'
            """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新夏季产品失败！")

def dongji(conn,cur):
    #护手霜。价格低于15元的，下限数量设为20，上限数量设为40；价格大于等于15元的下限数量设为10， 上限数量设为15；唇膏。价格低于35元的，下限数量设为9，上限数量设为12；价格大于等于35元的下限数量设为6，上限数量设为9；
    try:
        sqlstr="""update xiaoshou28_maxmin
        set maxval=40,minval=20
        where price<15 and proxl='护手霜'
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr=""" update xiaoshou28_maxmin
        set maxval=15,minval=10
        where price>=15 and proxl='护手霜'
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr=""" update xiaoshou28_maxmin
        set maxval=12,minval=9
        where price<35 and proxl='唇膏'
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr=""" update xiaoshou28_maxmin
        set maxval=12,minval=9
        where price<35 and proxl='唇彩'
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr=""" update xiaoshou28_maxmin
        set maxval=12,minval=9
        where price<35 and proxl='唇蜜'
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr=""" update xiaoshou28_maxmin
        set maxval=4,minval=3
        where price>=35 and proxl='唇膏'
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr=""" update xiaoshou28_maxmin
        set maxval=4,minval=3
        where price>=35 and proxl='唇彩'
        """
        cur.execute(sqlstr)
        conn.commit()

        sqlstr=""" update xiaoshou28_maxmin
        set maxval=4,minval=3
        where price>=35 and proxl='唇蜜'
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新冬季商品失败！")

def gaojiawei(conn,cur):
    #高价位商品 销售大于120以上的下上限都设为2；
    try:
        sqlstr=""" update xiaoshou28_maxmin
        set maxval=2,minval=2
        where price>120
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新高价位商品失败！")

def xiangshui(conn,cur):
    #部分无销售的香水数量设为1,护肤套装下限数量设为1，其它商品的下限数量都设为2以上(遵循基本公式)，保留了最低陈列面；
    #香水
    try:
        sqlstr="""
        update xiaoshou28_maxmin
        set minval=1
        where prozl like '%香水%'
        and total_qty=0
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新香水失败！")

    #有销售香水 基本公式算出下限<2的 设为2
    try:
        sqlstr="""
        update xiaoshou28_maxmin
        set minval=2
        where prozl like '%香水%'
        and total_qty>0 and minval<2
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新香水<2的失败！")

def hufu(conn,cur):
    #护肤套装
    try:
        sqlstr="""
        update xiaoshou28_maxmin
        set minval=1
        where prodl_id ='11' and spname like '%套%'
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新护肤套装失败！")

def suliaodai(conn,cur):
    #店用塑料袋 小的下限设为500个，上限设为1000个；大的下限设为300个，上限设为500个；
    #小塑料袋 00452564
    try:
        sqlstr="""
        update xiaoshou28_maxmin
        set maxval=1000,minval=500
        where proid='00452564'
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新小塑料袋失败！")

    #大塑料袋 00452540
    try:
        sqlstr=""" update xiaoshou28_maxmin
        set maxval=500,minval=300
        where proid='00452540'
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新大塑料袋失败！")

def cuxiao(conn,cur):
    #促销商品
    try:
        sqlstr="""
        update xiaoshou28_maxmin
        set maxval=maxval*1.2,minval= minval*1.2
        where cuxiao_1='T'
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("更新促销商品失败！")

def yuanzheng(conn,cur):
    #上下限圆整
    try:
        sqlstr="""
        update xiaoshou28_maxmin
        set maxval=round(maxval+0.2),minval=round(minval+0.2)
        """
        cur.execute(sqlstr)
        conn.commit()
    except:
        log("上下限圆整失败！")

if __name__=="__main__":
    main()



