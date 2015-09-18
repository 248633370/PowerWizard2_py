#!/usr/bin/env python
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
DEFAULT_SERIAL_BAUDRATE = 9600
DEFAULT_SERIAL_TIMEOUT = 1
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
        options.add_argument('parameter',
                            type=str,
                            nargs='*',
                            help='query PW parameter')
        options.add_argument('-a','--list-all',
                            help='list all available parameters',
                            action='store_true')
        options.add_argument('-g','--get-enable',
                            help='get value for enabled parameters, this options discard <parameter> ',
                            action='store_true')
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
def print_params_table(param_id, column):
    ''' function for printing table.
        param_id - list/dict of params that wil be printed; column - list of needed column from title;
        Curent title is: ['MaxVal', 'Enable', 'MinVal', 'TotalBytes', 'WriteRegister', 'ReadRegister', 'DisplayText', 'Offset', 'NumUsedBits', 'ParamID', 'Scale'] 
        and RegisterValue '''
    num_params = len(param_id)
    num_columns = len(column)

    print '| {0} | {1}'.format(column[0][0].ljust(19), column[1][0])
    print '| {0} | {1}'.format(''.ljust(19,'-'), ''.ljust(60,'-'))
    for row1,row2 in zip(column[0],column[1]):
        print '| {0} | {1}'.format(row1.ljust(19), row2)
        
def main():
    ''' Read script options '''
    options = Options()
    options_fill(options)
    arguments = options.parse_args()

    ''' Load conf to dictionary '''
    config = Params()
    config.load()

    ''' List some info to stdout '''
    if arguments.list_all:
        print 'List all available parameters'
        print '| {0} | {1}'.format('ParamID'.ljust(19), 'DisplayText')
        print '| {0} | {1}'.format(''.ljust(19,'-'), ''.ljust(60,'-'))
        for param in sorted(config.params.keys()):
            print '| {0} | {1}'.format(config.params[param]['ParamID'].ljust(19), config.params[param]['DisplayText'])
        sys.exit()
    elif arguments.list_enable:
        print 'List only enabled parameters'
        print '| {0} | {1}'.format('ParamID'.ljust(19), 'DisplayText')
        print '| {0} | {1}'.format(''.ljust(19,'-'), ''.ljust(60,'-'))
        for param in sorted(config.enabled_params.keys()):
            print '| {0} | {1}'.format(config.enabled_params[param]['ParamID'].ljust(19), config.enabled_params[param]['DisplayText'])
        sys.exit()
    elif arguments.title:
        print config.get_title()
        sys.exit()        
    elif arguments.get_enable:
        ''' If used "-g" option, discard all other options. 
            Fill arguments.parameter with all parameters enabled '''
        arguments.parameter = []
        for param in sorted(config.enabled_params.keys()):
            arguments.parameter.append(param)
    elif arguments.param_info:
        print config.get_info(arguments.param_info)
        sys.exit()
    elif len(sys.argv) == 1:
        ''' Wihtout scipt option(s) - get help '''
        options.print_help()
        sys.exit()

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
    for param in arguments.parameter:
#        print client.read_holding_registers(int(config.get_register(param))-1, 1, unit=DEFAULT_UNIT)               # may nedd for debug acq register value
        try:
            config.enabled_params[param]['RegisterValue'] = client.read_holding_registers(int(config.get_register(param))-1, 1, unit=DEFAULT_UNIT).registers[0]
        except AttributeError:
            ''' Acquisition Error'''
            config.enabled_params[param]['RegisterValue'] = 'acq_err'

    for param  in sorted(config.enabled_params.keys()):
        print '|{0}|{1}|{2}'.format(config.enabled_params[param]['ParamID'].ljust(19), str(config.enabled_params[param]['RegisterValue']).center(7), config.enabled_params[param]['DisplayText'])
    ''' Close client connection '''
    client.close()

    '''test get params
    print config.get_register(param_id='ParamID')
    print config.get_description(param_id='ParamID')
    print config.get_register(param_id='ENG_COOL_TMP')
    print config.get_description(param_id='ENG_COOL_TMP')


    '''

# For not to work as library
if __name__ == "__main__":
    main()

