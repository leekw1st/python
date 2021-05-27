import datetime

def _DEBUG_LOG_(function, log):
    time = datetime.datetime.now()
    date=time.strftime('%Y-%m-%d')
    time=time.strftime('%H:%M:%S')

    print('[',date,' ',time,']','[',function,']','[',log,']', sep='')

    dir = 'C:\\Source\\python\\coinpot\\log\\coinpot.log_'+date

    f = open(dir, "a", encoding='utf8')

    log = '['+date+' '+time+']'+'['+function+']'+'['+log+']'+'\n'
    
    f.write(log)

if __name__ == "__main__":
    _DEBUG_LOG_("main", "Hello World~~")