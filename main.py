
import serial
import thread

import nbp
import time

from collections import deque
readBufferQueue = deque([])
SLIP_END = 0xc0        # declared in hexa Frame End

SLIP_ESC = 0xdb	#Frame Escape
SLIP_ESC_END = 0xdc #transposed Frame End
SLIP_ESC_ESC = 0xdd #franspose Frame Escape
def connectToSerialPort():


    """ This function connect and configure the serial port. Then returns file descriptor
    :return serialFD: file descriptor
    """
    #serialFD = serial.Serial(port='/dev/ttyUSB0' )
    serialFD =serial.Serial(port = '/dev/ttyUSB0', baudrate = 9600, bytesize = 8, parity = 'N',  stopbits=1, xonxoff=False, rtscts=False)
    #serialFD = serial.Serial(port='/dev/ttyUSB1')
    # port='/dev/ttyUSB0'- port to open
    # baudrate=115200  - baud rate to communicate with the port
    # bytesize=8           - size of a byte
    # parity='N'           - no parity
    # stopbits=1           - 1 stop bit
    # xonxoff=False           - no software handshakes
    # rtscts=False           - no hardware handshakes
    return serialFD


def read_from_serial_port(thead_name,delay,serial_port):
    while True:
        data = serial_port.read()
        time.sleep(delay)
        print(data)


def write_serial_port(thead_name, delay,serial_port):
    while True:
        byteArray = [255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 240, 13, 241, 38, 0, 0, 0, 0, 0, 0, 0, 0, 47,
                     47, 47, 47, ord('?'), 13]
        writeToSerialPort(byteArray,serial_port)
        time.sleep(delay)
def writeToSerialPort( byteArray,serial_port):
    """
     This function accept a byte array and write it to the serial port

    :param serialFD: opened serial port file descriptor
    :param byteArray: accepted a byte array
    :return:
    """
    encodedSLIPBytes = nbp.encodeToSLIP(byteArray)

    byteString = ''.join(chr(b) for b in encodedSLIPBytes) #convert byte list to a string
    print(byteString)
    serial_port.write(byteString)

def main():
    import pdb;

    serial_port =  connectToSerialPort()
    try:
        thread.start_new_thread(write_serial_port, ("write", 20,serial_port))
        #pdb.set_trace()
        thread.start_new_thread(read_from_serial_port, ("read",0.1,serial_port))
        pdb.set_trace()
    except:
        print("Error: unable to start thread")

if __name__=="__main__":

    main()




