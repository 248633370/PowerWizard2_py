#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
    Modbus Client for get status from PowerWizard2.0 Panel by Nechaev Anton
    2015.08.19
    based on client from pymodbus lib
'''
#---------------------------------------------------------------------------# 
# import needed libraries
#---------------------------------------------------------------------------# 
import os
import sys
# Make utf8 default encoding
reload(sys)
sys.setdefaultencoding('utf-8')
import yaml
import argparse
import urllib

#---------------------------------------------------------------------------# 
# state a few constants
#---------------------------------------------------------------------------# 

DEFAULT_SERVER = "zabbix.synmedia.ru"
DEFAULT_PORT = 50280
DEFAULT_URL = 'http://' + DEFAULT_SERVER + ':' + str(DEFAULT_PORT) + '/data.yaml'

DEFAULT_PATH = os.path.dirname(__file__) + '/'
DEFAULT_STORE = '/tmp/pw2py/'              # place to store 
PID_FILE = DEFAULT_STORE + 'pw2c.pid'
LOG_FILE = '/var/log/pw2c.log'

#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig(format='%(asctime)s %(message)s', file=LOG_FILE)
log = logging.getLogger()

class Options(argparse.ArgumentParser):
    ''' argparse subclass  for operating options
        https://docs.python.org/2/library/argparse.html'''
    pass


class Params:
    '''class for manipulate Params ''' 
    def __init__(self, url=DEFAULT_URL):
        self.yamldata = urllib.urlopen(url)

    def load(self):
        #self.params = yaml.load(open(yamldata, 'r'))
        try:
            self.params = yaml.load(self.yamldata.read())
        except IOError:
            log.error('can not open url: Name or service not known')
#        self.params['ParamID']['RegisterValue'] = '6'
#        self.params['ParamID']['Value'] = '9'
                
    def get_title(self):
        ''' return "title" of dictionary'''
        return self.params['ParamID'].keys()

    def get_info(self, param_id):
        self.params_info = {}
        for param in param_id:
            self.params_info[param] = self.params[param]
        return self.params_info

    def get_register(self, param_id):
        ''' Get ReadRegister of param '''
        if self.params[param_id]['ReadRegister']:
            return self.params[param_id]['ReadRegister']
        else:
            return 'No ReadRegister'             # generate error if no read reg

    def get_write_register(self, param_id):
        ''' Get WriteRegister of param '''
        if self.params[param_id]['WriteRegister']:
            return self.params[param_id]['WriteRegister']
        else:
            return 'No WriteRegister'            # generate error if no write reg    

    def get_description(self, param_id):
        return self.params[param_id]['DisplayText']


def options_fill(options):
        ''' function for fill options '''
        options.add_argument('-g','--get-params',
                            type=str,
                            nargs='*',
                            help='get value for enabled parameters or separate <parameter> ')
        options.add_argument('-i','--param-info',
                            type=str,
                            nargs='+',
                            help='information about parameter')
        options.add_argument('-l','--list-params',
                            help='list ',
                            action='store_true')
        options.add_argument('-p','--port',
                            type=str,
                            help='port for connect to daemon')
        options.add_argument('-s','--server',
                            type=str,
                            help='server for connect to daemon')
        options.add_argument('-u','--url',
                            type=str,
                            help='url for connect to daemon')
        options.add_argument('-t','--title',
                            help='list params title',
                            action='store_true')

def print_params_table(param_dict, column, tab=6):
    ''' function for printing table.
        param_id - list/dict of params that will be printed; column - list of needed column from title;
        Current title is: ['ParamID', 'Enable', 'MinVal', 'MaxVal', 'Scale', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'DisplayText', 'Offset', 'NumUsedBits'] 
        additional: 'RegisterValue', 'Value' '''
    ''' Print table header '''
    headerline = ''
    for key in column:
        try:
            wtab = int(param_dict['ParamID'][key])
        except (KeyError,ValueError):
            wtab = tab
        subkey = key[0:wtab]
        sys.stdout.write('|{0}'.format(subkey.ljust(wtab)))
        headerline += '|' + '-' * wtab 
    print
    print headerline
    ''' Print table '''
    for param in sorted(param_dict.keys()):
        if param <> 'ParamID':
            for key in column:
                try:
                    wtab = int(param_dict['ParamID'][key])
                except KeyError:
                    wtab = tab
                subkey = str(param_dict[param][key]).decode('utf-8')[0:wtab]
                sys.stdout.write('|{0}'.format(subkey.ljust(wtab)))
            print
        
def check_pid():
    ''' Check PID for prevent two instances run 
        Function use only connections options like '-g', not use with help and list options '''
    if os.path.isfile(PID_FILE):
        pidfile = open(PID_FILE, 'r+')
        old_pid = pidfile.readline()
        ''' if another instance already run - close this one
            if not - write pid to file '''
        if os.path.exists("/proc/%s" % old_pid):
            sys.exit()
        else:
            pidfile.seek(0)
            pidfile.truncate()
            pidfile.write("%s" % os.getpid())
    else:
        try:
            os.makedirs(DEFAULT_STORE)
        except OSError:
            pass
        pidfile = open(PID_FILE, 'w')
        pidfile.write("%s" % os.getpid())
    pidfile.close()

# For not to work as library
if __name__ == "__main__":
    ''' Read script options '''
    options = Options()
    options_fill(options)
    arguments = options.parse_args()

    ''' Load conf to dictionary '''
    try:
        config = Params()
        config.load()
    except IOError:
        log.error('stream IOError')
        sys.exit()

    ''' List some info to stdout '''
    ''' {'ParamID', 'Enable', 'MinVal', 'MaxVal', 'Scale', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'DisplayText', 'Offset', 'NumUsedBits'} '''
    if arguments.list_params:
        print_params_table(config.params, ['ParamID', 'DisplayText', 'TotalBytes', 'WriteRegister', 'ReadRegister' ])
        sys.exit()
    elif arguments.title:
        ''' get title '''
        print config.get_title()
        sys.exit()        
    elif arguments.param_info:
        info_params = {}
        info_params['ParamID'] = config.params['ParamID']
        for param in arguments.param_info:
            info_params[param] = config.params[param]
        print_params_table(info_params, ['ParamID', 'DisplayText', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'Scale', 'Offset', 'MinVal', 'MaxVal' ])
        sys.exit()
    elif arguments.get_params is not None:
        ''' If used "-g" option, discard all other options '''
        if len(arguments.get_params) == 0:
            get_params = {}
            get_params['ParamID'] = config.params['ParamID']
            for param in sorted(arguments.get_params):
                arguments.get_params.append(param)
    elif len(sys.argv) == 1:
        ''' Wihtout scipt option(s) - get help '''
        options.print_help()
        sys.exit()

    ''' check pid befor main algorithm '''
    check_pid()

    print_params_table(config.params, ['ParamID', 'RegisterValue', 'Value', 'DisplayText', 'ReadRegister' ])
