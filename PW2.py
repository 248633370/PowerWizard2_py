#!/usr/bin/env python
''' 
    Modbus Client for get status from PowerWizard2.0 Panel by Nechaev Anton
    2015.08.19
    based on client from pymodbus lib
'''
#---------------------------------------------------------------------------# 
# import needed libraries
#---------------------------------------------------------------------------# 
import sys
# Make utf8 default encoding
reload(sys)
sys.setdefaultencoding('utf-8')

cfrom getopt import getopt
from pymodbus.constants import Defaults
from twisted.internet import reactor, protocol

#---------------------------------------------------------------------------# 
# choose the requested modbus protocol
#---------------------------------------------------------------------------# 
#from pymodbus.client.async import ModbusClientProtocol as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
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
DATA_FILE = 'Params_wDataTypes.yaml'
#DEFAULT_SERIAL_PORT  = "/dev/ttyr00"       # default port for npreals
DEFAULT_SERIAL_PORT  = "/dev/ttyS33"        # symlink to /dev/ttyr00
DEFAULT_REGS  = (201, 1)
DEFAULT_UNIT='0x01'
DEFAULT_REGS_STORE='/tmp/pw2/'              # place to hold regs status
CLIENT_DELAY = 1

#---------------------------------------------------------------------------# 
# helper method to test deferred callbacks
#---------------------------------------------------------------------------# 
def dassert(deferred, callback):
    def _assertor(value): assert(value)
    deferred.addCallback(lambda r: _assertor(callback(r)))
    deferred.addErrback(lambda  _: _assertor(False))


class Connect(ModbusClient):
    ''' Class for connection and request to PW console  '''
    SERIAL_PORT = DEFAULT_SERIAL_PORT
    UNIT = DEFAULT_UNIT
    REGS = DEFAULT_REGS
    def __init__(self):
        pass

    def RequestRegs(self, SERIAL_PORT=SERIAL_PORT, UNIT=UNIT, REGS=REGS):
        pass


class Options:
    ''' class for script options ''' 
    def Args(self):
        for args in sys.argv:
            if len(sys.argv) == 0:
                log.error('No args')
                
    def UsageInfo(self):
        ''' usage info'''
        return ' \n\
        pw2.py [options] <parameter> ... [parameter] \n\
        parametr - query PW parametr \n\
    Options: \n\
        -l, --list - list all available parameters \n\
        '


class Params:
    '''class for manipulate Params ''' 
    def __init__(self):
        pass

    def  load(self, yamfile):
        self.params = yaml.load(open(yamlfile, 'r'))
        close(yamlfile)

    def GetRegs(self):
        if self.parms[param_id]['ReadRegistr'] == 0:
            print 'No ReadRegistr'                                  #generate error if no read reg
        else:
            return self.parms[param_id]['ReadRegistr']


def main():
##    rr = client.read_holding_registers(201,1)
    start = Options()
    print start.Read()
    

# For not to work as library
if __name__ == "__main__":
    main()

