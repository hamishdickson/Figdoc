__author__ = 'TalbotJ'

import json
import os

# only need to do this once, then it's in memory
# Note: the implication of this is you have to restart to change config
_got_config = False


def get_config(module):
    return _config[module]

# I think this code is only run the first time the module is loaded, which is
# probably good for us...
# TODO: find a proper way to store/find the config file
usr = os.getenv('USERPROFILE')

conf_file = os.path.join(usr, 'testconfig.json')

try:
    f = open(conf_file, "r")
except IOError as e:
    print "Can't open config file"
else:
    _config = json.loads(f.read())
    f.close()
    _got_config = True


if __name__ == '__main__':
    c = get_config('grabber')
    print(c)
    print(c["server"])
    print(c["sender"])