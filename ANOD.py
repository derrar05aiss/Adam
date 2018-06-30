from bluetooth import *
import sys
import threading
import multiprocessing as mp
from pyfirmata import Arduino, util
import RPi.GPIO as GPIO
import signal
import time
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid ="94f39d29-7d6d-437d-973b-fba39e49d4ee"
advertise_service( server_sock,"SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
                    )
print("Waiting for connection on RFCOMM channel %d" % port)
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

def recv():
    listb1=['b1:0', 'b1:1', 'b1:2', 'b1:3', 'b1:4', 'b1:5', 'b1:6', 'b1:7', 'b1:8', 'b1:9', 'b1:10']; listb2=['b2:0', 'b2:1', 'b2:2', 'b2:3', 'b2:4', 'b2:5', 'b2:6', 'b2:7', 'b2:8', 'b2:9', 'b2:10']
    listliv=['liv:0', 'liv:1', 'liv:2', 'liv:3', 'liv:4', 'liv:5', 'liv:6', 'liv:7', 'liv:8', 'liv:9', 'liv:10']; listhal=['ha:0', 'ha:1', 'ha:2', 'ha:3', 'ha:4', 'ha:5', 'ha:6', 'ha:7', 'ha:8', 'ha:9', 'ha:10']
    listkit=['kit:0', 'kit:1', 'kit:2', 'kit:3', 'kit:4', 'kit:5', 'kit:6', 'kit:7', 'kit:8', 'kit:9', 'kit:10']; listgar=['gar:0', 'gar:1', 'gar:2', 'gar:3', 'gar:4', 'gar:5', 'gar:6', 'gar:7', 'gar:8', 'gar:9', 'gar:10']
    while True:
        data = client_sock.recv(1024)
        print data
        if (data == 'on_room1' or data == 'off_room1' or data in listb1):
            LED_R1(data)
        if (data == 'on_room2' or data == 'off_room2' or data in listb2):
            LED_R2(data)
        if (data == 'on_livingroom' or data == 'off_livingroom' or data in listliv):
            LED_LIV(data)
        if (data == 'on_hall' or data == 'off_hall' or data in listhal):
            LED_HAL(data)
        if (data == 'on_kitchen' or data == 'off_kitchen' or data in listkit):
            LED_KIT(data)
        if (data == 'on_garage' or data == 'off_garage'):
            LED_GAR(data)
        if (data == 'on_vent' or data == 'off_vent'):
            clima(data)
        if (data == 'on_GAR' or data == 'off_GAR'):
            DC_GARAGE(data)
        if (data == 'on_DOOR' or data == 'off_DOOR'):
            DC_DOOR(data)
        if (data == '150f'):
            stepper_DOR(150, 0)
        if (data == '50f'):
            stepper_CAM(50, 0)
        if (data == '150b'):
            stepper_DOR(0, 150)
        if (data == '50b'):
            stepper_CAM(0, 50)
        if (data == 'rotate' or data == 'right' or data == 'left'):
            if data == 'rotate':
                stepper_CAM(100, 0)
            elif data == 'left':
                stepper_CAM(0, 5)
            elif data == 'right':
                stepper_CAM(5, 0)
        
            



def dhtt():
     while True:
         th1 =threading.Thread(target=dht, args=())   
         th2 =threading.Thread(target=dht1, args=())         
         th1.start()
         th2.start()
         
                           
def send():
    while True:
        th3 =threading.Thread(target=IR1, args=())
        th4 =threading.Thread(target=IR2, args=())
        th5 =threading.Thread(target=IR3, args=())       
        th3.start()        
        th4.start()
        th5.start()      
        th3.join()
        th4.join()
        th5.join()
        
        
##        th6 =threading.Thread(target=Flame, args=())
##        th7 =threading.Thread(target=mq2, args=())                        
        
##        th6.start()
##        th7.start()                
        
def send1():
    while True:
        th8 =threading.Thread(target=LDR_Security, args=())
        th9 =threading.Thread(target=LDR_Door, args=())
        th8.start()
        th9.start()
        th8.join()
        th9.join()
        
def send2():
    while True:
        ultrason()
        motion()
        #mq2()
       # motion()
        
def DC_GARAGE(data):
    board = Arduino('/dev/ttyACM0')
    mot1_1= board.get_pin('d:7:o')
    mot1_2= board.get_pin('d:8:o')
    if data == 'on_GAR':
        mot1_1.write(1)
        time.sleep(2)
        mot1_1.write(0)
        mot1_2.write(0)
    elif data == 'off_GAR':
        mot1_2.write(1)
        time.sleep(2)
        mot1_2.write(0)
        mot1_1.write(0)

def DC_DOOR(data):
     board = Arduino('/dev/ttyACM0')
     mot1_3= board.get_pin('d:12:o')
     mot1_4= board.get_pin('d:13:o')
     if data == 'on_DOOR':
        mot1_3.write(1)
        time.sleep(0.5)
        mot1_3.write(0)
     elif data == 'off_DOOR':
        mot1_4.write(1)
        time.sleep(0.5)
        mot1_4.write(0)
def testmail(S, B):
    import smtplib
    smtpUser = 'cubnassim@gmail.com'
    smtpPass = 'bac2013n'
    toAdd = 'adam11oueznadji@gmail.com'
    fromAdd = smtpUser
    subject = S
    header = 'TO: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
    body = B
    print header + ' \n' + body
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, toAdd, header + '\n' + body)
    s.quit
def stepper_DOR(f, b):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    coil_A_1_pin = 11 # pink
    coil_A_2_pin = 5 # orange
    coil_B_1_pin = 6 # blue
    coil_B_2_pin = 13 # yellow 
    StepCount = 8
    Seq = range(0, StepCount)
    Seq[0] = [0,1,0,0]
    Seq[1] = [0,1,0,1]
    Seq[2] = [0,0,0,1]
    Seq[3] = [1,0,0,1]
    Seq[4] = [1,0,0,0]
    Seq[5] = [1,0,1,0]
    Seq[6] = [0,0,1,0]
    Seq[7] = [0,1,1,0]
    GPIO.setup(coil_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_B_2_pin, GPIO.OUT)
    def setStep(w1, w2, w3, w4):
        GPIO.output(coil_A_1_pin, w1)
        GPIO.output(coil_A_2_pin, w2)
        GPIO.output(coil_B_1_pin, w3)
        GPIO.output(coil_B_2_pin, w4)
    def forward(delay, f):
        for i in range(f):
            for j in range(StepCount):
                setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                time.sleep(delay)
    def backwards(delay, b):
        for i in range(b):
            for j in reversed(range(StepCount)):
                setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                time.sleep(delay) 
    delay = 1         
    forward(int(delay) / 1000.0, int(f))
    time.sleep(1)
    backwards(int(delay) / 1000.0, int(b))
def stepper_CAM(f, b):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    coil_A_1_pin = 19 # pink
    coil_A_2_pin = 26 # orange
    coil_B_1_pin = 20 # blue
    coil_B_2_pin = 21 # yellow
    StepCount = 8
    Seq = range(0, StepCount)
    Seq[0] = [0,1,0,0]
    Seq[1] = [0,1,0,1]
    Seq[2] = [0,0,0,1]
    Seq[3] = [1,0,0,1]
    Seq[4] = [1,0,0,0]
    Seq[5] = [1,0,1,0]
    Seq[6] = [0,0,1,0]
    Seq[7] = [0,1,1,0]
    GPIO.setup(coil_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_B_2_pin, GPIO.OUT)
    def setStep(w1, w2, w3, w4):
        GPIO.output(coil_A_1_pin, w1)
        GPIO.output(coil_A_2_pin, w2)
        GPIO.output(coil_B_1_pin, w3)
        GPIO.output(coil_B_2_pin, w4)
    def forward(delay, f):
        for i in range(f):
            for j in range(StepCount):
                    setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                    time.sleep(delay)
    def backwards(delay, b):
        for i in range(b):
            for j in reversed(range(StepCount)):
                setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                time.sleep(delay)
    delay = 1 
    forward(int(delay) / 1000.0, int(f))
    time.sleep(1)
    backwards(int(delay) / 1000.0, int(b))
def ultrason():
    GPIO.setmode(GPIO.BCM)
    pinTrigger = 18
    pinEcho = 23
    GPIO.cleanup
    def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup() 
	sys.exit(0)
    signal.signal(signal.SIGINT, close)
    GPIO.setup(pinTrigger, GPIO.OUT)
    GPIO.setup(pinEcho, GPIO.IN)
    while True:
	GPIO.output(pinTrigger, True)
	time.sleep(0.00001)
	GPIO.output(pinTrigger, False)
	startTime = time.time()
	stopTime = time.time()
	while 0 == GPIO.input(pinEcho):
		startTime = time.time()
	while 1 == GPIO.input(pinEcho):
		stopTime = time.time()
	TimeElapsed = stopTime - startTime
	distance = (TimeElapsed * 34300) / 2
	print ("Distance: %.1f cm" % distance)
	if distance < 20:
            print 'ultrason detect'
            client_sock.send('Ul')
	time.sleep(1)
        break
def motion():
    from gpiozero import MotionSensor

    def close(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, close)
    pir = MotionSensor(9)
    while True:
        if pir.motion_detected:
            print "Motion detected"
            client_sock.send('M')
            time.sleep(1)
        break
def IR1():
    ir1 = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ir1, GPIO.IN)
    GPIO.setwarnings(False)
    while True:
         if GPIO.input(ir1) == 0:
             print ('IR_ROOM1_Detect')
             Buzz(1)
             client_sock.send('IR1_Detect')
             time.sleep(1)
         else:
             Buzz(0)
         break
def IR2():
    ir2 = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ir2, GPIO.IN)
    GPIO.setwarnings(False)
    while True:
       	if GPIO.input(ir2) == 0:
            print ("infrared room 2 detected")
            client_sock.send('IR2_Detect')           
            Buzz(1)
            time.sleep(1)
        else:
            Buzz(0)
        break
def IR3():
    ir3 = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ir3, GPIO.IN)
    while True:
        if GPIO.input(ir3) == 0:
            print ("infrared garage  detected")
            client_sock.send('G_O')
            DC_GARAGE('on_GAR')
            time.sleep(5)
            client_sock.send('G_C')
            DC_GARAGE('off_GAR')            
        break
def Flame():
     GPIO.setwarnings(False)
     flame = 22
     GPIO.setmode(GPIO.BCM)
     GPIO.setup(flame, GPIO.IN)
     while True:
        if GPIO.input(flame) == 0:
           print ("flame detected")
           client_sock.send('Flame_Detect')
           Buzz(1)
           time.sleep(0.5)
        else:
           Buzz(0)
        break
def clima(data):
    board = Arduino('/dev/ttyACM0')
    vent = board.get_pin('d:4:o')
    if data == 'on_vent' or '1':
      vent.write(1)
    elif data == 'off_vent' or data == '0':
      vent.write(0)
def dht():
    import Adafruit_DHT
    humidity, temperature = Adafruit_DHT.read_retry(11, 24)
    print 'Temp:', temperature, 'C'
    client_sock.send(str(temperature))
    if temperature > 30:
       clima('1')
    else:
       clima('0')
    

def dht1():
    import Adafruit_DHT
    humidity, temperature = Adafruit_DHT.read_retry(11, 24)
    print 'Humidity:', humidity, '%'
    client_sock.send(str(humidity))
def mq2():
    import Adafruit_ADS1x15
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 1
    while True:
        values = [0]*1
        for i in range(1):
            values[i] = adc.read_adc(i, gain=GAIN)
        print('LPG: ' + '{0:>6}'.format(*values) + ' ppm')
        break
def LDR_Security():
    GPIO.setwarnings(False)
    __author__ = 'Gus (Adapted from Adafruit)'
    __license__ = "GPL"
    __maintainer__ = "pimylifeup.com"
    GPIO.setmode(GPIO.BCM)
    pin_to_circuit = 16
    def rc_time (pin_to_circuit):
        count = 0
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(pin_to_circuit, GPIO.IN)
        while (GPIO.input(pin_to_circuit) == GPIO.LOW):
            count += 1
        return count
    while True:
        ldr = rc_time(pin_to_circuit)
        print ('ldr Security:', ldr)

        if ldr > 50:
            Buzz(1)
            client_sock.send('s')
        else:
            Buzz(0)
        time.sleep(0.1)
        break
def LDR_Door():
    GPIO.setwarnings(False)
    __author__ = 'Gus (Adapted from Adafruit)'
    __license__ = "GPL"
    __maintainer__ = "pimylifeup.com"
    GPIO.setmode(GPIO.BCM)
    pin_to_circuit = 12
    def rc_time (pin_to_circuit):
        count = 0
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(pin_to_circuit, GPIO.IN)
        while (GPIO.input(pin_to_circuit) == GPIO.LOW):
            count += 1
        return count
    while True:
        ldr = rc_time(pin_to_circuit)
        print ('ldr Door:', ldr)
        if ldr > 100:
            client_sock.send('O')
            stepper_DOR(0, 150)
            time.sleep(5)
            client_sock.send('C')
            stepper_DOR(150, 0)
        else:
            stepper_DOR(0, 0)
        time.sleep(0.1)
        break
def LDR_YARD():
    GPIO.setwarnings(False)
    board = Arduino('/dev/ttyACM0')
    __author__ = 'Gus (Adapted from Adafruit)'
    __license__ = "GPL"
    __maintainer__ = "pimylifeup.com"
    GPIO.setmode(GPIO.BCM)
    pin_to_circuit = 10
    led_yard = board.get_pin('d:11:p')
    def rc_time (pin_to_circuit):
        count = 0
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(pin_to_circuit, GPIO.IN)
        while (GPIO.input(pin_to_circuit) == GPIO.LOW):
            count += 1
        return count
    while True:
        ldr = rc_time(pin_to_circuit)
        print ('ldr Yard:', ldr)
        if ldr <= 100:
            led_yard.write(0)
        elif 100 <ldr <= 200:
            led_yard.write(0.2)
        elif 200 < ldr <= 500:
            led_yard.write(0.5)
        elif 500 < ldr <= 800:
            led_yard.write(0.7)
        elif 800<ldr < 230000:
            led_yard.write(1)
        else:
            led_yard.write(0)
        time.sleep(1)
def Buzz(b):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(8, GPIO.OUT) 
    GPIO.output(8, b)
def LED_R1(data):
    from pyfirmata import Arduino, util
    board = Arduino('/dev/ttyACM0')
    led_r1 = board.get_pin('d:3:p')
    if data == 'off_room1' or data == 'b1:0' :
        led_r1.write(0)
    elif data ==  'on_room1' or data == 'b1:10':
        led_r1.write(1)
    elif 'b1:1' <= data <= 'b1:2':
        led_r1.write(0.2)
    elif 'b1:2' < data <= 'b1:5':
        led_r1.write(0.5)
    elif 'b1:5' < data <= 'b1:9':
        led_r1.write(0.8)
def LED_R2(data):
    board = Arduino('/dev/ttyACM0')
    led_r2 = board.get_pin('d:5:p')
    if   data == 'off_room2'  or data == 'b2:0' :
        led_r2.write(0) 
    elif data ==  'on_room2' or data == 'b2:10':
        led_r2.write(1)   
    elif 'b2:1' <= data <= 'b2:2':
        led_r2.write(0.2)
    elif 'b2:2' < data <= 'b2:5':
        led_r2.write(0.5)
    elif 'b2:5' < data <= 'b2:9':
        led_r2.write(0.8)
    else:
        led_r2.write(0)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
def LED_LIV(data):
    from pyfirmata import Arduino, util
    board = Arduino('/dev/ttyACM0')
    led_liv = board.get_pin('d:6:p')
    if   data == 'off_livingroom'  or data == 'liv:0' :
        led_liv.write(0)
    elif data ==  'on_livingroom' or data == 'liv:10':
        led_liv.write(1)
    elif 'liv:1' <= data <= 'liv:2':
        led_liv.write(0.2)
    elif 'liv:2' < data <= 'liv:5':
        led_liv.write(0.5)
    elif 'liv:5' < data <= 'liv:9':
        led_liv.write(0.8)
    else:
        led_liv.write(0)
def LED_HAL(data):
    board = Arduino('/dev/ttyACM0')
    led_hal = board.get_pin('d:9:p')
    if   data == 'off_hall'  or data == 'ha:0' :
        led_hal.write(0) 
    elif data ==  'on_hall' or data == 'ha:10':
        led_hal.write(1)   
    elif 'ha:1' <= data <= 'ha:2':
        led_hal.write(0.2)
    elif 'ha:2' < data <= 'ha:5':
        led_hal.write(0.5)
    elif 'ha:5' < data <= 'ha:9':
        led_hal.write(0.8)
    else:
        led_hal.write(0)
def LED_KIT(data):
    board = Arduino('/dev/ttyACM0')
    led_kit = board.get_pin('d:10:p')
    if   data == 'off_kitchen'  or data == 'kit:0' :
        led_kit.write(0) 
    elif data ==  'on_kitchen' or data == 'kit:10':
        led_kit.write(1)   
    elif 'kit:1' <= data <= 'kit:2':
        led_kit.write(0.2)
    elif 'kit:2' < data <= 'kit:5':
        led_kit.write(0.5)
    elif 'kit:5' < data <= 'kit:9':
        led_kit.write(0.8)
    else:
        led_kit.write(0)
def LED_GAR(data):
    board = Arduino('/dev/ttyACM0')
    led_gar = board.get_pin('d:2:o')
    if  data == 'off_garage':
        led_gar.write(0)
    elif data ==  'on_garage' :
        led_gar.write(1)
try:
    pro1 = mp.Process(target=recv, args=())
    pro1.start()
    pro2 = mp.Process(target=send1, args=())
    pro2.start()
    
    
    
    
    

except IOError:
     pass
print("disconnected")
client_sock.close()
server_sock.close()
print("all done")


