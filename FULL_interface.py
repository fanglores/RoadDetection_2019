import curses
import time
import os
import cv2

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

def stop(pi, ESC, STEER, cap):
    try:
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, 0)
        pi.set_servo_pulsewidth(STEER, 0)
        time.sleep(0.2)
        pi.stop()
        cap.release()
        cv2.destroyAllWindows()
        curses.endwin()
        print('Success')
    except:
        print('Critical error!')

c = ' '
pi = 0
try:
    pi, ESC, STEER = setup_gpio()
    cap = cv2.VideoCapture(0)

    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(38, 1)
    
    window = curses.initscr()
    curses.noecho()
    window.keypad(True) 
    print("Full Init completed\n")
except:
    print('Error while initializing')
    stop(pi, ESC, STEER, cap)
    exit()

control(pi, ESC, 1500, STEER, 90)
print('YEP!')
time.sleep(3)

try:
    while (ord(c) != 27):
    #try:
        
        for i in range(3):
            cap.grab()
            flag, img = cap.retrieve()

        cv2.imshow('Window', img)
        cv2.waitKey(1)
    
    
        c = window.get_wch()
        #print('Got an [' + str(c) + ']')
        #print('My angle is ',CURRENT_ANGLE)
        if(c == 'w'):
            pi.set_servo_pulsewidth(ESC, 1560)
            print("Moving forward")
            time.sleep(0.03)
        elif(c == 's'):
            pi.set_servo_pulsewidth(ESC, 1380)
            print("Moving backward")
            time.sleep(0.03)
        elif(c == 'a'):
            if(CURRENT_ANGLE < 112):
                CURRENT_ANGLE += 2
                pi.set_servo_pulsewidth(STEER, int(16.6666666*CURRENT_ANGLE))
                print('Rotating left')
            else:
                print('Max angle!')
        elif(c == 'd'):
            if(CURRENT_ANGLE > 68):
                CURRENT_ANGLE -= 2
                pi.set_servo_pulsewidth(STEER, int(16.6666666*CURRENT_ANGLE))
                print('Rotating right')
            else:
                print('Min angle!')

        time.sleep(0.1)
        pi.set_servo_pulsewidth(ESC, 1500)
        curses.flushinp()
        window.refresh()

except:
    print("Runtime error")
    stop(pi, ESC, STEER, cap)


stop(pi, ESC, STEER, cap)
