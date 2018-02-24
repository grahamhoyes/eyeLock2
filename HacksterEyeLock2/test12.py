from flask import Flask 
from flask_ask import Ask,  request, session, statement, question
from random import randint
import serial 
from recognition_tutorial import initialization, recognize

app = Flask(__name__) 
ask = Ask (app, '/') 
	
initialization();

@ask.launch
def launch():
	return question("Welcome to Eye Lock!")
	
@ask.intent("test") 
def doorUnlock():
	if (recognize() == "s1"): 
		return statement("The door has been unlocked and opened")
	
	return question("Sorry, your face is not recognized, please try again.")

if __name__ == "__main__":
	app.run(debug=True) 


