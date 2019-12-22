import os, sys

sys.path.insert(0, os.path.join(os.path.abspath('/var/www/html/logisticPython')))



def execfile(filename):
    globals = dict( __file__ = filename )
    exec( open(filename).read(), globals )

activate_this = os.path.join( '/var/www/html/logisticPython', 'venv/bin', 'activate_this.py' )
execfile( activate_this )

print(os.path.dirname(sys.executable))

from interface import app as application
application.debug = True
