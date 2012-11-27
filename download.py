# -*- coding: utf-8 -*-

import datetime,time,memcache,os,codecs,gzip

from ftplib import FTP


yqfiles = ['product',
           'product_all',
           'v_allstock',
           'v_com_branch',
           'alloc','pmt',
           'v_sale_daily',
           'v_com_product']

downloaddir = 'D:\\getdata\\ftp\\'

ftpinfo = {"ip":'211.147.235.194',
           "port":'15443',
           "user":'ftpcl',
           "pwd":'ftpcl'}



def main():
    doclean = [doCleaning(file) for file in yqfiles]
    zipfiles = [ getzipfile(file) for file in yqfiles]
    ftpdownload(zipfiles)
    doconvert = [convertZip(file) for file in zipfiles]
    

def doCleaning(file):
    dir = downloaddir
    try:
        path = dir+file+'*'
        cmdstr = 'del /Q ' + dir + file + '*'
        print cmdstr
        os.system(cmdstr)
        return 'yes'
    except:
        return 'no'
    
def getzipfile(file):
    today=datetime.datetime.now().strftime('%Y-%m-%d')    
    return file + '_' + today + '.csv.zip'

def ftpdownload(zipfiles):
    ''' FTP下载 '''
    dir = downloaddir        
    ftp=FTP()
    ftp.set_debuglevel(2)
    ftp.connect(ftpinfo["ip"],ftpinfo["port"])
    ftp.login(ftpinfo["user"],ftpinfo["pwd"])
    #ftp.retrlines('LIST')
    for zip_file in zipfiles:
        ftp.retrbinary('RETR '+zip_file,open( dir + zip_file,'wb').write)
        print zip_file
    ftp.quit()
        
def convertZip(zipfile):
    ''' 解压缩并转为utf8编码 zipfile:zip压缩文件名'''
    try:
        dir = downloaddir
        z=gzip.open(dir+zipfile,'rb')
        content=z.read()
        content=content.decode('GBK')
        codecs.open(dir+zipfile[0:-4], 'w','utf8').write(content)
        z.close()
        return 'yes'
    except:
        return 'no'
    

if __name__=="__main__":
    main()
        
        
    



    







    
