#!/bin/sh

##
##############################################################################
# @file   deploy.sh
# @author SRA-SAIL, Noida
# @brief  Script for deploying the X-LINUX-SPN1 application to STM32MP1 board
##############################################################################
# @attention
#
# Copyright (c) 2023 STMicroelectronics.
# All rights reserved.
#
# This software is licensed under terms that can be found in the LICENSE file
# in the root directory of this software component.
# If no LICENSE file comes with this software, it is provided AS-IS.
#
##############################################################################
##

# usage ./deploy <ip address of the board>

if [ $# -eq 0 ]; then
    echo "Error: please provide the IP address of the board"
    exit 1
fi

ssh root@$1 "cd /usr/local/demo/application;rm -r x_linux_spn1;mkdir -p x_linux_spn1"
scp -r ../application/x_linux_spn1/* root@$1:/usr/local/demo/application/x_linux_spn1/
scp ../application/080-x-linux-spn1.yaml root@$1:/usr/local/demo/application/