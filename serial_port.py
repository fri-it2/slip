#source: http://recolog.blogspot.com/2012/10/serial-line-internet-protocol-slip.html
import serial
import nbp

def connectToSerialPort():


    """ This function connect and configure the serial port. Then returns file descriptor
    :return serialFD: file descriptor
    """
    serialFD =serial.Serial(port = '/dev/ttyUSB1', baudrate = 9600, bytesize = 8, parity = 'N',  stopbits=1, xonxoff=False, rtscts=False)
    #serialFD = serial.Serial(port='/dev/ttyUSB1')
    # port='/dev/ttyUSB0'- port to open
    # baudrate=115200  - baud rate to communicate with the port
    # bytesize=8           - size of a byte
    # parity='N'           - no parity
    # stopbits=1           - 1 stop bit
    # xonxoff=False           - no software handshakes
    # rtscts=False           - no hardware handshakes
    return serialFD


def readFromSerialPort(serialFD):


    """
    This function reads from the serial port and return a byte array
    :param serialFD: file descriptor of opened serial port
    :return: byteArray
    """
    byteArray = nbp.decodeFromSLIP(serialFD)
    if byteArray is None:
        print("readFromSerialPort(serialFD): Error")
        return -1
    else:
        return byteArray


def writeToSerialPort(serialFD, byteArray):
    """
     This function accept a byte array and write it to the serial port

    :param serialFD: opened serial port file descriptor
    :param byteArray: accepted a byte array
    :return:
    """
    encodedSLIPBytes = nbp.encodeToSLIP(byteArray)

    byteString = ''.join(chr(b) for b in encodedSLIPBytes) #convert byte list to a string
    print(byteString)
    serialFD.write(byteString)

def disconnectFromSerialPort(SerialFD):
    SerialFD.close()
    return

serialFD=connectToSerialPort()
byte=readFromSerialPort(serialFD)

byteArray=[255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 240, 13, 241, 38, 0, 0, 0, 0, 0, 0, 0, 0, 106, 101, 32, 102, 104, 111, 32, 100, 111, 109, 97, 13]
writeToSerialPort(serialFD, byteArray)
