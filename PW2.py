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

from pymodbus.constants import Defaults
# need for async TCP client
#from twisted.internet import reactor, protocol

#---------------------------------------------------------------------------# 
# choose the requested modbus protocol
#---------------------------------------------------------------------------#
'''First step - only sync serial connection'''
#from pymodbus.client.async import ModbusClientProtocol as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusSerialClient
#from pymodbus.client.async import ModbusUdpClientProtocol as ModbusClient

#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
#log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# state a few constants
#---------------------------------------------------------------------------# 
DEFAULT_SERIAL_METHOD = "rtu"
DEFAULT_SERIAL_STOPBITS = 1
DEFAULT_SERIAL_BYTESIZE = 8
DEFAULT_SERIAL_PARITY = "E"
DEFAULT_SERIAL_BAUDRATE = 19200
DEFAULT_SERIAL_TIMEOUT = 0.3
DEFAULT_SERIAL_PORT = "/dev/ttyr00"        # default port for npreals
#DEFAULT_SERIAL_PORT = "/dev/ttyS33"        # symlink to /dev/ttyr00

#DEFAULT_TCP_SERVER = "172.16.156.69"
#DEFAULT_TCP_PORT = 590
#DEFAULT_TCP_ = 

DEFAULT_REGS  = 201
DEFAULT_UNIT = 0x01

DEFAULT_PATH = os.path.dirname(__file__) + '/'
DATA_FILE = DEFAULT_PATH + 'Params_wDataTypes.yaml'        # file with params config
DEFAULT_STORE = '/tmp/pw2py/'              # place to store regs status
PID_FILE = DEFAULT_STORE + 'pw2py.pid'
LOG_FILE = '/var/log/pw2py.log'

class Options(argparse.ArgumentParser):
    ''' argparse subclass  for operating options
        https://docs.python.org/2/library/argparse.html'''
    pass


class Params:
    '''class for manipulate Params ''' 
    def __init__(self):
        pass

    def load(self, yamlfile=DATA_FILE):
        self.params = yaml.load(open(yamlfile, 'r'))
        self.params['ParamID']['RegisterValue'] = '6'
        self.params['ParamID']['Value'] = '9'
        self.enabled_params = {}
        for param in self.params.keys():
            if self.params[param]['Enable'] == '1':
                self.enabled_params[param] = self.params[param]
        
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
#        options.add_argument('parameter',
#                            type=str,
#                            nargs='*',
#                            help='query PW parameter')
        options.add_argument('-a','--list-all',
                            help='list all available parameters',
                            action='store_true')
        options.add_argument('-g','--get-params',
                            type=str,
                            nargs='*',
                            help='get value for enabled parameters or separate <parameter> ')
        options.add_argument('-i','--param-info',
                            type=str,
                            nargs='+',
                            help='information about parameter')
        options.add_argument('-l','--list-enable',
                            help='list only enabled parameters',
                            action='store_true')
        options.add_argument('-p','--port',
                            type=str,
                            help='port for connect to panel')
        options.add_argument('-t','--title',
                            help='list params title',
                            action='store_true')

def print_params_table(param_id, column, tab=6):
    ''' function for printing table.
        param_id - list/dict of params that wil be printed; column - list of needed column from title;
        Curent title is: ['ParamID', 'Enable', 'MinVal', 'MaxVal', 'Scale', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'DisplayText', 'Offset', 'NumUsedBits'] 
        additionaly: 'RegisterValue', 'Value' '''
    ''' Print table header '''
    for key in column:
        try:
            wtab = int(config.params['ParamID'][key])
        except KeyError:
            wtab = tab
        subkey = key[0:wtab]
        sys.stdout.write('|{0}'.format(subkey.ljust(wtab)))
    print
    for key in column:
        try:
            wtab = int(config.params['ParamID'][key])
        except KeyError:
            wtab = tab
        sys.stdout.write('|{0}'.format(''.ljust(wtab,'-')))
    print
    ''' Print table '''
    for param in sorted(param_id):
        for key in column:
            try:
                wtab = int(config.params['ParamID'][key])
            except KeyError:
                wtab = tab
            subkey = str(config.params[param][key]).decode('utf-8')[0:wtab]
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
    config = Params()
    config.load()

    ''' List some info to stdout '''
    ''' {'ParamID', 'Enable', 'MinVal', 'MaxVal', 'Scale', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'DisplayText', 'Offset', 'NumUsedBits'} '''
    if arguments.list_all:
        print_params_table(config.params.keys(), ['ParamID', 'MinVal', 'MaxVal', 'Scale', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'DisplayText' ])
        sys.exit()
    elif arguments.list_enable:
        print_params_table(config.enabled_params.keys(), ['ParamID', 'DisplayText', 'TotalBytes', 'WriteRegister', 'ReadRegister' ])
        sys.exit()
    elif arguments.title:
        ''' get title '''
        print config.get_title()
        sys.exit()        
    elif arguments.param_info:
        ''' Information for separate params '''
        print_params_table(arguments.param_info, ['ParamID', 'DisplayText', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'Scale', 'Offset', 'MinVal', 'MaxVal' ])
        sys.exit()
    elif arguments.get_params is not None:
        ''' If used "-g" option, discard all other options '''
        if len(arguments.get_params) == 0:
            for param in sorted(config.enabled_params.keys()):
                arguments.get_params.append(param)
    elif len(sys.argv) == 1:
        ''' Wihtout scipt option(s) - get help '''
        options.print_help()
        sys.exit()

    ''' check pid befor main algorithm '''
    check_pid()

    ''' Check override default arguments value '''
    if arguments.port:
        SERIAL_PORT = arguments.port
    else:
        SERIAL_PORT = DEFAULT_SERIAL_PORT

    ''' main algorithm
        init connection conf and connect'''
    client = ModbusSerialClient( method=DEFAULT_SERIAL_METHOD, 
                        port=SERIAL_PORT, 
                        stopbits=DEFAULT_SERIAL_STOPBITS,
                        bytesize=DEFAULT_SERIAL_BYTESIZE,
                        parity=DEFAULT_SERIAL_PARITY,
                        baudrate = DEFAULT_SERIAL_BAUDRATE,
                        timeout = DEFAULT_SERIAL_TIMEOUT )
    client.connect()
    ''' get params and regs '''
    for param in arguments.get_params:
        try:
            config.params[param]['RegisterValue']  = client.read_holding_registers(int(config.get_register(param))-1, 1, unit=DEFAULT_UNIT).registers[0]
            scale = float(config.params[param]['Scale'].replace(',','.'))
            offset = int(config.params[param]['Offset'])
            min_val = float(config.params[param]['MinVal'].replace(',','.'))
            max_val = float(config.params[param]['MaxVal'].replace(',','.'))
            config.params[param]['Value'] = config.params[param]['RegisterValue'] * scale + offset
            if (config.params[param]['Value'] > max_val) or (config.params[param]['Value'] < min_val):
                ''' Out of range '''
                config.params[param]['RegisterValue'] = 'ran_er'
                config.params[param]['Value'] = 0
        except AttributeError:
            ''' Acquisition Error'''
            config.params[param]['RegisterValue'] = 'acq_er'
            config.params[param]['Value'] = 0
        except (OSError):
            ''' Port Error'''
            config.params[param]['RegisterValue'] = 'prt_er'
            config.params[param]['Value'] = 0

    print_params_table(arguments.get_params, ['ParamID', 'RegisterValue', 'Value', 'DisplayText', 'ReadRegister' ])

    ''' Close client connection '''
    client.close()

    '''test get params
    print config.get_register(param_id='ParamID')
    print config.get_description(param_id='ParamID')
    print config.get_register(param_id='ENG_COOL_TMP')
    print config.get_description(param_id='ENG_COOL_TMP')
    '''

