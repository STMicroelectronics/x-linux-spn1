#!/usr/bin/python3

# Copyright (c) 2024 STMicroelectronics. All rights reserved.
#
# This software component is licensed by ST under BSD 3-Clause license,
# the "License"; You may not use this file except in compliance with the
# License. You may obtain a copy of the License at:
#                        opensource.org/licenses/BSD-3-Clause

# For simulating UI on PC , please use
# the variable SIMULATE = 1

import sys
import time
from application.x_linux_spn1.stspin_driver import STSpinDriver


class IHM15a1Driver(STSpinDriver):
    def __init__(self, pins=None):
        super().__init__()
        if pins is None:
            self.pins = {
                "pwm_a": (self.chip_d, 15),
                "pwm_b": (self.chip_e, 10),
                "ref_a": (self.chip_a, 11),
                "ref_b": (self.chip_a, 12),
                "en_a": (self.chip_e, 1),
                "en_b": (self.chip_e, 14),
                "stdby": (self.chip_h, 6),
                "dir_a": (self.chip_e, 9),
                "dir_b": (self.chip_d, 1)
            }
        else:
            self.pins=pins
        

        self.SIMULATE = 0

    def setup_gpio(self):
        super().setup_gpio()

        try:
            chip, pin = self.pins["pwm_a"]
            self.lines["pwm_a"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_output})
            chip, pin = self.pins["pwm_b"]
            self.lines["pwm_b"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_output})
            chip, pin = self.pins["ref_a"]
            self.lines["ref_a"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_output})
            chip, pin = self.pins["ref_b"]
            self.lines["ref_b"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_output})
            chip, pin = self.pins["en_a"]
            self.lines["en_a"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_input})
            chip, pin = self.pins["en_b"]
            self.lines["en_b"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_input})
            chip, pin = self.pins["stdby"]
            self.lines["stdby"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_output})
            chip, pin = self.pins["dir_a"]
            self.lines["dir_a"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_output})
            chip, pin = self.pins["dir_b"]
            self.lines["dir_b"] = self.gpio_chips[chip].request_lines(consumer="X-LINUX-SPN1",config={pin: self.config_output})

            self.set_lines_value(["stdby", "ref_a", "ref_b"], [1, 0, 0])
            self.set_lines_value(["dir_a", "dir_b", "pwm_a", "pwm_b"], [0, 0, 0, 0])

        except Exception as e:
            print(f"An error occurred during GPIO setup: {e}")
            sys.exit(1)

    def current_check(self):
        if self.SIMULATE == 1:
            return 0
        try:
            chip1, pin_a = self.pins["en_a"]
            chip2, pin_b = self.pins["en_b"]
            return (self.lines["en_a"].get_value(pin_a) and self.lines["en_b"].get_value(pin_b))
        except Exception as e:
            print(f"Error reading current state: {e}")
            return None

    def cleanup_gpio(self):
        if self.SIMULATE > 0:
            return
        try:
            for line in self.lines.values():
                line.release()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def start(self):
        if self.SIMULATE > 0:
            return
        self.is_on = 1
        try:
            self.set_lines_value(["ref_a", "ref_b", "pwm_a", "pwm_b"], [0, 0, 1, 1])
        except Exception as e:
            print(f"Error starting the motor: {e}")

    def stop(self):
        if self.SIMULATE > 0:
            return
        self.is_on = 0
        try:
            self.set_lines_value(["pwm_a", "pwm_b"], [0, 0])
        except Exception as e:
            print(f"Error stopping the motor: {e}")

    def right(self):
        if self.SIMULATE > 0:
            return
        try:
            if self.current_state != "R" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [0, 0])
                time.sleep(1)

            self.set_lines_value(["dir_a", "dir_b"], [0, 1])

            if self.current_state != "R" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [1, 1])
            self.current_state = "R"
        except Exception as e:
            print(f"Error turning right: {e}")

    def left(self):
        if self.SIMULATE > 0:
            return
        try:
            if self.current_state != "L" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [0, 0])
                time.sleep(1)

            self.set_lines_value(["dir_a", "dir_b"], [1, 0])

            if self.current_state != "L" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [1, 1])
            self.current_state = "L"
        except Exception as e:
            print(f"Error turning left: {e}")

    def forward(self):
        if self.SIMULATE > 0:
            return
        try:
            if self.current_state != "F" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [0, 0])
                time.sleep(1)

            self.set_lines_value(["dir_a", "dir_b"], [0, 0])

            if self.current_state != "F" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [1, 1])
            self.current_state = "F"
        except Exception as e:
            print(f"Error moving forward: {e}")

    def backward(self):
        if self.SIMULATE > 0:
            return
        try:
            if self.current_state != "B" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [0, 0])
                time.sleep(1)

            self.set_lines_value(["dir_a", "dir_b"], [1, 1])

            if self.current_state != "B" and self.is_on == 1:
                self.set_lines_value(["pwm_a", "pwm_b"], [1, 1])

            self.current_state = "B"
        except Exception as e:
            print(f"Error moving backward: {e}")

    def end(self):
        if self.SIMULATE > 0:
            return
        self.is_on = 0
        try:
            self.set_lines_value(["ref_a", "ref_a", "pwm_a", "pwm_b", "dir_a", "dir_b"], [0, 0, 0, 0, 0])

        except Exception as e:
            print(f"Error ending the motor operation: {e}")
