#!/bin/sh
apt update
apt upgrade -y
apt install portaudio19-dev -y
apt install mpg321 -y
apt install flac -y
apt install python3 -y
apt install python3-pip -y
apt install git -y
pip3 install SpeechRecognition
pip3 install pyaudio
pip3 install gTTS

git clone https://github.com/ShinyDavid/RaspiHome.git
chmod -R 755 "RaspiHome"
cd RaspiHome
chmod o+x main.py
echo "Listo, instalación realizada"
echo "Ejecutese con: python3 main.py"
