import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


from excpetions.Error import Error


class TimeWindowExceeded(Error):
   """Raised when the input value is too small"""
   pass