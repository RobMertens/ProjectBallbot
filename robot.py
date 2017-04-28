import mavlink
import serial

class Robot:
    x = 0.0
    y = 0.0
    z = 0.0
    roll = 0.0
    pitch = 0.0
    yaw = 0.0

    gpio_float = [0 for i in range(8)]
    gpio_int = [0 for i in range(8)]

    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial(port, 115200, timeout=0)
        if self.ser.isOpen:
            self.ser.flushInput()
            self.ser.flushOutput()
        else:
            print "Error when opening serial port"

        self.mav = mavlink.MAVLink(0)

    def receive(self):
	    b = self.ser.read(1024)
	    for k in range (0,len(b)) :
	        msg = self.mav.parse_char(b[k])
	        if msg is not None:
                    self.info(msg)

    def send(self, msg):
        self.ser.write(msg.get_msgbuf())

    def info(self, msg):
        switch = {
            mavlink.MAVLINK_MSG_ID_HEARTBEAT: self.info_heartbeat,
            mavlink.MAVLINK_MSG_ID_THREAD_INFO: self.info_thread_info,
            mavlink.MAVLINK_MSG_ID_PRINT: self.info_print,
            mavlink.MAVLINK_MSG_ID_POSE: self.info_pose,
            mavlink.MAVLINK_MSG_ID_GPIO: self.info_gpio
        }
        func = switch.get(msg.get_msgId())
        return func(msg)

    def info_heartbeat(self, msg):
        return

    def info_thread_info(self, msg):
        return

    def info_print(self, msg):
        print msg.text

    def info_pose(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.z = msg.z
        self.roll = msg.roll
        self.pitch = msg.pitch
        self.yaw = msg.yaw

    def info_gpio(self, msg):
        self.gpio_float = msg.gpio_float
        self.gpio_int = msg.gpio_int

    def mode_idle(self):
        return 200

    def mode_attitude(self):
        return 201

    def mode_velocity(self):
        return 202

    def mode_position(self):
        return 203

    def set_idle_mode(self):
        msg = self.mav.event_encode(self.mode_idle())
        self.send(msg)

    def set_attitude_mode(self):
        msg = self.mav.event_encode(self.mode_attitude())
        self.send(msg)

    def set_velocity_mode(self):
        msg = self.mav.event_encode(self.mode_velocity())
        self.send(msg)

    def set_position_mode(self):
        msg = self.mav.event_encode(self.mode_position())
        self.send(msg)

    def set_velocity_cmd(self, vx, vy, vz):
        msg = self.mav.velocity_cmd_encode(vx, vy, vz, 0, 0, 0)
        self.send(msg)


