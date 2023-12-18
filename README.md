# X-LINUX-SPN1 V2.0.0 Linux Package

![latest tag](https://img.shields.io/github/v/tag/STMicroelectronics/x-linux-spn1.svg?color=brightgreen)
==============================================================================================================

## Introduction

**X-LINUX-SPN1** is an OpenSTLinux based expansion software package to support application development for STSPIN family devices on the STM32MP microprocessor platform. It provides Linux software (drivers, APIs, and applications) to target the expansion boards based on STSPIN family motor drivers.
This software could be used as a starting point for developing more complex motor control applications. The included application and drivers run on Cortex-A core(s) of the MPU.

![X-LINUX-SPN1 Package](/_htmresc/01_x-linux-spn1-package.png "X-LINUX-SPN1 Package")

## Description

### X-LINUX-SPN1 software features:

The **X-LINUX-SPN1** expansion software provides drivers and user space applications running on the STM32MP platform to control multiple channels of a motor driver. The X-LINUX-SPN1 software package is made up of the following components:
1. Python APIs
2. GTK-based UI application

### X-LINUX-SPN1 Architecture:

The software uses *libgpiod* to control the motor drivers via GPIOs

![System Components](/_htmresc/02_system_components.png "System Components")

The provided GTK Application is built on top of the Python APIs and provides a ready-to-use interface. Application developers could, however, write their own applications using the Python APIs provided with this package.

![X-LINUX-SPN1 Architecture](/_htmresc/03_system_architecture.png "X-LINUX-SPN1 Architecture")

### X-LINUX-SPN1 Package Structure:

The package contains following files and folders:

```
├── application/    
│   ├── x_linux_spn1/
│   │   ├── pictures/
│   │   ├── ihm12_api.py
│   │   ├── ihm15_api.py
│   │   ├── __init__.py
│   │   ├── spn1_ui.css
│   │   ├── spn1_ui.glade
│   │   └── spn1_ui.py
│   ├── 080-x-linux-spn1.yaml
│   └── LICENSE.md
├── _htmresc/
├── scripts/
│   ├── deploy.sh
│   └── LICENSE.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── file_list.md
├── LICENSE.md
├── README.md*
├── Release_Notes.md
└── SECURITY.md*
```

The contents of the package are described below.

- "application": 
    - "x_linux_spn1": This folder contains sources for the API and UI App
        - "pictures": All the picture and icon resources required by the UI App are present in this folder
        - "ihm12_api.py" & "ihm15_api.py": These files implements the API used to control the respective motor drivers
        - "spn1_ui.py": Contains GTK-based UI application’s source code
        - "spn1_ui.glade": This file is generated by "Glade" tool and contains widgets configuration used in UI App
        - "spn1_ui.css": Contains visual styles used by the widgets in UI App
    - "080-x-linux-spn1.yaml": This file adds a menu entry to the default demo application that comes with the STM32MP1 evaluation/discovery boards
    - "deploy.sh": This is the deployment script used to deploy files from the host computer to the MPU board. It copies the files to the correct location in the MPU filesystem, such that the demo launcher recognizes and loads the new application at startup 

## Hardware Setup:

The current package provides software support for the following boards
 - [X-NUCLEO-IHM15A1 board](https://www.st.com/en/ecosystems/x-nucleo-ihm15a1.html) based on STSPIN840 driver. 
    [STSPIN840](https://www.st.com/en/motor-drivers/stspin840.html) is an affordable and easy-to-use solution for the implementation of compact motor driving applications such as thermal printers, robotics, and toys. It also supports parallel operation, where it acts as a single brush DC driver with double the current capability. The current limiters and complete set of protection features make it suitable for reliable applications.
 - [X-NUCLEO-IHM12A1 board](https://www.st.com/en/ecosystems/x-nucleo-ihm12a1.html) based on STSPIN240 driver. 
    [STSPIN240](https://www.st.com/en/motor-drivers/stspin240.html) can control two brushed DC motors at the same time. It comes in a very small 4x4 QFN package and a low resistance power stage. It can also work in parallel mode as a single full-bridge driver with higher current capability. It has two PWM current controllers that can be set by the user. It has a low power mode and several protections for the power stage. It is suitable for demanding industrial applications.


![X-NUCLEO-IHM15A1 Board](/_htmresc/05_hw_setup_ihm15a1.png "X-NUCLEO-IHM15A1")

![X-NUCLEO-IHM12A1 Board](/_htmresc/05_hw_setup_ihm12a1.png "X-NUCLEO-IHM12A1")

The board plugs into the Arduino connectors available at the back side of the STM32MP157F-DK2 discovery boards, as shown below.  
 
![X-NUCLEO-IHM15A1 mounted on STM32MP157F-DK2](/_htmresc/06_x-nucleo-ihm15a1_stm32mp157f-dk2.png "X-NUCLEO-IHM15A1 on STM32MP157F-DK2")

## Software Setup:

The section describes the software setup that is required for building, flashing, deploying, and running the application.

### Recommended PC prerequisites

A Linux® PC running Ubuntu® 20.04 or 22.04 is recommended. Developers can follow the link below for details.
https://wiki.st.com/stm32mpu/wiki/PC_prerequisites

Follow the instructions on the ST wiki page [Image flashing](https://wiki.st.com/stm32mpu/wiki/STM32MP15_Discovery_kits_-_Starter_Package#Image_flashing) to prepare a bootable SD card with the starter package.  
Alternatively, a Windows / Mac computer can also be used; in that case, the following tools would be useful:
- Use [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) to flash the OpenSTLinux started package image onto the SD card
- Use [TeraTerm](https://github.com/TeraTermProject/osdn-download/releases/) or [PuTTY](https://putty.org/) to access the console interface via USB
- Use [winscp](https://winscp.net/eng/index.php) to copy the application to the MPU board

*The following conventions are used when referring to the code instructions.*
```
#Comments: Comment describing steps
PC>$ : Development or Host PC/machine command prompt. Text after $ is a command
Board>$ : STM32MP1 command prompt. Text after $ is a command
```
**STMPU Software Prerequisites**

The Python package ["gpiod"](https://github.com/hhk7734/python3-gpiod) is a prerequisite for the x-linux-spn1 software and must be installed onto the STM32MP1 board.

```bash
#Install Python pip if not already installed
Board>$ apt-get install python3-pip
#Install gpiod
Board>$ python3 -m pip install gpiod==1.5.4
```

### Deploying the files to the MPU board

It is required to transfer the built binaries, Python scripts, and application resources to the STM32MP board from the development PC.

The resources can be transferred via any of the following methods:

1. **Using a network connection**

Refer to [How to Transfer a File Over a Network](https://wiki.st.com/stm32mpu/wiki/How_to_transfer_a_file_over_network)
 
To connect the MPU board to a network, you may connect it to a wired network via the Ethernet jack on the MPU board.  
 
**OR**  

To connect to a WLAN, refer to [How to Setup a WLAN Connection"](https://wiki.st.com/stm32mpu/wiki/How_to_setup_a_WLAN_connection)

2. **Using a serial protocol** (like zmodem from Teraterm or kermit)

For Linux hosts refer to [How to transfer a file over a serial console](https://wiki.st.com/stm32mpu/wiki/How_to_transfer_a_file_over_serial_console)  
For Windows hosts, refer to
[How to transfer files to Discovery kit using Tera Term](https://wiki.st.com/stm32mpu/wiki/How_to_transfer_files_to_Discovery_kit_using_Tera_Term_on_Windows_PC)

To evaluate the X-LINUX-SPN1 package quickly, developers may copy the contents of the "application" folder contained in the package to `/usr/local/demo/application` folder on the STM32MP board using any of the above methods.
To ease this action, the deployment script present inside the "application" folder of X-LINUX-SPN1 package could be used (but only if using a network connection).

```bash
# Go to the application folder
PC>$ cd application
# Add execute permission to the deployment script
PC>$ chmod +x deploy.sh
# Run the deployment script
PC>$ ./deploy.sh <ip address of MPU board>
```

After the files have been copied to the MPU board, reboot the board. After reboot, the demo menu would have an option added for X-LINUX-SPN1 as shown below.

![X-LINUX-SPN1 Icon](/_htmresc/07_x-linux-spn1_icon_image.png "X-LINUX-SPN1 Launch Icon")

- **Using the GTK Application**: On opening the application, the user is presented with the option to select the motor driver board to be used. The interface is depicted below.

![X-LINUX-SPN1 Interface](/_htmresc/08_x-linux-spn1_home_screen.png "X-LINUX-SPN1 GTK Application Interface")

The application interface is simple with a start/stop button and four direction buttons. The application is designed for 2 channels that are controlling the 2 motors mounted on left and right sides of a toy car. On tapping the *On/Off* button, both motors would start moving in the forward direction. On clicking the *back* button, both motors start moving in the reverse direction. On tapping the *left* and *right* buttons, both motors move in opposite directions to make the car turn left or right as per the user's action. The interface is depicted below.

![X-LINUX-SPN1 Interface](/_htmresc/09_x-linux-spn1_control_screen.png "X-LINUX-SPN1 GTK Application Interface")

## License

Details about the terms under which various components are licensed are available [here](LICENSE.md)

## Release notes

Details about the content of this release are available in the release note [here](Release_Notes.md).

## Compatibility information

The software package is validated for the [OpenSTLinux](https://www.st.com/en/embedded-software/stm32-mpu-openstlinux-distribution.html) version 5.0. For running the software on other ecosystem versions customization may be needed.
The software is tested on the [STM32MP157F-DK2](https://www.st.com/en/evaluation-tools/stm32mp157f-dk2.html) board.
**Note**: The STM32MP135 series discovery boards do not have an Arduino connector required for the X-NUCLEO-IHMxx boards.

#### Related Information and Documentation:

- [X-STM32MP-MSP01](https://www.st.com/en/evaluation-tools/x-stm32mp-msp01.html)
- [STM32MP157F-DK2](https://www.st.com/en/evaluation-tools/stm32mp157f-dk2.html)
- [X-NUCLEO-IHM15A1](https://www.st.com/en/ecosystems/x-nucleo-ihm15a1.html)
- [STSPIN840](https://www.st.com/en/motor-drivers/stspin840.html)
- [X-NUCLEO-IHM12A1](https://www.st.com/en/ecosystems/x-nucleo-ihm12a1.html)
- [STSPIN240](https://www.st.com/en/motor-drivers/stspin240.html)
