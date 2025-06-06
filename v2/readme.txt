# Wall Street Hamster

Complete tutorial at https://hackaday.io/project/203244-wall-street-hamster

# Requirements

Raspberry Pi (2 or 3 will do it)https://www.dfrobot.com/product-2028.html?tracking=61357a929f73e
Rotary Encoder https://amzn.to/3FIgLZ5
Oled screen https://www.dfrobot.com/product-1514.html?tracking=61357a929f73e
PIR sensor https://www.dfrobot.com/product-119.html?tracking=61357a929f73e
3d printed parts https://cults3d.com/en/3d-model/gadget/hamster-trading

# Software

Setup the Raspberry Pi with Raspberry Pi OS (download Windows, Mac or Linux software from https://www.raspberrypi.org/downloads to copy the image into the microSD card)

Connect a keyboard and HDMI screen to setup the Raspberry. 

Connect the PIR, Oled and Rotary using jumper cables.

Oled
SDA, white to GPIO2
SCL to GPIO3
+ to 5V
- to GND

PIR
+ - 5v
GND - GND (pin6)
GPIO14, to PIR signal

Rotary Encoder
CLK - GPIO17 (pin11)
DT - GPIO18 (pin12)
+ - 3v3 (pin1)
GND - GND (pin6)

Start the Raspberry Pi.

Install Alpaca trading libraries

$ sudo pip3 install alpaca-trade-api
$ sudo apt-get install libatlas-base-dev

Sign up at alpaca trading https://app.alpaca.markets/signup
Login and get your API keys (public and secret)

Enable SSH

$ sudo raspi-config 

Use the arrows on your keyboard to select Interfacing Options.
Select the P2 SSH option on the list.
Select <Yes> on the “Would you like the SSH server to be enabled?” prompt.
Now go to Network Options, Wifi and specify your WiFi credentials.

Exit. Now you can disconnect the keyboard and the screen and connect remotely to your Raspberry with Putty or any other terminal.

Upload all project files to root/alpaca folder. You can use any FTP client with the same SSH credentials.

$ nano wallstreethamster.py and enter your own Alpaca credentials

api_key = ''
api_secret = ''
base_url = ''

Download and print the 3d parts.

Connect the wheel to the Rotary encoder and the PIR to the support base. Connect PIR to the Buy/Sell house.

Execute 
$ cd alpaca
$ sudo python3 wallstreethamster.py

