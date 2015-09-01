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

from getopt import getopt
from pymodbus.constants import Defaults
from twisted.internet import reactor, protocol

#---------------------------------------------------------------------------# 
# choose the requested modbus protocol
#---------------------------------------------------------------------------# 
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

DATA_FILE = 'Params_wDataTypes.yaml'        # file with params config
DEFAULT_STORE = '/tmp/pw2py/'              # place to store regs status
PID_FILE = DEFAULT_STORE + 'pw2py.pid'

#---------------------------------------------------------------------------# 
# helper method to test deferred callbacks
#---------------------------------------------------------------------------# 
def dassert(deferred, callback):
    def _assertor(value): assert(value)
    deferred.addCallback(lambda r: _assertor(callback(r)))
    deferred.addErrback(lambda  _: _assertor(False))


class Client(ModbusSerialClient):
    ''' Class for connection and request to PW console  '''
    def __init__(self, method=DEFAULT_SERIAL_METHOD, stopbits=DEFAULT_SERIAL_STOPBITS, bytesize=DEFAULT_SERIAL_BYTESIZE, parity=DEFAULT_SERIAL_PARITY, port=DEFAULT_SERIAL_PORT):
        pass

    def request_regs(self, regs=DEFAULT_REGS):
        '''read_holding_registers'''
        return self.read_holding_registers(REG, DEFAULT_REGS[1])


class Options:
    ''' class for script options ''' 
    def __init__(self):
        pass

    def args(self):
        for args in sys.argv:
            if len(sys.argv) == 0 :
                log.error('No args')
            else:
                return 

    def usage_info(self):
        ''' usage info'''
        print ' \n\
        pw2.py [options] <parameter> ... [parameter] \n\
        parametr - query PW parametr \n\
    Options: \n\
        -a, --list - list all available parameters \n\
        -l, --list-enable - list all enabled parameters \n\
        '
        sys.exit()


class Params:
    '''class for manipulate Params ''' 
    def __init__(self):
        self.params = {}

    def  load(self, yamlfile=DATA_FILE):
        self.params = yaml.load(open(yamlfile, 'r'))
        
    def get_header(self):
        ''' return "header" of dictionary'''
        return self.params['ParamID'].keys()

    def get_register(self, param_id ):
        if self.params[param_id]['ReadRegister']:
            return self.params[param_id]['ReadRegister']
        else:
            return 'No ReadRegister'                                  #generate error if no read reg

    def get_write_register(self, param_id ):
        if self.params[param_id]['WriteRegister']:
            return self.params[param_id]['WriteRegister']
        else:
            return 'No WriteRegister'                                  #generate error if no write reg    

    def get_description(self, param_id ):
        return self.params[param_id]['DisplayText']
       

def main():
##    rr = client.read_holding_registers(201,1)
    ''' Load conf to dictionary '''
    config = Params()
    config.load()

    print config.get_header()
#   test get params
    print config.get_register(param_id='ParamID')
    print config.get_description(param_id='ParamID')
    print config.get_register(param_id='ENG_COOL_TMP')
    print config.get_description(param_id='ENG_COOL_TMP')


# For not to work as library
if __name__ == "__main__":
    main()

