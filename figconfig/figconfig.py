__author__ = 'TalbotJ'


import json
import os


def get_config(module):

    return _config[module]


# I think this code is only run the first time the module is loaded, which is
# probably good for us...
# TODO: find a proper way to store/find the config file
usr = os.getenv('USERPROFILE')
conf_file = os.path.join(usr, 'Documents\\Github\\Figdoc\\configuration\\testconfig.json')

f = open(conf_file, "r")
_config = json.loads(f.read())
f.close()

if __name__ == '__main__':

    c = get_config('emailing')
    print(c)
    print(c["server"])
    print(c["sender"])