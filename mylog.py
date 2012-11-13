import logging

def log(request):
    logging.basicConfig(filename='d:/vcms/lib/py/mana1/mylog.log',level=logging.INFO)
    logging.info(request)

