# WinSAT KubOS Flight Software
This repository contains the flight software prototype for the WinSAT-1 Cubesat as part of the CSDC 5 competition. [CSDC](https://www.csdcms.ca/)

More information about the WinSAT CubeSat satellite and team can be found on the team website. [WinSAT](https://www.winsat.ca/)

The flight software utilizes the KubOS satellite software framework. [KubOS](https://www.kubos.com/)

## Overview

<img src="/images/arch.png" width="400"/> <img src="/images/software.png" width="400"/>

The flight software runs on the main Onboard Computer (OBC) and interfaces will all of other major subsystems onboard the satellite:

* Attitude Determination and Control (ADCS)
* Electrical Power System (EPS)
* Radio Frequency (RF)
* Payload

Mission applications, services, and hardware APIs are provided here that interface with all of these major subsystems as well as add other functionality such as telemetry handling and scheduling.

Testing has been done with one of the KubOS compatible computers, the Beaglebone Black, with COTS replacements (Adafruit, RPi, Sparkfun, etc...) for most of the onboard subsytems.