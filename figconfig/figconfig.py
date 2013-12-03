__author__ = 'TalbotJ'

import json


def get_config(module):

    return _config[module]


# I think this code is only run the first time the module is loaded, which is
# probably good for us...
# TODO: find a proper way to store/find the config file
f = open(r"C:\Users\talbotj\PycharmProjects\Figdoc\figconfig\testconfig.json", "r")
_config = json.loads(f.read())
f.close()

if __name__ == '__main__':

    c = get_config('emailing')
    print(c)
    print(c["server"])
    print(c["sender"])
