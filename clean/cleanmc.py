#coding:utf8
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import confsql,datetime,memcache
from django.utils import simplejson
import writemc
from mylog import log
confsql=confsql.Confsql()
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
def cleanmc(request,sqlstr=""):
    if request.method=='POST':
        pass
    else:
        t=get_template('mana1/cleanmc.html')
        result=""
        html=t.render(Context({'result':result}))
        return HttpResponse(html)

