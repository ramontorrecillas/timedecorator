import time
from functools import wraps
from collections import defaultdict
from tabulate import tabulate

class timefunctiondecorator(object):
    
    instance=None

    def __new__(cls,*args,**kwargs):
        
        if not cls.instance:
            cls.instance=super().__new__(cls)
            cls.instance._itemsTimeFunction=defaultdict(list)
        return cls.instance

    def __init__(self,ncalls=1):
                
        self.ncalls=ncalls

    def __call__(self,function):

        ncalls=self._ncalls 

        @wraps(function)
        def wrapper(*args,**kwargs):
   
            timesFunction=list()
            timesCpuFunction=list()
                        
            for _ in range(ncalls): 

                initTime=time.monotonic()
                initTimeCpu=time.process_time()

                outcome=function(*args,**kwargs)

                endTimeCpu=time.process_time()
                endTime=time.monotonic()

                timesFunction.append(endTime - initTime)
                timesCpuFunction.append(endTimeCpu - initTimeCpu)

            self._itemsTimeFunction['ncalls'].append(ncalls)
            self._itemsTimeFunction['functionName'].append(function.__name__)
            self._itemsTimeFunction['date'].append(time.strftime('%Y-%m-%d'))
            self._itemsTimeFunction['time'].append(time.strftime('%H:%M:%S'))        
            self._itemsTimeFunction['bestFuncTime'].append(min(timesFunction))
            self._itemsTimeFunction['totFuncTime'].append(sum(timesFunction))
            self._itemsTimeFunction['avgFuncTime'].append(sum(timesFunction) / ncalls)    
            self._itemsTimeFunction['bestCpuTime'].append(min(timesCpuFunction))
            self._itemsTimeFunction['avgCpuTime'].append(sum(timesCpuFunction) / ncalls)
            
            return outcome

        return wrapper

    @property
    def ncalls(self):
        return self._ncalls
    
    @ncalls.setter
    def ncalls(self,value):

        assert isinstance(value,int), '<expected int>'
        assert value > 0, 'Number of iterations should be > 0'
        self._ncalls=value        
    
    def __del__(self):        

        print(tabulate(self._itemsTimeFunction,headers='keys',floatfmt='.8f',stralign='right',tablefmt='plain'))



