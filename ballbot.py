from robot import Robot
import threading
import time

port = '/dev/ttyAMA0'       # default usb port
#port = '/dev/rfcomm0'       # default bluetooth port

ballbot = Robot(port)         #make a robot/ballbot
running = True                          #set the running flag

# Function where the ballbot receives data
def ballbot_update():
    while running:
        ballbot.receive()
        ballbot.info_print()
	time.sleep(0.05)
	
# Controller update
dt = 5
def controller_update():
    for i in range(0,dt):
        print (dt-i)
        time.sleep(1)
    ballbot.set_attitude_mode() # go to attitude mode
    for i in range(0,dt):
        print (dt-i)
        time.sleep(1)
    ballbot.set_velocity_mode() # go to velocity mode
    while running:
        # update the pids here
        ballbot.set_velocity_cmd(0, 0, 0)
        time.sleep(0.1)

################
# MAIN PROGRAM #
################
# Make the 2 threads and start them
ballbot_thread = threading.Thread(None,ballbot_update,"ballbot_thread")
controller_thread = threading.Thread(None,controller_update,"controller_thread")
ballbot_thread.start()
controller_thread.start()

# Wait for user input to make the program halt
raw_input("press some key...")
# Set running false when we got a keystroke
running = False
# Wait for both threads to finish
while ballbot_thread.is_alive() or controller_thread.is_alive():
    time.sleep(0.1)
ballbot.set_idle_mode()
print "Stopped"
