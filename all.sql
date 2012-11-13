--=============================================================================
--     FileName: all.sql
--         Desc: 
--       Author: solomon
--        Email: 253376634@qq.com
--     HomePage: 
--      Version: 0.0.1
--   LastChange: 2012-10-24 10:59:02
--      History:
--=============================================================================
drop TABLE allstock;
drop TABLE branch;
drop TABLE product;
drop TABLE maxminval;
drop TABLE sugvalue;
drop TABLE sugvalue_temp;
drop TABLE maxmin; --用户导入
drop TABLE delivery; --用户导入
drop TABLE deliveryval;
drop TABLE brainfo; --门店综合信息 供重算审核 
drop TABLE xiaoshou
drop TABLE xiaoshou28
drop TABLE v_sale_daily_14
drop TABLE v_sale_daily
drop TABLE v_sale_daily_201208
drop TABLE alloc
drop TABLE pmt
drop TABLE xiaoshou28_res
drop TABLE xiaoshou28_res_temp
drop TABLE xiaoshou28_res_temp
drop TABLE product_all
drop TABLE quantou

-- 库存表
CREATE TABLE allstock
(
  braid character varying(100),
  proid character varying(100),
  curqty numeric(12,3)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE allstock OWNER TO postgres;

-- 上下限表
CREATE TABLE maxmin
(
  braid character varying(100),
  proid character varying(100),
  maxval numeric(12,3),
  minval numeric(12,3),
  banben character varying(4),
  startdate character varying(20),
  enddate character varying(20),
  adddate character varying(20)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE maxmin OWNER TO postgres;


--有效上下限表
CREATE TABLE maxminval
(
  braid character varying(100),
  proid character varying(100),
  maxval numeric(12,0),
  minval numeric(12,0)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE maxminval OWNER TO postgres;

-- 配送建议值表
CREATE TABLE sugvalue
(
  braid character varying(100),
  braname character varying(100),
  proid character varying(100),
  proname character varying(100),
  suggest numeric(12,3),
  suggestcost numeric(12,3),
  maxval numeric(12,3),
  minval numeric(12,3),
  curqty numeric(12,3),
  AllocQty numeric(12,3)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE sugvalue OWNER TO postgres;

-- 配送建议值中间表
CREATE TABLE sugvalue_temp
(
  braid character varying(100),
  braname character varying(100),
  proid character varying(100),
  proname character varying(100),
  suggest numeric(12,3),
  suggestcost numeric(12,3),
  maxval numeric(12,3),
  minval numeric(12,3),
  curqty numeric(12,3),
  AllocQty numeric(12,3)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE sugvalue OWNER TO postgres;


-- 配送规则表
CREATE TABLE delivery
(
  braid character varying(100),
  weekdelivery character varying(100),
  adddate character varying(20)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE delivery OWNER TO postgres;

--符合配送规则门店
CREATE TABLE deliveryval
(
  braid character varying(100)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE deliveryval OWNER TO postgres;

-- 门店表
CREATE TABLE branch
(
  hqid character varying(3),
  braid character varying(5) NOT NULL,
  braname character varying(40) NOT NULL,
  brasname character(16) NOT NULL,
  bratype character(1),
  bracode character varying(10),
  addr character varying(40),
  tel character varying(30),
  fax character varying(30),
  zipcode character(6),
  distid character(4),
  master character varying(8),
  opendate timestamp without time zone,
  sizecode character(1),
  square numeric(8,2),
  allopriority character(1),
  allodiscount numeric(5,3),
  allopricelevel integer,
  alloperoid integer,
  reserveamt integer,
  manageamt integer,
  paydate integer,
  whid character varying(5),
  sprice_quotiety numeric(4,2),
  mprice_quotiety numeric(4,2),
  vehiclenum integer,
  empcount integer,
  managemode character(1),
  place character(1),
  storetype character(1),
  status character(1),
  serialno integer,
  createdate timestamp without time zone,
  updatedate timestamp without time zone,
  purchaseid character varying(5),
  settlemethod character(1),
  paymethod character(1),
  settledays integer,
  saletype character(1),
  alloctype character(1),
  closedate timestamp without time zone,
  macaddr character varying(20),
  sys_regno character varying(255),
  mac_regno character varying(255),
  useperiod character varying(6),
  clientnum character varying(6),
  accounttype character(1)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE branch OWNER TO postgres;

-- 商品表
CREATE TABLE product
(
  proid character varying(13) NOT NULL,
  barcode character varying(13) NOT NULL,
  proname character varying(50) NOT NULL,
  prosname character varying(30),
  classid character varying(8),
  spec character varying(12),
  brandid character varying(8),
  statid character varying(8),
  grade character varying(6),
  area character varying(12),
  supid character varying(8),
  measureid character varying(2),
  packetqty numeric(12,3),
  packetqty1 numeric(12,3),
  weight numeric(12,3),
  length numeric(8,2),
  width numeric(8,2),
  height numeric(8,2),
  taxtype character(1),
  intax numeric(5,3),
  saletax numeric(5,3),
  inprice numeric(12,5),
  taxprice numeric(12,5),
  normalprice numeric(10,2),
  memberprice numeric(10,2),
  groupprice numeric(10,2),
  mainflag character(1),
  proflag character(1),
  weightflag character(1),
  barmode character(1),
  ordermode character(1),
  minorderqty numeric(12,3),
  ordermultiplier numeric(12,3),
  freshmode character(1),
  returnrat numeric(5,3),
  warrantydays integer,
  udf1 character varying(20),
  udf2 character varying(20),
  udf3 character varying(20),
  status character(1),
  promtflag character(1),
  potflag character(1),
  canchangeprice character(1),
  avgcostprice numeric(12,5),
  cardpoint numeric(12,3),
  createdate timestamp without time zone,
  updatedate timestamp without time zone,
  stopdate timestamp without time zone,
  suppmtflag character(1),
  operatorid character varying(5)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE product OWNER TO postgres;


--门店综合信息 供门店审核是否需要重写
-- Table: brainfo

-- DROP TABLE brainfo;

CREATE TABLE brainfo
(
  "门店代码" character varying(5) NOT NULL,
  "门店名称" character varying(100),
  "品项数" bigint,
  "库存数量" numeric,
  "建议订货总量" numeric,
  "建议订货总额" numeric
)
WITH (
  OIDS=FALSE
);
ALTER TABLE brainfo OWNER TO postgres;

--14天销售
CREATE TABLE v_sale_daily_14
(
  hqid character varying(3) NOT NULL,
  braid character varying(5) NOT NULL,
  saledate timestamp without time zone NOT NULL,
  proid character varying(13) NOT NULL,
  barcode character varying(50) NOT NULL,
  classid character varying(8) NOT NULL,
  brandid character varying(8) NOT NULL,
  donatetype character(1),
  transtype character(1),
  productpmtplanno character varying(20),
  brandpmtplanno character varying(20),
  transpmtplanno character varying(20),
  producttype character(1),
  saletax numeric(5,3),
  posno character(4),
  salerid character varying(5),
  saleman character varying(5),
  saletype character(1) NOT NULL,
  saleqty numeric(12,3),
  saleamt numeric(14,2),
  saledisamt numeric(14,2),
  transdisamt numeric(14,2),
  normalprice numeric(10,2),
  curprice numeric(10,2),
  lastcostprice numeric(12,5),
  saleid character varying(20) NOT NULL,
  memcardno character varying(16),
  invoiceid character varying(20),
  points1 numeric(10,2),
  points numeric(10,2),
  returnrat numeric(5,3),
  inputdate timestamp without time zone NOT NULL,
  sendflag character(1),
  classpmtplanno character varying(20),
  brandclasspmtplanno character varying(20),
  productclusterpmtplanno character varying(20),
  pcashpayamt numeric(14,2),
  integralpayamt numeric(14,2),
  updatedate timestamp without time zone,
  pmtsale character varying(1) NOT NULL
)

--销售表 供写入内存14天销售
CREATE TABLE xiaoshou 
(
  "braid" character varying(5) NOT NULL,
  "proid" character varying(13) NOT NULL,
  "s1" numeric(13,3),
  "s2" numeric(13,3),
  "s3" numeric(13,3),
  "s4" numeric(13,3),
  "s5" numeric(13,3),
  "s6" numeric(13,3),
  "s7" numeric(13,3),
  "s8" numeric(13,3),
  "s9" numeric(13,3),
  "s10" numeric(13,3),
  "s11" numeric(13,3),
  "s12" numeric(13,3),
  "s13" numeric(13,3),
  "s14" numeric(13,3),
  "t1" numeric(12,2),
  "t2" numeric(12,2),
  "t3" numeric(12,2),
  "t4" numeric(12,2),
  "t5" numeric(12,2),
  "t6" numeric(12,2),
  "t7" numeric(12,2),
  "t8" numeric(12,2),
  "t9" numeric(12,2),
  "t10" numeric(12,2),
  "t11" numeric(12,2),
  "t12" numeric(12,2),
  "t13" numeric(12,2),
  "t14" numeric(12,2)
)


--在途数据
create table alloc(
braid character varying(5) NOT NULL,
proid character varying(13) NOT NULL,
AllocQty numeric(12,3)
)

--促销商品
create table pmt(
braid character varying(5) NOT NULL,
proid character varying(13) NOT NULL,
pmtdescription character varying(255),
startdate timestamp without time zone NOT NULL,
enddate timestamp without time zone NOT NULL
)


--原始销售数据
create table v_sale_daily(
  hqid character varying(3) NOT NULL,
  braid character varying(5) NOT NULL,
  saledate timestamp without time zone NOT NULL,
  proid character varying(13) NOT NULL,
  barcode character varying(50) NOT NULL,
  classid character varying(8) NOT NULL,
  brandid character varying(8) NOT NULL,
  donatetype character(1),
  transtype character(1),
  productpmtplanno character varying(20),
  brandpmtplanno character varying(20),
  transpmtplanno character varying(20),
  producttype character(1),
  saletax numeric(5,3),
  posno character(4),
  salerid character varying(5),
  saleman character varying(5),
  saletype character(1) NOT NULL,
  saleqty numeric(12,3),
  saleamt numeric(14,2),
  saledisamt numeric(14,2),
  transdisamt numeric(14,2),
  normalprice numeric(10,2),
  curprice numeric(10,2),
  lastcostprice numeric(12,5),
  saleid character varying(20) NOT NULL,
  memcardno character varying(16),
  invoiceid character varying(20),
  points1 numeric(10,2),
  points numeric(10,2),
  returnrat numeric(5,3),
  inputdate timestamp without time zone NOT NULL,
  sendflag character(1),
  classpmtplanno character varying(20),
  brandclasspmtplanno character varying(20),
  productclusterpmtplanno character varying(20),
  pcashpayamt numeric(14,2),
  integralpayamt numeric(14,2),
  updatedate timestamp without time zone,
  pmtsale character varying(1) NOT NULL
)


--只存放28天销售数据
CREATE TABLE xiaoshou28
(
  hqid character varying(3),
  braid character varying(5),
  saledate timestamp without time zone,
  proid character varying(13),
  barcode character varying(50),
  classid character varying(8),
  brandid character varying(8),
  donatetype character(1),
  transtype character(1),
  productpmtplanno character varying(20),
  brandpmtplanno character varying(20),
  transpmtplanno character varying(20),
  producttype character(1),
  saletax numeric(5,3),
  posno character(4),
  salerid character varying(5),
  saleman character varying(5),
  saletype character(1),
  saleqty numeric(12,3),
  saleamt numeric(14,2),
  saledisamt numeric(14,2),
  transdisamt numeric(14,2),
  normalprice numeric(10,2),
  curprice numeric(10,2),
  lastcostprice numeric(12,5),
  saleid character varying(20),
  memcardno character varying(16),
  invoiceid character varying(20),
  points1 numeric(10,2),
  points numeric(10,2),
  returnrat numeric(5,3),
  inputdate timestamp without time zone,
  sendflag character(1),
  classpmtplanno character varying(20),
  brandclasspmtplanno character varying(20),
  productclusterpmtplanno character varying(20),
  pcashpayamt numeric(14,2),
  integralpayamt numeric(14,2),
  updatedate timestamp without time zone,
  pmtsale character varying(1)
)


--28天销售加工结果临时表
create table xiaoshou28_res_temp(
braid character varying(5),
proid character varying(13),
week1_qty numeric(13,3),
week1_amt numeric(12,2),
week2_qty numeric(13,3),
week2_amt numeric(12,2),
week3_qty numeric(13,3),
week3_amt numeric(12,2),
week4_qty numeric(13,3),
week4_amt numeric(12,2),
total_qty numeric(13,3),
total_amt numeric(12,2)
);

--28天销售加工结果
create table xiaoshou28_res(
braid character varying(5),
proid character varying(13),
week1_qty numeric(13,3),
week1_amt numeric(12,2),
week2_qty numeric(13,3),
week2_amt numeric(12,2),
week3_qty numeric(13,3),
week3_amt numeric(12,2),
week4_qty numeric(13,3),
week4_amt numeric(12,2),
total_qty numeric(13,3),
total_amt numeric(12,2)
);

--28天销售上下限程序生成结果临时表
create table xiaoshou28_maxmin_temp(
braid character varying(5),
proid character varying(13),
week1_qty numeric(13,3),
week1_amt numeric(12,2),
week2_qty numeric(13,3),
week2_amt numeric(12,2),
week3_qty numeric(13,3),
week3_amt numeric(12,2),
week4_qty numeric(13,3),
week4_amt numeric(12,2),
total_qty numeric(13,3),
total_amt numeric(12,2),
prodl character varying(255), --商品大类
prozl character varying(255),
proxl character varying(255),
bradl character varying(255),
brazl character varying(255),
braxl character varying(255),
price numeric(13,2), --单价
status character varying(255),
basedisplay numeric(13,2),
maxval numeric(13,2),
minval numeric(13,2)
);

--28天上下限程序生成结果
create table xiaoshou28_maxmin(
braid character varying(5),
proid character varying(13),
week1_qty numeric(13,3),
week1_amt numeric(12,2),
week2_qty numeric(13,3),
week2_amt numeric(12,2),
week3_qty numeric(13,3),
week3_amt numeric(12,2),
week4_qty numeric(13,3),
week4_amt numeric(12,2),
total_qty numeric(13,3),
total_amt numeric(12,2),
prodl character varying(255), --商品大类
prozl character varying(255),
proxl character varying(255),
bradl character varying(255),
brazl character varying(255),
braxl character varying(255),
price numeric(13,2), --单价
status character varying(255),
basedisplay numeric(13,2),
maxval numeric(13,2),
minval numeric(13,2)
);


--商品配送单位
CREATE TABLE product_gl_packetqty_rules
(
  xcode character varying(13),  --代码
  excode character varying(13), --代码说明
  packetqty1 numeric(12,3)      --配货单位  必须是大于l零的整数
);

--商品最大最小上下限规则
CREATE TABLE dhrules
(
  mdcode character varying(16),  --门店代码 (02058, null)
  xcode character varying(16),   --代码
  excode character varying(16),  --代码说明 (sp, xl, zl, dl, null)
  yqkey character varying(16),   --规则对象 (maxlimit, minlimit)
  yqrule character varying(16),  --规则说明 (jd, xd)
  yqvalue character varying(16)  --规则值
);

-- Table: product_all

-- DROP TABLE product_all;

CREATE TABLE product_all
(
  proid character varying(13),
  barcode character varying(13),
  proname character varying(50),
  prosname character varying(30),
  classid character varying(8),
  spec character varying(12),
  brandid character varying(8),
  statid character varying(8),
  grade character varying(6),
  area character varying(12),
  supid character varying(8),
  measureid character varying(2),
  packetqty numeric(12,3),
  packetqty1 numeric(12,3),
  weight numeric(12,3),
  length numeric(8,2),
  width numeric(8,2),
  height numeric(8,2),
  taxtype character(1),
  intax numeric(5,3),
  saletax numeric(5,3),
  inprice numeric(12,5),
  taxprice numeric(12,5),
  normalprice numeric(10,2),
  memberprice numeric(10,2),
  groupprice numeric(10,2),
  mainflag character(1),
  proflag character(1),
  weightflag character(1),
  barmode character(1),
  ordermode character(1),
  minorderqty numeric(12,3),
  ordermultiplier numeric(12,3),
  freshmode character(1),
  returnrat numeric(5,3),
  warrantydays integer,
  udf1 character varying(20),
  udf2 character varying(20),
  udf3 character varying(20),
  status character(1),
  promtflag character(1),
  potflag character(1),
  canchangeprice character(1),
  avgcostprice numeric(12,5),
  cardpoint numeric(12,3),
  createdate timestamp without time zone,
  updatedate timestamp without time zone,
  stopdate timestamp without time zone,
  suppmtflag character(1),
  operatorid character varying(5),
  braxl_id character varying(10),
  braxl character varying(100),
  brazl_id character varying(10),
  brazl character varying(100),
  bradl_id character varying(10),
  bradl character varying(100),
  proxl_id character varying(10),
  proxl character varying(100),
  prozl_id character varying(10),
  prozl character varying(100),
  prodl_id character varying(10),
  prodl character varying(100)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE product_all OWNER TO postgres;


create table quantou
(
  proid character varying(100)
)


'''
--测试数据
insert into allstock values('00000017','02001',23);
insert into allstock values('00000024','02001',6);
insert into allstock values('00000017','02002',24);
insert into allstock values('00000024','02002',21);
insert into allstock values('00000017','02003',25);
insert into allstock values('00000024','02003',23);
insert into maxmin values('00000017','02001',29,33,'B','2012-08-15','2012-08-25');
insert into maxmin values('00000024','02001',23,16,'B','2012-08-17','2012-08-25');
insert into maxmin values('00000017','02002',28,20,'B','2012-08-10','2012-08-25');
insert into maxmin values('00000017','02001',28,20,'A',NULL,NULL);
insert into maxmin values('00000017','02003',39,23,'A',NULL,NULL);
insert into maxmin values('00000024','02003',39,23,'A',NULL,NULL);
insert into delivery values('02001','星期一');
insert into delivery values('02002','星期二');
insert into delivery values('02003','星期三');
insert into delivery values('02004','星期三');
insert into delivery values('02005','星期三');
insert into delivery values('02006','星期三');
'''

'''
--存储过程

CREATE FUNCTION sugvalue_temp() RETURNS void AS $$

	    --生成建议值
        insert into sugvalue_temp
        SELECT  t1.braid, t2.braname,t1.proid, t3.proname,0 AS suggest, 0 AS suggestcost,t1.maxval,t1.minval,0 As curqty
        FROM maxminval t1, branch t2, product t3
        WHERE t1.braid=t2.braid and t1.proid=t3.proid;
        
        insert into sugvalue_temp
        SELECT  t1.braid, t2.braname,t1.proid, t3.proname,0 AS suggest, 0 AS suggestcost,0 as maxval,0 as minval ,t1.curqty
        FROM allstock t1, branch t2, product t3
        WHERE t1.braid=t2.braid and t1.proid=t3.proid;
        
        insert into sugvalue 
        select braid, braname, proid, proname, sum(suggest) as suggest, sum(suggestcost) as suggestcost, sum(maxval) as maxval, sum(minval) as minval, sum(curqty) as curqty
        from sugvalue_temp
        group by braid, braname, proid, proname; 
        
        update sugvalue
        set suggest=maxval-curqty, suggestcost=(maxval-curqty)*product.normalprice        
        from product       
        where sugvalue.proid=product.proid
        and sugvalue.curqty < sugvalue.minval
        and sugvalue.maxval > 0
        and sugvalue.curqty > 0;
            
$$ LANGUAGE SQL;

'''
