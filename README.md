# ph-monitor
This program talk to a `Knick Protavo 904` ph meter and `Hei_FLOW Precision 01` pumps. Depending on the hp value read from the ph meter, the pump flow is controlled. The program is capable of controlling
multiple pumps. This application will only work on Windows. 

## `Knick Protavo 904` ph meter setup
Download and install application called `Paraly SW 112` using [this](https://www.knick-international.com/en/products/portables/portavo/portavo-904/index.html) link.

This is how the application looks like
![alt text](images/ph_app.JPG)
Image of `Knick Protavo 904` ph meter 
![alt text](images/ph.jpg)

Connect `Knick Protavo 904` ph meter using micro-usb. Start the application `Paraly SW 112` and 
device should atomically connect. Click on the start button to start logging ph.
 
Note: this project is not maintained. If the link does not work, just google `Knick Protavo 904`.
## `Hei_FLOW Precision 01` pump setup
Computer talks to pump using RS232 connect. No Other set up required.

## Program Prerequisites for (our code)
### Install Anaconda
1. Download Anaconda from [here](https://www.anaconda.com/distribution/). Make sure to select Windows and Python <3.5.
2. Install Anaconda.
3. Start Command Prompt as administrator. It is important to start Command Prompt as administrator because 
, we need to install some python packages that requires permission fro windows.
4. Run the following commands in command prompt to create anaconda environment.
```buildoutcfg
conda create -n ph python=3.5
```  

where ph is the name of the environment
5. Enter environment
```buildoutcfg
conda activate ph
```
6. Run the following commands to install python packages.
```buildoutcfg
conda install -c conda-forge pyautogui pyperclip
conda install -c anaconda pyserial 
```

## Before running Program
Please follow the following steps before running the program.
1. Make sure `Paraly SW 112` is running and logging in the background
2. Make sure the log inveral and the `ph_read_interval` variable value inside the  inside the `configuration.json` file matches. 
`configuration.json` file is in the root directory of this project. You can add multiple COM ports if you have more pumps.
3. Pump is stopped (Not turned off).
4. Go inside Device Manager and under Ports(COM & LPT) you will find COM`X` (where `X` is a number) for the pump.
5. Put this COM`X` inside the `configuration.json` file.

## Running Program
The program can be run using an IDE like pycharm, but you will have to install pycharm and set the environment to 
ph (which we created earlier). Or you can run it on the termnial using the following command

```buildoutcfg
python3 Controller.py
```

When the program start it ask user to continue only when they are performed the steps on the screen. So please follow the steps.


Some to look for
1. When the `Paraly SW 112` is logging, the row are the same. You need to scroll to the bottom to see the new values.
2. Your COM port is not correct.
3. Google things if you do not understand. 
## How to make changes.
This program is very customized to specific need. The code is well coded and structured. It uses a observer design
pattern. Email me if you want to make changes. Me? well I am Muhammad Abdullah Sumbal.