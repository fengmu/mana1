#coding:utf-8
'''
#=============================================================================
#     FileName: urls.py
#         Desc: 
#       Author: solomon
#        Email: 253376634@qq.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2012-08-09 09:21:19
#      History:
#=============================================================================
'''
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r'^insult_maxmin/$','mana1.maxmin.insult_maxmin'),  #上下限
    url(r'^import_maxmin/$','mana1.maxmin.import_maxmin'),
    url(r'^save_maxmin/$','mana1.maxmin.save_maxmin'),
    url(r'^backup_maxmin/$','mana1.maxmin.backup_maxmin'),
    
    url(r'^insult_shangxiaxian/','mana1.shangxiaxian.insult_shangxiaxian'), #计算新的上下限
    url(r'^checkAdvMaxMin/$','mana1.checkAdvMaxMin.checkAdvMaxMin'),    
    url(r'^save_checkadvmaxmin/$', 'mana1.checkAdvMaxMin.save_checkAdvMaxMin'),
    url(r'^insult_checkAdvMaxMin/$','mana1.checkAdvMaxMin.insult_checkAdvMaxMin'),

    url(r'^insult_delivery/$','mana1.delivery.insult_delivery'), #配送日
    url(r'^import_delivery/$','mana1.delivery.import_delivery'),
    url(r'^delete_delivery/$','mana1.delivery.delete_delivery'),
    url(r'^save_delivery/$','mana1.delivery.save_delivery'),
    url(r'^deleteData_delivery/$','mana1.delivery.deleteData_delivery'),

    url(r'^insult_product_gl_packetqty_rules/','mana1.product_gl_packetqty_rules.insult_product_gl_packetqty_rules'), #商品配送单位规则查询界面
    url(r'^import_product_gl_packetqty_rules/','mana1.product_gl_packetqty_rules.import_product_gl_packetqty_rules'), #商品配送单位规则导入
    url(r'^delete_product_gl_packetqty_rules/','mana1.product_gl_packetqty_rules.delete_product_gl_packetqty_rules'), #商品配送单位规则删除界面
    url(r'^save_product_gl_packetqty_rules/','mana1.product_gl_packetqty_rules.save_product_gl_packetqty_rules'), #商品配送单位规则保存
    url(r'^deleteData_product_gl_packetqty_rules/','mana1.product_gl_packetqty_rules.deleteData_product_gl_packetqty_rules'), #商品配送单位规则删除

    url(r'^insult_dhrules/','mana1.dhrules.insult_dhrules'), #商品最大最小上下限规则查询
    url(r'^import_dhrules/','mana1.dhrules.import_dhrules'), #商品最大最小上下限规则导入界面    
    url(r'^save_dhrules/','mana1.dhrules.save_dhrules'), #商品最大最小上下限规则导入
    url(r'^delete_dhrules/','mana1.dhrules.delete_dhrules'), #商品最大最小上下限规则删除界面
    url(r'^deleteData_dhrules/','mana1.dhrules.deleteData_dhrules'), #商品最大最小上下限规则删除

    

    url(r'^insult_dhPauserules/','mana1.dhPauserules.insult_dhPauserules'), #暂停订货范围规则查询    
    url(r'^import_dhPauserules/','mana1.dhPauserules.import_dhPauserules'),
    url(r'^save_dhPauserules/','mana1.dhPauserules.save_dhPauserules'), 
    url(r'^delete_dhPauserules/','mana1.dhPauserules.delete_dhPauserules'), 
    url(r'^deleteData_dhPauserules/','mana1.dhPauserules.deleteData_dhPauserules'), 
    
    url(r'^insult_sugvalue/$','mana1.sugvalue.insult_sugvalue'),    
    url(r'^tranedit/$', 'mana1.tranedit.tranedit'),
    url(r'^rewrite/$', 'mana1.rewrite.rewrite'),                      #自动补货检查
    url(r'^rewrite_verify/$', 'mana1.rewrite_verify.rewrite_verify'), #审核重写
    url(r'^cleanmc_verify/$', 'mana1.cleanmc_verify.cleanmc_verify'), #审核重写
    
    url(r'^insult_quantou/','mana1.quantou.insult_quantou'), #上下限计算规则中的拳头商品设置
    url(r'^import_quantou/','mana1.quantou.import_quantou'), 
    url(r'^save_quantou/','mana1.quantou.save_quantou'), 
    url(r'^delete_quantou/','mana1.quantou.delete_quantou'), 
    url(r'^deleteData_quantou/','mana1.quantou.deleteData_quantou'),


    url(r'^insult_tianshu/','mana1.tianshu.insult_tianshu'), #上下限计算规则中的配送周期设置
    url(r'^import_tianshu/','mana1.tianshu.import_tianshu'), 
    url(r'^save_tianshu/','mana1.tianshu.save_tianshu'), 
    url(r'^delete_tianshu/','mana1.tianshu.delete_tianshu'), 
    url(r'^deleteData_tianshu/','mana1.tianshu.deleteData_tianshu'),
    
    url(r'^insult_basedisplay/','mana1.basedisplay.insult_basedisplay'), #上下限计算规则中的基本陈列量设置
    url(r'^import_basedisplay/','mana1.basedisplay.import_basedisplay'), 
    url(r'^save_basedisplay/','mana1.basedisplay.save_basedisplay'), 
    url(r'^delete_basedisplay/','mana1.basedisplay.delete_basedisplay'), 
    url(r'^deleteData_basedisplay/','mana1.basedisplay.deleteData_basedisplay'), 
    
    #上下限促销日放大倍数
    url(r'^insult_maxminCuxiaori/','mana1.maxminCuxiaori.insult_maxminCuxiaori'),
    url(r'^import_maxminCuxiaori/','mana1.maxminCuxiaori.import_maxminCuxiaori'),
    url(r'^delete_maxminCuxiaori/','mana1.maxminCuxiaori.delete_maxminCuxiaori'),
    url(r'^save_maxminCuxiaori/','mana1.maxminCuxiaori.save_maxminCuxiaori'),
    url(r'^deleteData_maxminCuxiaori/','mana1.maxminCuxiaori.deleteData_maxminCuxiaori'),
   

)
