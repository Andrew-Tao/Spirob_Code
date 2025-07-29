import time
import keyboard
import threading
from motors import Motors
import numpy as np
import queue
import time
# from keyboard_control import MyListener
import sys
import pygame
from pygame import joystick
import pigpio
import matplotlib.pyplot as plt

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
joy = pygame.joystick.Joystick(0)
joy.init()

debug_pulse_thread_interval=[]
debug_control_thread_interval = []
def plot_motor_signal_output(timestamps,levels):
    plot_time = [0]
    plot_level = [levels[0] if levels else 0]
    for t,l in zip(timestamps,levels):
        plot_time.extend([t,t])
        plot_level.extend([plot_level[-1],l])
    #plt.figure(figsize=(10,3))
    #plt.step(plot_time,plot_level,where = 'post')
    timestamps_freq = []
    print(len(timestamps)-1)
    for i in range(int(len(timestamps)-1)):
        timestamps_freq.append(timestamps[i+1]-timestamps[i])
    x_values = list(range(len(timestamps_freq)))
    
    mean = np.mean(timestamps_freq)
    var = np.var(timestamps_freq)
    print("Mean",mean,"s")
    print("Varience",var)
    
    plt.figure(1)

    plt.plot(x_values,timestamps_freq)
    plt.ylim(0,0.01)
    plt.xlabel("Time")
    plt.ylabel("GPIO Level")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    
    
    x_values2 = list(range(len(timestamps)))
    plt.figure(2)
    plt.plot(x_values2,timestamps)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    
    plt.show()
    
def main_loop(motors,motor_index: int = 0, dir: int = 1, speed: float = 1):
    

    print('Running motor', motor_index, 'forward' if dir > 0 else 'backward', 'at speed', speed)

    if dir > 0:
        motors.dir_motor_forward([motor_index])
    else:
        motors.dir_motor_backward([motor_index])
    motors.set_motor_speed([motor_index], speed)
    motors.start_motor([motor_index])

    # state = {"direction": 1, "speed": 1}
    # listener = MyListener(state)
    # listener.start()

    print("Starting main loop.")
    Action = True
    start_step = motors.num_of_steps[motor_index]
    duration = 500

    try:
        while Action:
            # if state["direction"] > 0:
            #     motors.dir_motor_forward()
            # else:
            #     motors.dir_motor_backward()
            # motors.set_motor_speed([2], state["speed"])
            current_step = motors.num_of_steps[motor_index]
            elapsed = current_step - start_step
            motors.update([0, 1, 2])
            if abs(elapsed) >= duration: Action = False
            #time.sleep(0.002)
    except KeyboardInterrupt:
        print("\nMain loop interrupted by Ctrl+C.")
    finally:
        motors.stop_motor([0, 1, 2])
        print(motors.motor_direction)
        print(motors.num_of_steps)
"""
def home_arm(motors):
    print("Moving the Arm to Home Position...")
    for motor_index in range(len(motors._PUL_devices)):
        print(motor_index)
        if motors.num_of_steps[motor_index] > 0:
             motors.dir_motor_backward([motor_index])
        else:
             motors.dir_motor_forward([motor_index])
        motors.set_motor_speed([motor_index], 1)
        motors.start_motor([motor_index])
        #start_step = motors.num_of_steps.copy()
        #target_steps = list(np.subtract([0,0,0],start_step))
        target = [0,0,0]
        

        #print("motor_directions",motors.motor_direction)
        #print("motor_running",motors._motor_running)
    
    Action = threading.Event()
    Action.set()
    def control_thread():
        global debug_control_thread_interval
        try:
            while Action.is_set():

                start_time = time.perf_counter()
                
                current_step = motors.num_of_steps.copy()
                gap_step = [abs(a - b) for a,b in zip(target,current_step)]
                
                print(current_step,"|motor_running",motors._motor_running,"|motor_directions",motors.motor_direction,"|target_step",target)
                
                for motor_index in range(len(motors._PUL_devices)):
                    if gap_step[motor_index] <= 5:
                        motors.stop_motor([motor_index])

                if np.sum(motors._motor_running) == 0:
                    print("The process is done")
                    Action.clear()
                else:
                    end_time = time.perf_counter()
                debug_control_thread_interval.append(end_time)
                #time.sleep(0.01)

                current_step = motors.num_of_steps[0]
                gap_step = target[0]-current_step
                
            
                if gap_step <=  5:
                    Action.clear()
        except KeyboardInterrupt:
            print("\nMain loop interrupted by Ctrl+C.")

        finally:
            Action.clear()

        
    def pulse_thread():
        global debug_control_thread_interval
        try: 
            while Action.is_set():
                #start_time = time.perf_counter()
                motors.update([0,1,2])
                #end_time = time.perf_counter()
                #debug_pulse_thread_interval.append(end_time)
                #time.sleep(0.005)
        except KeyboardInterrupt:
            print("\nMain loop interrupted by Ctrl+C.")

        finally:
            motors.stop_motor([0, 1, 2])
            print(motors.motor_direction)
            print(motors.num_of_steps)
            
    threading.Thread(target = control_thread,daemon = True).start()
    threading.Thread(target = pulse_thread,daemon = True).start()
    

    
    print("Arm has been Homed")
"""

def home_arm(motors):
    print("Moving the Arm to Home Position...")
    for motor_index in range(len(motors._PUL_devices)):
        print(motor_index)
        if motors.num_of_steps[motor_index] > 0:
             motors.dir_motor_backward([motor_index])
        else:
             motors.dir_motor_forward([motor_index])
        motors.set_motor_speed([motor_index], 1)
        motors.start_motor([motor_index])
        #start_step = motors.num_of_steps.copy()
        #target_steps = list(np.subtract([0,0,0],start_step))
        target = [0,0,0]
        

        #print("motor_directions",motors.motor_direction)
        #print("motor_running",motors._motor_running)
        Action = True
        
    try:
        while Action == True:
            """
        
            current_step = motors.num_of_steps
            gap_step = [abs(a - b) for a,b in zip(target,current_step)]
            
            print(current_step,"|motor_running",motors._motor_running,"|motor_directions",motors.motor_direction,"|target_step",target)
            motors.update([0,1,2])
            for motor_index in range(len(motors._PUL_devices)):
                if gap_step[motor_index] <= 5:
                    motors.stop_motor([motor_index])

            if np.sum(motors._motor_running) == 0:
                print("The process is done")
                Action = False
            """
            
            current_step0 = motors.num_of_steps[0]
            current_step1 = motors.num_of_steps[1]
            current_step2 = motors.num_of_steps[2]

            
            gap_step0 = target[0] - current_step0
            gap_step1 = target[1] - current_step1
            gap_step2 = target[2] - current_step2
            
            #print(current_step,"|motor_running",motors._motor_running,"|motor_directions",motors.motor_direction,"|target_step",target)
            motors.update([0,1,2])
       
            if gap_step0 <= 5:
                motors.stop_motor([0])
            if gap_step1 <= 5:
                motors.stop_motor([1])
            if gap_step2 <= 5:
                motors.stop_motor([2])
                
            if np.sum(motors._motor_running) == 0:
                print("The process is done")
                Action = False

    except KeyboardInterrupt:
        print("\nMain loop interrupted by Ctrl+C.")
    finally:
        motors.stop_motor([0, 1, 2])
        print(motors.motor_direction)
        print(motors.num_of_steps)

    print("Arm has been Homed")


def listen_for_home_command(motors):
    global exc_home_time
    print("Listening for command...") 
    input_buffer = ""
    while True:

        cmd = input()
        if cmd.strip().lower() == "home the robot":
            exc_home_time = time.time()
            pause_main_tread.clear()
            home_arm(motors)
            pause_main_tread.set()
    return home_time
            
def button_reaction(mode: int):
    if mode == 0: direction = -1  # Standard mode
    elif mode == 1: direction = 1 # Left_button is pressed
    
    A_pressed = joy.get_button(0)
    B_pressed = joy.get_button(1)
    X_pressed = joy.get_button(2)
    if joy.get_button(3):
        Y_button_case(mode)
    if A_pressed: button = 2
    elif B_pressed: button = 0
    elif X_pressed: button = 1

    if A_pressed or B_pressed or X_pressed: 
        args = [motors,button,direction,1]
        main_loop(*args)

    return 0

def Y_button_case(mode):
    if mode == 0:
        # Show Current num_of_step
        print("Current num_of_step:",motors.num_of_steps)
        return 0
    elif mode == 1:
        # Calibrate Step Mannully by pressing Y
        motors.num_of_steps = [0,0,0]
        print("Your step record has been calibrated! Current num_of_step:",motors.num_of_steps)
    

if __name__ == "__main__":     
    print("Start Program")  
    Coordinate_Debug = False


    PUL = [17, 25, 22] 
    DIR = [27, 24, 23] 
    MOTOR_ORIENTATION = [True, True, False]
    
    timestamps = []
    levels = []

 
    
    def gpio_callback(gpio,level,tick):
        t = time.time() - start_time
        timestamps.append(t)
        levels.append(level)
        
    pi = pigpio.pi()
    
    pi.set_mode(17,pigpio.INPUT)
    start_time = time.time()

    motors = Motors(
        PUL, 
        DIR, 
        MOTOR_ORIENTATION, 
        steps_per_rev=1600, 
        max_rpm=30, 
        pulse_width=10 * 1e-6,
        debug=False)
        
   
    
    if Coordinate_Debug:
        motors.num_of_steps = [-5000,0,0]
        print("Doing home_arm() debug")
        home_arm(motors)
        cb.cancel()
        pi.stop()
        plot_motor_signal_output(timestamps,levels)


    cb = pi.callback(17,pigpio.RISING_EDGE,gpio_callback)
    
    #result_queue = queue.Queue()
    listener_thread = threading.Thread(target=listen_for_home_command, args = (motors,),daemon = True)
    
    listener_thread.start()
    pause_main_tread = threading.Event()
    pause_main_tread.set()
    #home_time = result_queue.get() 
    
    
    try :
        
        while True:
            pause_main_tread.wait()
            pygame.event.pump()
            button_to_motor = {0:0,1:1,2:2}
            ALLOWED_BUTTON = {0,1,2}
            
            for event in pygame.event.get():
                if event.type  == pygame.JOYBUTTONDOWN:
                    if joy.get_button(4):
                        button_reaction(1)
                    else:
                        button_reaction(0)
                if event.type == pygame.JOYBUTTONUP:
                    pass
    
            
    except KeyboardInterrupt:
        print("Main loop interrupted")
    finally:
        cb.cancel()
        pi.stop()
        """
        print("Start time",start_time)
        print("raw_home_time",exc_home_time)
        exc_home_time -= start_time
        print("home time is",exc_home_time)
        timestamps = [x for x in timestamps if x  >= exc_home_time]
        """
        plot_motor_signal_output(timestamps,levels)
        """
        print("Control",len(debug_control_thread_interval),np.mean(debug_control_thread_interval))
        print("pulse",len(debug_pulse_thread_interval),np.mean(debug_pulse_thread_interval))
        
        with open("raw_data.txt","w") as f: 
            f.write("Control Intervals:\n")
            for item in debug_control_thread_interval:
                f.write(f"{item}\n")
            f.write("Pulse Intervals:\n")
            for item in debug_pulse_thread_interval:
                f.write(f"{item}\n")
        con_list = debug_control_thread_interval,debug_control_thread_interval
        pul_list = debug_pulse_thread_interval,debug_pulse_thread_interval
        plt.scatter(con_list, con_list, color='red', label='Control Intervals')
        plt.scatter(pul_list, pul_list, color='blue', label='Pulse Intervals')
        #plt.plot(debug_control_thread_interval,color = "red",label = "control")
        #plt.plot(debug_pulse_thread_interval,color = "blue",label = "pulse")
        plt.plot()
        plt.legend()
        plt.show()
        """
        pass
        
    
