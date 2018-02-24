from flask import Flask 
from flask_ask import Ask,  request, session, statement, question
from random import randint
import serial 
from recognition_tutorial import initialization, recognize

arduinoSerial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
app = Flask(__name__) 
ask = Ask(app, '/') 

isDoorOpen = 0
initialization();

#start of Alexa handler
@ask.launch
def launch():	
	return question("Welcome, this is eye lock!")

@ask.intent("testLightOn") 
def testLightOn(): 
	arduinoSerial.write(b'O') 
	return question("Test light turned on!") 

@ask.intent("testLightOff") 
def testLightOff(): 
	arduinoSerial.write(b'X') 
	return question("Test light turned off!") 

@ask.intent("getOutdoorCondition") 
def getOutdoorCondition():
	arduinoSerial.write(b'A')
	soilMoisture = arduinoSerial.readline()
	sunLight = arduinoSerial.readline()
	temperature = arduinoSerial.readline()
	humidity = arduinoSerial.readline()

	if (int(soilMoisture) < 15):
		soilMoisture = "dry. "
	elif (int(soilMoisture) < 25):
		soilMoisture = "fairly dry. "
	elif (int(soilMoisture) < 60):
		soilMoisture = "damp. "
	elif (int(soilMoisture) < 80):
		soilMoisture = "fairly wet. "
	else: soilMoisture = "flooded. "

	if (int(sunLight) < 10):
		sunLight = "It is pitch black, probably night time. "	
	elif (int(sunLight) < 25):
		sunLight = "There seems to be moonlight, it is probably night time. " 	
	elif (int(sunLight) < 50):
		sunLight = "It is cloudy, overcast skies. "	
	elif (int(sunLight) < 80):
		sunLight = "It is a nice day, but not excessively bright. "   	
	else: sunLight = "It is super bright. "

	returnStatement = "Here is information about the weather outside. The ground is " + soilMoisture + sunLight + "The temperature is " + str(float(temperature)) + " degrees Celsius. " + "And the relative humidity is " + str(float(humidity)) + " percent."

	return statement(returnStatement)

@ask.intent("checkTemp")
def checkTemp():
	arduinoSerial.write(b'T')
	temperature = arduinoSerial.readline()
	returnStatement = "The temperature is " + str(float(temperature)) + " degrees Celsius. "
	return statement(returnStatement)

@ask.intent("checkHumid")
def checkHumid():
	arduinoSerial.write(b'H')
	humidity = arduinoSerial.readline()
	returnStatement = "The relative humidity is " + str(float(humidity)) + " percent."
	return statement(returnStatement)

@ask.intent("doorUnlock") 
def doorUnlock():
	global isDoorOpen
	if (isDoorOpen == 1):
		return statement("The door is already open!")
	
	if (recognize() == "s1"): 
		arduinoSerial.write(b'o')
		isDoorOpen = 1
		return statement("The door has been unlocked and opened")
	
	return question("Sorry, your face is not recognized, would you like to try again?")

@ask.intent("doorLock") 
def doorLock():
	global isDoorOpen
	if (isDoorOpen == 1):
		isDoorOpen = 0
		
	return statement("Door has been locked")

if __name__ == "__main__":
	app.run(debug=True) 


