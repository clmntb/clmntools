DEBUG = 3
WARNING = 2
ERROR = 1
LOG_LEVEL = DEBUG

class Colors():
    def __init__(self):
        init(autoreset=True)
        self.HEADER = Fore.MAGENTA
        self.OK = Fore.BLUE
        self.DBG = Fore.GREEN
        self.WARNING = Fore.YELLOW
        self.ERROR = Fore.RED
        
    def color(self,s,c):
        if c == DEBUG:
            return self.DBG+"[DEBUG] "+s
        if c == WARNING:
            return self.WARNING+"[WARNING] "+s
        if c == ERROR:
            return self.ERROR+"[ERROR] "+s
        else:
            return s
        
class Debuger():
    def __init__(self,debug=LOG_LEVEL):
        self.count = 0
        self.max = 10
        self.signal = None
        self.dbg_level = debug
        self.colors = Colors()
        self.handles = []
    
    def setLevel(self,level):
        self.dbg_level = level
        if level == 3:
            self.log('Debug level changed to DEBUG',DEBUG)
    
    def handler(self,signum, frame):
        print 'Signal handler called with signal', signum
        self.count += 1
        self.log('Signal called %d time, %d remaining before quit' % (self.count, self.max-self.count),DEBUG)
        for handle in self.handles:
            handle.__call__()        
        if self.count == self.max:
            print self.log('Now Quitting...',DEBUG)
            sys.exit()

    def debug(self):
        self.object = object
        self.signal = signal.signal(signal.SIGINT, self.handler)
        self.log("The debuger is started, press CTRL+C to see traces",DEBUG)

    def add_handle(self,h):
        if not hasattr(h, '__call__'):
            self.log("The handle must be a function !", ERROR)
        else:
            self.handles.append(h)
            self.log("The handle has been successfuly registered",DEBUG)
        
    def log(self,log,level=DEBUG):
        if level <= self.dbg_level:
            print self.colors.color(log,level)
