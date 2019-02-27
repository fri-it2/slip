#source: http://recolog.blogspot.com/2012/10/serial-line-internet-protocol-slip.html
import serial

from collections import deque
readBufferQueue = deque([])
SLIP_END = 0xc0        # declared in hexa Frame End

SLIP_ESC = 0xdb	#Frame Escape
SLIP_ESC_END = 0xdc #transposed Frame End
SLIP_ESC_ESC = 0xdd #franspose Frame Escape

MTU = 200

def decodeFromSLIP(serialFD):

    """this function uses getSerialByte() function to get SLIP encoded bytes from
    the serial port and return a decoded byte list
    
    :param serialFD: opened serial port
    :return: byte at the time
    """

    dataBuffer = []
    while 1:
        serialByte= getSerialByte(serialFD)
        if serialByte is None:
            return -1
        elif serialByte == SLIP_END:
            if len(dataBuffer) > 0:
                return dataBuffer
        elif serialByte == SLIP_ESC:
            if serialByte is None:
                return -1

            elif serialByte == SLIP_ESC_ESC:
                dataBuffer.append(SLIP_ESC)
            elif serialByte == SLIP_ESC_END:
                dataBuffer.append(SLIP_ESC)
            else:
                print("Error protocol")
        else:
            dataBuffer.append(serialByte)
    return

def getSerialByte(SerialFD):

    """This function read byte chuncks from the serial port and return one byte at a time

    :param SerialFD: file descriptor of opened serial port
    :return: newByte: 1 byte
    """
    if len(readBufferQueue) ==0:
        i=0
        while len(readBufferQueue) < MTU:
            newByte = ord(SerialFD.read())

            #newByte = SerialFD.read()
            readBufferQueue.append(newByte)
        newByte = readBufferQueue.popleft()
        return newByte
    else:
         newByte = readBufferQueue.popleft()
         return newByte

def encodeToSLIP(byteList):
    """This function takes a byte list, encode it in SLIP protocol and return the encoded byte list

    :param byteList: bytelist
    :return: tempSLIPBuffer: SLIP encoded byte
    """
    tempSLIPBuffer = []
    tempSLIPBuffer.append(SLIP_END)
    for i in byteList:
        if i == SLIP_END:
            tempSLIPBuffer.append(SLIP_ESC_END)
        elif i == SLIP_ESC:
            tempSLIPBuffer.append(SLIP_ESC_ESC)
        else:
            tempSLIPBuffer.append(i)
    tempSLIPBuffer.append(SLIP_END)
    return tempSLIPBuffer
