# RaspiHome
Asistente de voz realizado en python3 basado en una placa ARM Raspberry Pi 3

# Instalación
La instalación se realiza en una placa de desarrollo Raspberry pi con sistema basado en debian "Raspbian", basta con descargar y ejecutar el archivo install_asistente.sh con permisos de root. (No es necesario usar antes apt update/upgrade).

```
sudo install_asistente.sh
```

Despues de esto se debera editar el archivo main.py con su editor de texto favorito, para cambiar el nombre del microfono por el de su equipo y otras configuraciones que requiera o crea pertinentes.

# Detalles
Se puede instalar en cualquier distro de linux, se tiene que quitar del main.py las menciones del archivo raspberry.py

Este pequeño asistente de voz, nace a traves de la necesidad de poder impresionar a la chica que me gusta, y tambien para adaptar distintos dispositivos para su funcionamiento por reconocimiento de voz, como reles principalemte para poder activar/desactivar electrodomesticos, aunque principalmente inicio como un timer que encendia mis luces a cierta hora y las apaga despues, creo que se ha desarrollado muy bien para poder utilizarlo en placas de desarrollo como la Raspberry Pi.<br><br>
Considero que este proyecto es capaz de correr en cualquier versión de dicha tarjeta aunque solo ha sido probada el la RPi 3b, Utiliza el reconocimiento de voz por parte de Google con una licencia para pruebas (no comercial) que es el principal motor que lo impulsa, a traves de un microfono (recomiento USB ya que se puede fabricar uno con entradas en los pines del GPIO pero no da el mismo rendimiento) procesa la voz en el lenguaje seleccionado (Ingles/Español) y ejecuta el comando según este escrito en el codigo.<br><br>
Funciona hilos para realizar sus tareas, ademas que tiene la capacidad de poder recibir comandos a traves de sockets para ejecutarse de la misma forma que si se reconociera por voz (Esto es por que se trabaja en una aplicación para dispositivos moviles la cual pueda darle mas funcionalidad).<br><br>
Aunque su uso es recomendable en raspberry Pi u otra tarjeta de desarrollo NO es forzoso utilizarlo en estos sistemas, puede funcionar en cualquier sistema linux de cualquier plataforma que tenga Python3, Pip3.<br><br>
