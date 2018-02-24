#include <SimpleDHT.h>


/* ==========================================================
eyeLock

By: Steve Kim, Graham Hoyes, Kevin Zhang
==============================================================
*/

// Setting pin assignments

#define led 2
#define photoPin 1
#define moisturePin 0
#define tempHumidPin 7
#define stepPin 9
#define dirPin 8
#define enable 13

//const int stepPin = 9;
//const int dirPin = 8;
//const int enable = 13;

char cmd = 'Z';

int minLight; // Used to calibrate the readings for brightness
int maxLight;
int lightLevel;
int normalizedLightLevel;

int minMoisture; // Used to calibrate the readings for moisture levels
int maxMoisture;
int moistureLevel;
int normalizedMoistureLevel;

SimpleDHT11 dht11; 

void setup() {
 Serial.begin(9600);
 
 pinMode(led, OUTPUT);
 pinMode(stepPin,OUTPUT);
 pinMode(enable,OUTPUT);
 
 // Setup the starting light level limits
 lightLevel = analogRead(photoPin);
 minLight = lightLevel-20;
 maxLight = lightLevel;

 
 // Setup the starting moisture level limits
 moistureLevel = analogRead(moisturePin);
 minMoisture = moistureLevel-20;
 maxMoisture= moistureLevel;
 
 //Turn off motor initially 
 digitalWrite(enable,HIGH);
 
}

void loop() { 
  cmd = 'Z';
  
  if (Serial.available() > 0){
    cmd = Serial.read();
  }
  
  if (cmd == 'O') { 
    digitalWrite(led, HIGH);
  }
  else if(cmd == 'X') {
    digitalWrite(led, LOW);
  } 
  else if(cmd == 'A') {
    /*Start of soil moisture sensor code*/
    moistureLevel = analogRead(moisturePin);
    
    if(minMoisture >  moistureLevel){
      minMoisture =  moistureLevel;
    }
    if(maxMoisture < lightLevel){
      maxMoisture = lightLevel;
    }
    
    //Adjust the light level for a normalized result b/w 0 and 100.
    normalizedMoistureLevel = map(moistureLevel, minMoisture, maxMoisture, 100, 0);
    
    /*Start of photocell code*/
    //auto-adjust the minimum and maximum limits in real time
    lightLevel = analogRead(photoPin);
    
    if(minLight > lightLevel){
      minLight = lightLevel;
    }
    if(maxLight < lightLevel){
      maxLight = lightLevel;
    }

    //Adjust the light level for a normalized result b/w 0 and 100.
    normalizedLightLevel = map(lightLevel, minLight, maxLight, 100, 0);

    /*Start of temp and humidity sensor code*/
    byte temperature = 0;
    byte humidity = 0;
    dht11.read(tempHumidPin, &temperature, &humidity, NULL);
    
    /*Printing results to serial*/
    Serial.println(normalizedMoistureLevel);
    Serial.println(normalizedLightLevel);
    Serial.println(int(temperature));
    Serial.println(int(humidity));
  }
  else if(cmd == 'T') {
    /*Start of temp and humidity sensor code*/
    byte temperature = 0;
    byte humidity = 0;
    dht11.read(tempHumidPin, &temperature, &humidity, NULL);
    
    Serial.println(int(temperature));  
  }
  else if(cmd == 'H') {
    byte temperature = 0;
    byte humidity = 0;
    dht11.read(tempHumidPin, &temperature, &humidity, NULL);
    
    Serial.println(int(humidity));
  }
  else if(cmd == 'o') { 
    digitalWrite(enable,LOW);
    
    Serial.println("opening");

    digitalWrite(dirPin,HIGH);
    for(int x = 0; x < 7000; x++) {
      digitalWrite(stepPin,HIGH);   
      delayMicroseconds(1200); 
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(1200); 
    }
    digitalWrite(enable,HIGH);
  }
  else if(cmd == 'c') {
    digitalWrite(enable,LOW);
    
    Serial.println("closing");
    
    digitalWrite(dirPin,LOW); 
    for(int x = 0; x < 7000; x++) {
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(1200);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(1200);
    }  
    digitalWrite(enable,HIGH);
  
  }
  delay(50);
}
