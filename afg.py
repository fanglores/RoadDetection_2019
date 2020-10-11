import time
import os

STEER = 11
ESC = 12
spd = 10
ang = 90

def setup_gpio():
    os.system("sudo pigpiod")  # Launching GPIO library
    time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
    import pigpio
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(ESC, 0)
    pi.set_servo_pulsewidth(STEER, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, 1500)
    time.sleep(1)

    return pi,ESC,STEER

def calibrate(pi,ESC):
    max_value = 2000
    min_value = 700
    pi.set_servo_pulsewidth(ESC, 0)
    print("Power off and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Plug in the battery and wait until you hear 2 beeps. Then press enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print ("The signal iscoming")
            time.sleep(7)
            print ("Be patient ....")
            time.sleep (5)
            print ("Don't worry, just wait.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print ("Power off the esc now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print ("Calibration done")
            # control() # You can change this to any other function you want
            pi.set_servo_pulsewidth(ESC, 1500)

def control(pi,ESC,speed,STEER,angle):
    pi.set_servo_pulsewidth(ESC, speed)
    pi.set_servo_pulsewidth(STEER,int(16.6666666*angle))

def stop(pi,ESC): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

def main():  #angles - 75 - 90 - 105

    pi, ESC, STEER = setup_gpio()
    print("Attempt")
    try:
        pi,set_servo_pulsewidth(ESC, 1500)
        print("Success")
    except:
        print("Failed")
        
    #calibrate(pi,ESC)
    print(spd, ang)
    control(pi, ESC, spd, STEER, ang)

if __name__ == '__main__':
    main()
