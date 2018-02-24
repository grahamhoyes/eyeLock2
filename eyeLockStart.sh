#!/bin/bash

BASEDIR=/home/pi/Desktop/eyeLock2
SUBDOMAIN=eyelock # For use with custom ngrok subdomains
echo "Starting"
echo "----------$(date)----------" >> ${BASEDIR}HacksterEyeLock2/pythonlogs.log
echo "----------$(date)----------" >> ${BASEDIR}HacksterEyeLock2/mavenlogs.log
npm start --prefix ${BASEDIR}alexa-avs-sample-app/samples/companionService --cwd ${BASEDIR}alexa-avs-sample-app/samples/companionService &
(sleep 10; sudo mvn -f ${BASEDIR}alexa-avs-sample-app/samples/javaclient exec:exec) &
(sleep 25; cd ${BASEDIR}alexa-avs-sample-app/samples/wakeWordAgent/src; ./wakeWordAgent -e sensory) & 
(cd ${BASEDIR}HacksterEyeLock2; python eyeLock2.py) &
# Omit the -subdomain flag and "> /dev/null" to output ngrok url for Alexa endpoint if not using a custom subdomain
(${BASEDIR}ngrok http -subdomain=${SUBDOMAIN} 5000 > /dev/null)
echo "Up and running!"
