
#just add this as an attribute to scene. like self.scene.sched
class Scheduler(object):
    def __init__(self, timevar):
        self.sched = {}
        self.timevar = timevar
        self.lasttime = 0
        
    def add(self, delay, func, args = None):
        if self.timevar+delay in self.sched:
            self.sched[self.timevar+delay].append([func, args])
        else:
            self.sched[self.timevar+delay] = [[func, args],]
        
    def execute(self):
        for i in range(self.lasttime, self.timevar):
            if i in self.sched:
                for func, args in self.sched[i]:
                    if args == None:
                        func()
                    else:
                        func(*args)
        
        self.remove_outdated()
        
    def set_time(self, t):
        self.lasttime, self.timevar = self.timevar, t    
    
    def search_next(self, func, args):
        for i, v in self.sched.iteritems():
            if [func, args] in v:
                return i
            
    def time_till(self, func, args):
        x = self.search_next(func, args)
        if x is not None:
            return x - self.timevar
        
    #remove a certain entry
    def remove_next(self, func, args):
        for i, v in self.sched.iteritems():
            if [func, args] in v:
                v.remove([func, args])
                break
                
    def remove_outdated(self):
        for i in self.sched.keys():
            if i < self.lasttime:
                del self.sched[i]
