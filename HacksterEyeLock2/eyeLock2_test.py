from flask import Flask 
from flask_ask import Ask,  request, session, statement, question
from random import randint
import serial 
from recognition_tutorial import initialization, recognize

app = Flask(__name__) 
ask = Ask(app, '/') 

isDoorOpen = 0

#start of Alexa handler
@ask.launch
def launch():	
	return question("Welcome, this is eye lock!")

@ask.intent("testLightOn") 
def testLightOn(): 
	return question("Test light turned on!") 

@ask.intent("testLightOff") 
def testLightOff(): 
	return question("Test light turned off!") 

@ask.intent("getOutdoorCondition") 
def getOutdoorCondition():
	returnStatement = "Here is information about the weather outside."

	return statement(returnStatement)

@ask.intent("checkTemp")
def checkTemp():
	returnStatement = "The temperature is " 
	return statement(returnStatement)

@ask.intent("checkHumid")
def checkHumid():
	returnStatement = "The relative humidity is "
	return statement(returnStatement)

@ask.intent("doorUnlock") 
def doorUnlock():
	global isDoorOpen
	if (isDoorOpen == 1):
		return statement("The door is already open!")
	
	return question("Sorry, your face is not recognized, would you like to try again?")

@ask.intent("doorLock") 
def doorLock():
	global isDoorOpen
	if (isDoorOpen == 1):
		isDoorOpen = 0
		
	return statement("Door has been locked")

if __name__ == "__main__":
	app.run(debug=True) 


