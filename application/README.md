## Integrating X-LINUX-SPN1 into OpenSTLinux demo-launcher

The OpenSTLinux starter package includes a demo-launcher application that provides easy access to various demo applications, such as video playback and AI demos. This guide will help you integrate the X-LINUX-SPN1 package into the demo-launcher.

### Steps to Integrate

1. **Copy Files Manually**:
    - Copy the contents of the `demo-launcher` folder from this package to the `/usr/local/demo/application/` directory on your MPU board.
    - On the next startup, the X-LINUX-SPN1 icon will appear in the demo-launcher, enabling easy access to the application.

2. **Using the Deployment Script**:
    - Run the `deploy.sh` script located in the `scripts` folder at the root of this package. This script automates the integration process.
    
    ```sh
    cd scripts
    ./deploy.sh
    ```

### Additional Information

For more detailed instructions on integrating applications into the OpenSTLinux demo-launcher, please refer to the [stm32mp wiki page](https://wiki.st.com/stm32mpu/wiki/GTK_demo_launcher).
