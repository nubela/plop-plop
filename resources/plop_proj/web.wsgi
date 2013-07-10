import sys, os

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cwd)
activate_this = os.path.join(cwd, "v_env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from web.plop import app
application = app