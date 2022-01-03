#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################
# Title		:	Hamster trading
# Version	:	1.0
# Date 		:	Oct 2021
# Roni Bandini - @RoniBandini
##############################################

from gpiozero import MotionSensor
from datetime import datetime
from RPi import GPIO
from time import sleep

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import alpaca_trade_api as tradeapi

import datetime
from time import sleep
import time
import random
import string

clk = 17
dt = 18
pir = MotionSensor(14)

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

# Oled screen
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
font = ImageFont.load_default()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0

pirStarted = 0

# Alpaca authentication and connection details
api_key = ''
api_secret = ''
base_url = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

currentTrade="Buy"
stockSelected="False"
lastTickerTraded=""
numberOfStocks=10
pauseBetweenOrders=5

# logo
image = Image.open('/home/pi/alpaca/logorat.png').convert('1')
disp.image(image)
disp.display()
time.sleep(3)

image = Image.open('/home/pi/alpaca/wait.png').convert('1')
disp.image(image)
disp.display()

################################################################################

def generateOrder():
	# generate order number
	letters = string.ascii_uppercase
	myOrder= ''.join(random.choice(letters) for i in range(15))
	return myOrder

def checkOpenOrders(myOrder):
	print("Checking open orders...")

	# Check if last order was filled

	try:
		myAnswer=api.get_order_by_client_order_id(myOrder).status

		if (myAnswer!='filled'):
			print('Last order was not filled :(')
			return 0
		else:
			print('Filled :)')
			return 1


	except Exception as myError:
		print("> "+str(myError))
################################################################################

now = datetime.datetime.now()

# Argentine stock tickers

myTickers = ["MELI", "TS", "GLOB"]

print('------------------------------------------------')
print('Hamster trading')
print('Roni Bandini - 12-2021 - Buenos Aires, Argentina')

print("Started " + str( now.strftime("%Y-%m-%d %H:%M:%S")) )

# query Alpaca API
account = api.get_account()
print("Equity: "+str(account.equity))

# Display
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
now = datetime.datetime.now()
draw.text((x, top),       str( now.strftime("%Y-%m-%d %H:%M:%S")),  font=font, fill=255)
draw.text((x, top+8),     "Started", font=font, fill=255)
draw.text((x, top+16),    "Action: "+currentTrade,  font=font, fill=255)
draw.text((x, top+25),    "Equity: $"+str(account.equity),  font=font, fill=255)
disp.image(image)
disp.display()

#check if market is open
clock = api.get_clock()

if clock.is_open:
	print('Market is open :)')
else:
    print('Market is closed :(')
    #quit()

try:

	while True:


			if pir.motion_detected:

				print("*** Trading")

				orderId=generateOrder()

				if currentTrade=="Buy":

					if stockSelected=="True":

						stockSelected="False"

						myTicker=myTickers[counter]
						lastTickerTraded=myTicker

						print("Sending Buy order for "+myTicker)
						try:
							api.submit_order(symbol=myTicker,
								qty=numberOfStocks,
								side='buy',
								time_in_force='gtc',
								type='market',
								client_order_id=orderId)

						except Exception as myError:
							print("Exception in buy order "+str(myError))
							quit()

						currentTrade="Sell"

						time.sleep(pauseBetweenOrders)

						# wait until order is not pending
						while checkOpenOrders(orderId)==0:
							time.sleep(10)




				else:

					print("Sending sell order for "+lastTickerTraded)

					try:
						api.submit_order(symbol=lastTickerTraded,
							qty=numberOfStocks,
							side='sell',
							time_in_force='gtc',
							type='market',
							client_order_id=orderId)

					except Exception as myError:
						print("Exception in sell order "+str(myError))
						quit()

					currentTrade="Buy"
					stockSelected="False"

					image = Image.new('1', (width, height))
					draw = ImageDraw.Draw(image)
					draw.rectangle((0,0,width,height), outline=0, fill=0)
					padding = -2
					top = padding
					bottom = height-padding
					x = 0
					now = datetime.datetime.now()
					draw.text((x, top),       str( now.strftime("%Y-%m-%d %H:%M:%S")),  font=font, fill=255)
					draw.text((x, top+8),     "Waiting to execute", font=font, fill=255)
					draw.text((x, top+16),    "Last Ticker: "+str(myTickers[counter]),  font=font, fill=255)
					draw.text((x, top+25),    "Equity: $"+str(account.equity),  font=font, fill=255)
					disp.image(image)
					disp.display()

					time.sleep(pauseBetweenOrders)

					# wait until order is not pending
					while checkOpenOrders(orderId)==0:
						time.sleep(10)

				# Display
				image = Image.new('1', (width, height))
				draw = ImageDraw.Draw(image)
				draw.rectangle((0,0,width,height), outline=0, fill=0)
				padding = -2
				top = padding
				bottom = height-padding
				x = 0
				now = datetime.datetime.now()
				draw.text((x, top),       str( now.strftime("%Y-%m-%d %H:%M:%S")),  font=font, fill=255)
				draw.text((x, top+8),     currentTrade, font=font, fill=255)

				if currentTrade=="Buy":
					draw.text((x, top+16),    "Bought: "+str(myTickers[counter]),  font=font, fill=255)
				else:
					draw.text((x, top+16),    "Sold: "+lastTickerTraded,  font=font, fill=255)

				draw.text((x, top+25),    "Equity: $"+str(account.equity),  font=font, fill=255)
				disp.image(image)
				disp.display()

				pir.wait_for_no_motion()

			else:

				clkState = GPIO.input(clk)
				dtState = GPIO.input(dt)

				if clkState != clkLastState:

						stockSelected="True"

						if dtState != clkState:
								counter += 1
						else:
								counter -= 1

						if counter<0:
								counter	=	2
						if counter>2:
								counter	=	0

						print("Ticker:"+str(myTickers[counter]))						

						clkLastState = clkState

						#sleep(0.01)

				sleep(0.01)



finally:
        GPIO.cleanup()
