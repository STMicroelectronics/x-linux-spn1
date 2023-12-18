#!/usr/bin/python3

# Copyright (c) 2023 STMicroelectronics. All rights reserved.
#
# This software component is licensed by ST under BSD 3-Clause license,
# the "License"; You may not use this file except in compliance with the
# License. You may obtain a copy of the License at:
#                        opensource.org/licenses/BSD-3-Clause

# For simulating UI on PC , please use
# the variable SIMULATE = 1

SIMULATE = 0

import sys
import time
def intialize():
    if SIMULATE > 0:
        return    
    global line_pwm_a
    global line_pwm_b
    global line_ref_a
    global line_ref_b
    global line_en_a
    global line_en_b
    global line_dir_a
    global line_dir_b
    global line_stdby
    global config
    global config_input
    global gpio_chip_a
    global gpio_chip_d
    global gpio_chip_e
    global gpio_chip_g

    gpio_chip_a = gpiod.chip("gpiochip0")
    gpio_chip_d = gpiod.chip("gpiochip3")
    gpio_chip_e = gpiod.chip("gpiochip4")
    gpio_chip_g = gpiod.chip("gpiochip6")
  
    line_pwm_a = gpio_chip_d.get_line(15)
    line_pwm_b = gpio_chip_e.get_line(10)
    line_ref_a = gpio_chip_a.get_line(11)
    line_ref_b = gpio_chip_a.get_line(12)
    line_en_a = gpio_chip_e.get_line(1)
    line_en_b = gpio_chip_e.get_line(14)
    line_stdby = gpio_chip_g.get_line(3)
    line_dir_a = gpio_chip_d.get_line(14)
    line_dir_b = gpio_chip_d.get_line(1)


    line_pwm_a.request(config)
    line_pwm_b.request(config)
    line_en_a.request(config_input)
    line_en_b.request(config_input)
    line_stdby.request(config)
    line_ref_a.request(config)
    line_ref_b.request(config)
    line_dir_a.request(config)
    line_dir_b.request(config)



    line_stdby.set_value(1)
    line_pwm_a.set_value(0)
    line_pwm_b.set_value(0)
 
if SIMULATE == 0:
    try:
        import gpiod
    except:
        print("gpiod not found")

    config = gpiod.line_request()
    config.consumer = "x-linux-spn1"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
    config_input = gpiod.line_request()
    config_input.consumer = "x-linux-spn1"
    config_input.request_type = gpiod.line_request.DIRECTION_INPUT
    intialize()


current_state = "F"
is_on = 0

def Current_check():
    if SIMULATE==1:
        return 0
    value1 = line_en_a.get_value()
    value2 = line_en_b.get_value()
  
    return value1 and value2



def cleanup():
    if SIMULATE > 0:
        return
    
    line_pwm_a.release()
    line_pwm_b.release()
    line_en_a.release()
    line_en_b.release()
    line_stdby.release()
    line_ref_a.release()
    line_ref_b.release()
    line_dir_a.release()
    line_dir_b.release()
 

def end():
    if SIMULATE > 0:
        return
    global is_on
    is_on = 0
    line_ref_a.set_value(0)
    line_ref_b.set_value(0)

    line_pwm_a.set_value(0)
    line_pwm_b.set_value(0)

    line_dir_a.set_value(0)
    line_dir_b.set_value(0)
    

 
  
def reset():
    if SIMULATE > 0:
        return
    global current_state
    current_state = "F"
    global is_on
    is_on = 0

  
    line_pwm_a.set_value(0)
    line_pwm_b.set_value(0)

    line_dir_a.set_value(0)
    line_dir_b.set_value(0)


def start():
    if SIMULATE > 0:
        return
    global is_on
    is_on = 1
    line_pwm_a.set_value(1)
    line_pwm_b.set_value(1)


def stop():
    if SIMULATE > 0:
        return
    global is_on
    is_on = 0
    line_pwm_a.set_value(0)
    line_pwm_b.set_value(0)


def right():
    if SIMULATE > 0:
        return
    global current_state
    global is_on
    if current_state != "R" and is_on == 1:
        line_pwm_a.set_value(0)
        line_pwm_b.set_value(0)
        time.sleep(1)
    line_dir_a.set_value(1)
    line_dir_b.set_value(0)
    if current_state != "R" and is_on == 1:
        line_pwm_a.set_value(1)
        line_pwm_b.set_value(1)

    current_state = "R"


def left():
    if SIMULATE > 0:
        return
    global current_state
    global is_on
    if current_state != "L" and is_on == 1:

        line_pwm_a.set_value(0)
        line_pwm_b.set_value(0)
        time.sleep(1)
    line_dir_a.set_value(0)
    line_dir_b.set_value(1)

    if current_state != "L" and is_on == 1:
      
        line_pwm_a.set_value(1)
        line_pwm_b.set_value(1)

    current_state = "L"


def forward():
    if SIMULATE > 0:
        return
    global current_state
    global is_on
    if current_state != "F" and is_on == 1:
        line_pwm_a.set_value(0)
        line_pwm_b.set_value(0)

        time.sleep(1)

    line_dir_a.set_value(0)
    line_dir_b.set_value(0)
    if current_state != "F" and is_on == 1:
        line_pwm_a.set_value(1)
        line_pwm_b.set_value(1)

    current_state = "F"


def backward():
    if SIMULATE > 0:
        return
    global current_state
    global is_on
    if current_state != "B" and is_on == 1:
        line_pwm_a.set_value(0)
        line_pwm_b.set_value(0)
        time.sleep(1)
    line_dir_a.set_value(1)
    line_dir_b.set_value(1)
    if current_state != "B" and is_on == 1:
        line_pwm_a.set_value(1)
        line_pwm_b.set_value(1)

    current_state = "B"


# Main
if __name__ == "__main__":
    command_map = {
        "F": forward,
        "B": backward,
        "R": right,
        "L": left,
        "S": start,
        "stop": stop,
        "reset": reset,
    }

    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1 in command_map:
            command_map[arg1]()

    pin_map = {
        "EN-A": line_en_a,  # "PE1"
        "PHA": line_dir_a,  # "PD14"
        "PWM-B": line_pwm_b,  # "PE10",
        "PWM-A": line_pwm_a,  # "PD15",
        "PHB": line_dir_b,  # "PD1",
        "STDBY": line_stdby,  # "PG3",
        "EN-B": line_en_b,  # "PE14",
        "REF-B": line_ref_b,  # "PA12",
        "REF-A": line_ref_b,  # "PA11"
    }

    if len(sys.argv) == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1 in pin_map:
            pin_map[arg1].set_value(arg2)
