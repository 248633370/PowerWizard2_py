#!/usr/bin/env python
''' 
    Modbus Client for get status from PowerWizard2.0 Panel by Nechaev Anton
    2015.08.19
    based on client from pymodbus lib
'''
#---------------------------------------------------------------------------# 
# import needed libraries
#---------------------------------------------------------------------------# 
from twisted.internet import reactor, protocol
from pymodbus.constants import Defaults
# Make utf8 default encoding
reload(sys)
sys.setdefaultencoding('utf-8')

#---------------------------------------------------------------------------# 
# choose the requested modbus protocol
#---------------------------------------------------------------------------# 
#from pymodbus.client.async import ModbusClientProtocol as ModbusClient
from pymodbus.client.async import ModbusSerialClient as ModbusClient
#from pymodbus.client.async import ModbusUdpClientProtocol as ModbusClient

#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# state a few constants
#---------------------------------------------------------------------------# 
DATA_FILE = 'Params_wDataTypes.yaml'
#DEFAULT_SERIAL_PORT  = "/dev/ttyr00"       # default port for npreals
DEFAULT_SERIAL_PORT  = "/dev/ttyS33"        # symlink to /dev/ttyr00
DEFAULT_REGS  = (201, 1)
DEFAULT_UNIT='0x01'
CLIENT_DELAY = 1

#---------------------------------------------------------------------------# 
# helper method to test deferred callbacks
#---------------------------------------------------------------------------# 
def dassert(deferred, callback):
    def _assertor(value): assert(value)
    deferred.addCallback(lambda r: _assertor(callback(r)))
    deferred.addErrback(lambda  _: _assertor(False))

# class for init connection and request regs
class Connect(ModbusClient):
    ''' Class for connection to PW console  '''
    SERIAL_PORT = DEFAULT_SERIAL_PORT
    UNIT = DEFAULT_UNIT
    REGS = DEFAULT_REGS
    def __init__(self):
        pass

    def ReadRegs(self, SERIALPORT_SERIAL_PORT, UNIT=UNIT, REGS=REGS):
        pass
    def 


class Options:
    ''' class for input options ''' 
    def


class Params:
    '''class for manipulate Params ''' 
    def __init__(self):
        pass

    def  load(self, yamfile):
        self.params = yaml.load(open(yamlfile, 'r'))
        close(yamlfile)

    def GetRegs(self)
        if self.parms['ReadRegistr'] == 0:
            print 'No ReadRegistr'
        else:
            return 


def main ()
##    rr = client.read_holding_registers(201,1)

# For not to work as library
if __name__ == "__main__":
    main()

