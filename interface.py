import curses
import time
import os

STEER = 18
ESC = 17
spd = 10
ang = 90
CURRENT_ANGLE = 90

def setup_gpio():
    print("Initializing gpio")
    try:
        #os.system("sudo pigpiod")  # Launching GPIO library
        #time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
        import pigpio
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(ESC, 0)
        pi.set_servo_pulsewidth(STEER, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, 1500)
        time.sleep(1)
    except:
        print('gpio init failed')
        exit(0)
    print("gpio init success")
    
    return pi,ESC,STEER

def control(pi,ESC,speed,STEER,angle):
    pi.set_servo_pulsewidth(ESC, speed)
    pi.set_servo_pulsewidth(STEER,int(16.6666666*angle))

def stop(pi,ESC): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

c = ' '
pi = 0
try:
    pi, ESC, STEER = setup_gpio()
    
    window = curses.initscr()
    curses.noecho()
    window.keypad(True) 
    print("Full Init completed\n")
except:
    print('Error while initializing')
    exit()

control(pi, ESC, 1500, STEER, 90)
print('YEP!')
time.sleep(3)

while (ord(c) != 27):
#try:
    c = window.get_wch()
    #print('Got an [' + str(c) + ']')
    print('My angle is ',CURRENT_ANGLE)
    if(c == 'w'):
        pi.set_servo_pulsewidth(ESC, 1570)
        time.sleep(0.5)
        print("Moving forward")
    elif(c == 's'):
        pi.set_servo_pulsewidth(ESC, 1350)
        time.sleep(0.5)
        print("Moving backward")
    elif(c == 'a'):
        if(CURRENT_ANGLE >= 90):
            CURRENT_ANGLE -= 20
            pi.set_servo_pulsewidth(STEER, int(16.6666666*CURRENT_ANGLE))
            time.sleep(0.5)
            print('Rotating left')
        else:
            print('Min angle!')
    elif(c == 'd'):
        if(CURRENT_ANGLE <= 90):
            CURRENT_ANGLE += 20
            pi.set_servo_pulsewidth(STEER, int(16.6666666*CURRENT_ANGLE))
            time.sleep(0.5)
            print('Rotating right')
        else:
            print('Max angle!')
    pi.set_servo_pulsewidth(ESC, 1500)
    curses.flushinp()
#except:
    #print("Caught Error")

    window.refresh()

#pi.set_servo_pulsewidth(STEER, 90)
time.sleep(1)
pi.set_servo_pulsewidth(ESC, 0)
pi.set_servo_pulsewidth(STEER, 0)
time.sleep(0.2)
pi.stop()
curses.endwin()
