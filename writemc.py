## -*- coding: utf-8 -*-

import download
import process, processcl, processdh, processrep
import importmem, shangxiaxian_jisuan
import importmemdh
from mylog import log
import datetime,time

def main():
    today=datetime.datetime.now().strftime('%Y-%m-%d')
    
    log("***********************" + str(today) + "******************************")
    log("writemc:"+str(today)+" start at "+str(time.asctime()))
    
    download.main()
    log("donwnload:"+str(today)+" end at "+str(time.asctime()))
    #print " end at "+str(time.asctime())
    
    
    process.main()
    log("process:"+str(today)+" end at "+str(time.asctime()))
    
    processcl.main()
    log("processcl:"+str(today)+" end at "+str(time.asctime()))   
    
    
    processdh.main()
    log("processdh:"+str(today)+" end at "+str(time.asctime()))
    
    importmemdh.main()
    log("importmemdh:"+str(today)+" end at "+str(time.asctime()))
    
    processrep.main()
    log("processrep:"+str(today)+" end at "+str(time.asctime()))
    
    shangxiaxian_jisuan.main()
    log("shangxiaxian_jisuan"+str(today)+" end at "+str(time.asctime()))
    
    

    
    #importmem.main("select braid from branch where braid = '02058'")
    #log("impormem:"+str(today)+" end at "+str(time.asctime()))    
    
    
    log("writemc:"+str(today)+" end at "+str(time.asctime()))
    
if __name__=="__main__":
    main()
