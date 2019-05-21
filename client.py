# telnet program example
import socket, select, string, sys
import mraa
import time
import csv
from threading import Thread # thread

LED_GPIO = 5                   # The LED pin
BUTTON_GPIO = 6                # The button GPIO
MIC_GPIO = 0
led = mraa.Pwm(LED_GPIO)      # Get the LED pin object
btn = mraa.Gpio(BUTTON_GPIO)   # Get the button pin object
btn.dir(mraa.DIR_IN)           # Set the direction as input
mic = mraa.Aio(MIC_GPIO)

led.period_us(5000)        # Set the period as 5000 us or 5ms

led.enable(True)           # enable PWM
value = 0

delta = 0.05               # Used to manipulate duty cycle of the pulse
msg = "0"
def enviar(s):
    while True:
        s.send("%s"%msg)
        time.sleep(0.01)

led.write(0)


#main function
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    t = Thread(target=enviar, args=(s,))
    t.start()
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Start sending messages'

    while 1:
        if (value >= 1):
            # Itensity at max, need to reduce the duty cycle, set -ve delta
            value = 1
            delta = -0.05
        elif (value <=0):
            value = 0
    	    # Intensity at lowest, set a +ve delta
            delta = 0.05

    	led.write(value) # Set the duty cycle
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
    	msg = mic.read()
        if mic.read() <= 79 and mic.read()>60:
            pass
        else:
            print "barulho ---%s---"%mic.read()
            value = value + delta

        time.sleep(0.005)
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)

                    #user entered a message
