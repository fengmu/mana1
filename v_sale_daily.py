#encoding:utf-8
'''
#=============================================================================
#     FileName: v_sale_daily.py
#         Desc: 2周销售数据
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-09-13 21:59:29
#      History:
#=============================================================================
'''
import datetime,time,memcache,os,codecs,gzip
from mylog import log
from ftplib import FTP
from confsql import Confsql
#import pdb
#pdb.set_trace()
class v_sale_daily():
    def __init__(self,dbstr="postgres://postgres:zcbdcyj123@localhost/yq3",mchost="127.0.0.1:11211",sqlstr=""):
    #def __init__(self,dbstr="postgres://fengmu:zj@localhost/yq3",mchost='127.0.0.1:11211',sqlstr=""):
        self.dbstr=dbstr
        self.mchost=mchost
        self.sqlstr=sqlstr
        st=time.time()
        today=datetime.datetime.now().strftime('%y-%m-%d')
        #log("v_sale_daily:"+str(today)+" start at "+str(time.asctime()))
        self.doCleaning() #清理
        #log("doCleaning:"+str(today)+" end at "+str(time.asctime()))
        #os.system('cmd.exe /c c:/ZSW/memcached/memcached.exe -m 256 -p 11211') #开启内存服务
        #today='2012-08-30'
        zip_file='v_sale_daily_'+str(today)+'.csv.zip'
        conn=Confsql(dbstr,mchost)
        self.ftpdownload(zip_file) #下载zip文件
        log("download:"+str(today)+" end at "+str(time.asctime()))
        self.ConvertZip(zip_file)
        self.writepostgrs(conn) #写postgres
        self.writepostgrs_fm(conn) #写postgres
        #log("writepostgrs:"+str(today)+" end at "+str(time.asctime()))
        conn.writemc_xiaoshou() #写内存
        en=time.time()
        
        #log("writemc:"+str(today)+" end at "+str(time.asctime()))
        #log("writemc:"+str(today)+" cost "+str((en-st)/60)+" Minute")
        
    def ftpdownload(self,zip_file):
        ''' FTP下载 '''
        start_time=time.time()
        ftp=FTP()
        ftp.set_debuglevel(2)
        ftp.connect('211.147.235.194','15443')
        ftp.login('ftpcl','ftpcl')
        #ftp.retrlines('LIST')
        ftp.retrbinary('RETR '+zip_file,open('D:/getdata/ftp/'+zip_file,'wb').write)
        end_time=time.time()

    def ConvertZip(self,zip_file):
        ''' 解压缩 '''
        #os.rename('D:/getdata/ftp/'+zip_file,'D:/getdata/ftp/'+zip_file[0:-4]+".gz") 
        #os.system('cmd.exe /c gzip -d D:/getdata/ftp/'+zip_file[0:-4]+".gz")
        z=gzip.open('D:/getdata/ftp/'+zip_file,'rb')
        content=z.read()
        content=content.decode('GBK')
        codecs.open('D:/getdata/ftp/'+zip_file[0:-4], 'w','utf8').write(content)
        z.close()

    def writepostgrs(self,theconfsql):
        today=datetime.datetime.now().strftime('%y-%m-%d')
        ''' 写入postgreSQL'''
        #设置临时环境变量 postgreSQL数据库密码
        
        os.system('cmd.exe /c set PGPASSWORD=zcbdcyj123')
        
        #清空前三天数据
        startdate=(datetime.date.today()-datetime.timedelta(days=3)).strftime('%y-%m-%d')
        os.system('cmd.exe /c C:/Progra~1/postgreSQL/8.4/bin/psql.exe -h localhost -U postgres -d yq3 -p 5432 -c "delete from v_sale_daily_14 where saledate >=\''+startdate+'\'";')
       
        #导入三天数据 导入postgreSQL
        os.system('cmd.exe /c C:/Progra~1/postgreSQL/8.4/bin/psql.exe -h localhost -U postgres -d yq3 -p 5432 -c "copy v_sale_daily_14 from \'D:/getdata/ftp/v_sale_daily_'+today+'.csv\' delimiter as E\'\t\' csv";')
        
        #数据加工
        startdate=(datetime.date.today()-datetime.timedelta(days=14)).strftime('%Y-%m-%d')

        s='insert into xiaoshou'
        s=s+' select braid,proid'
        s=s+' from v_sale_daily_14'
        s=s+' where saledate>=\''+startdate+'\''
        s=s+' group by braid,proid'
        os.system('cmd.exe /c C:/Progra~1/postgreSQL/8.4/bin/psql.exe -h localhost -U postgres -d yq3 -p 5432 -c "'+s+'"') 

        for i in range(1,15):
            j=15-i
            startdate=(datetime.date.today()-datetime.timedelta(days=j)).strftime('%Y-%m-%d')
            s='update xiaoshou'
            s=s+' set s'+str(i)+'=t2.saleqty, '
            s=s+' t'+str(i)+'=t2.saleamt'
            s=s+' from (select braid,proid,sum(saleqty) AS saleqty , sum(saleamt) AS saleamt from v_sale_daily_14 where saledate=\''+startdate+'\' group by braid,proid) t2'
            s=s+' where xiaoshou.braid=t2.braid '
            s=s+'  and xiaoshou.proid=t2.proid'
            print s
            os.system('cmd.exe /c C:/Progra~1/postgreSQL/8.4/bin/psql.exe -h localhost -U postgres -d yq3 -p 5432 -c "'+s+'"') 
    
    def writepostgrs_fm(self,theconfsql):
        today=datetime.datetime.now().strftime('%y-%m-%d')
        ''' 写入postgreSQL'''
        #设置临时环境变量 postgreSQL数据库密码
        
        os.system('set PGPASSWORD=zj')
        
        #清空前三天数据
        startdate=(datetime.date.today()-datetime.timedelta(days=3)).strftime('%y-%m-%d')
        os.system('d:/Progra~1/postgreSQL/8.3/bin/psql.exe -h localhost -U fengmu -d yq3 -p 5432 -c "delete from v_sale_daily_14 where saledate >=\''+startdate+'\'";')
       
        #导入三天数据 导入postgreSQL
        os.system('d:/Progra~1/postgreSQL/8.3/bin/psql.exe -h localhost -U fengmu -d yq3 -p 5432 -c "copy v_sale_daily_14 from \'D:/getdata/ftp/v_sale_daily_'+today+'.csv\' delimiter as E\'\t\' csv";')
        
        #数据加工
        startdate=(datetime.date.today()-datetime.timedelta(days=14)).strftime('%Y-%m-%d')

        s='insert into xiaoshou'
        s=s+' select braid,proid'
        s=s+' from v_sale_daily_14'
        s=s+' where saledate>=\''+startdate+'\''
        s=s+' group by braid,proid'
        os.system('d:/Progra~1/postgreSQL/8.3/bin/psql.exe -h localhost -U fengmu -d yq3 -p 5432 -c "'+s+'"') 

        for i in range(1,15):
            j=15-i
            startdate=(datetime.date.today()-datetime.timedelta(days=j)).strftime('%Y-%m-%d')
            s='update xiaoshou'
            s=s+' set s'+str(i)+'=t2.saleqty, '
            s=s+' t'+str(i)+'=t2.saleamt'
            s=s+' from (select braid,proid,sum(saleqty) AS saleqty , sum(saleamt) AS saleamt from v_sale_daily_14 where saledate=\''+startdate+'\' group by braid,proid) t2'
            s=s+' where xiaoshou.braid=t2.braid '
            s=s+'  and xiaoshou.proid=t2.proid'
            print s
            os.system('d:/Progra~1/postgreSQL/8.3/bin/psql.exe -h localhost -U fengmu -d yq3 -p 5432 -c "'+s+'"') 

    def doCleaning(self):
        os.system('cmd.exe /c del /Q D:\\getdata\\ftp\\v_sale_daily*')

if __name__=="__main__":
    """
    st=time.time()
    today=datetime.datetime.now().strftime('%Y-%m-%d')
    dbstr="postgres://fengmu:zj@localhost/yq3"
    mchost='127.0.0.1:11211'
    #os.system('cmd.exe /c c:/ZSW/memcached/memcached.exe -m 256 -p 11211') #开启内存服务
    zipfiles=['product_'+today+'.csv.zip','v_allstock_'+today+'.csv.zip','v_com_branch_'+today+'.csv.zip']
    conn=confsql(dbstr,mchost)

    ftpdownload(zipfiles) #下载zip文件
    ConvertZip(zipfiles) #转换为csv
    writepostgrs() #写postgres
    conn.main() #写内存
    doCleaning() #清理
    en=time.time()
    print str((en-st)/60)+"Minute"
    """
    v_sale_daily()

