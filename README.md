# RaspiHome
Asistente de voz realizado en python3 basado en una placa ARM Raspberry Pi 3

Este pequeño asistente de voz, nace a traves de la necesidad de poder adaptar distintos dispositivos para su funcionamiento por reconocimiento de voz, aunque principalmente inicio como un timer que encendia mis luces a cierta hora y las apaga despues, creo que se ha desarrollado muy bien para poder utilizarlo en placas de desarrollo como la Raspberry Pi.
Considero que este proyecto es capaz de correr en cualquier versión de dicha tarjeta aunque solo ha sido probada el la RPi 3b, Utiliza el reconocimiento de voz por parte de Google con una licencia para pruebas (no comercial) que es el principal motor que lo impulsa, a traves de un microfono (recomiento USB ya que se puede fabricar uno con entradas en los pines del GPIO pero no da el mismo rendimiento) procesa la voz en el lenguaje seleccionado (Ingles/Español) y ejecuta el comando según este escrito en el codigo.
Funciona hilos para realizar sus tareas, ademas que tiene la capacidad de poder recibir comandos a traves de sockets para ejecutarse de la misma forma que si se reconociera por voz (Esto es por que se trabaja en una aplicación para dispositivos moviles la cual pueda darle mas funcionalidad).
Aunque su uso es recomendable en raspberry Pi u otra tarjeta de desarrollo NO es forzoso utilizarlo en otros sistemas, puede funcionar en cualquier sistema linux de cualquier plataforma que tenga Python3, Pip3.

Para poder funcionar correctamente se deben instalar lo siguiente:

sudo apt-get install portaudio19-dev<br>
sudo apt-get install mpg321<br>
sudo apt install python3-pip<br>
sudo apt-get install flac<br>
sudo pip3 install SpeechRecognition<br>
sudo pip3 install pyaudio<br>
sudo pip3 install gTTS<br>

