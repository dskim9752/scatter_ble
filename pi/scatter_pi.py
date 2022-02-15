import sys
import glob
import serial
import requests


BAUD = 9600
URL = ""    #need URL
item = "starbucks"
count = 0


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system

    https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(2,256)]   #Except com1 (Communication port)
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port,BAUD)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


ser = serial_ports()
print(ser[0], end=' ')
s = serial.Serial(ser[0], BAUD)
print('start')


while True:
    data = s.readline()
    if 'DISCS' in str(data):
        while 'DISCE' not in str(data):
            data = s.readline()
            if 'DISCS' not in str(data) and str(data).find(item) != -1:
                count += 1
            if 'DISCS' not in str(data) and str(data).find("Scatter") != -1: #demo
                count += 1
        print(f"{item} : {count}", end='    ')
        datas = {    # item , count
            'item' : item,
            'count' : count
        }
        #send to server
        try:
            response = requests.post(URL, data = datas)
            print('===========    send')
        except Exception as e:
            print("===========    fail : ",e)
        count = 0
s.close()


