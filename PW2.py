#!/usr/bin/env python
''' 
    Modbus Client for get status from PowerWizard2.0 Panel by Nechaev Anton
    2015.08.19
    based on async-client from pymodbus lib
'''
#---------------------------------------------------------------------------# 
# import needed libraries
#---------------------------------------------------------------------------# 
from twisted.internet import reactor, protocol
from pymodbus.constants import Defaults
# Делаем UTF-8 стандлратной кодировкой
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
#SERIAL_PORT  = "/dev/ttyr00"       # default port for npreals
SERIAL_PORT  = "/dev/ttyS33"        # symlink to /dev/ttyr00
#REGS  = (201, 1, 1)
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

class connection(ModbusClient):
    def __init__(self):
        pass

# class for manipulate Params
class Params(self):
    def __init__(self):
        pass

def main ()
##    rr = client.read_holding_registers(201,1)


if __name__ == "__main__":
    main()

