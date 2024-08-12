#!/bin/sh

##
##############################################################################
# @file   deploy.sh
# @author SRA-SAIL, Noida
# @brief  Script for deploying the X-LINUX-SPN1 application to STM32MP1 board
##############################################################################
# @attention
#
# Copyright (c) 2024 STMicroelectronics.
# All rights reserved.
#
# This software is licensed under terms that can be found in the LICENSE file
# in the root directory of this software component.
# If no LICENSE file comes with this software, it is provided AS-IS.
#
##############################################################################
##

# Usage ./deploy <ip address of the board>

# Ensure that the script is run from its directory
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
CURRENT_DIR=$(pwd)

if [ "$SCRIPT_DIR" != "$CURRENT_DIR" ]; then
    echo "Error: Script must be run from its directory: $SCRIPT_DIR"
    exit 1
fi

# Ensure that the IP Address is provided
if [ $# -eq 0 ]; then
    echo "Error: please provide the IP address of the board"
    exit 1
fi

ssh root@$1 "cd /usr/local/demo/application;rm -r x_linux_spn1;mkdir -p x_linux_spn1"
scp -r ../application/demo-launcher/* root@$1:/usr/local/demo/application/