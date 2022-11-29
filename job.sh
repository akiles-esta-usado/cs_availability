#!/bin/sh
python 	/home/pi/proyecto/capturar_foto.py;
cd darknet;
./darknet detect cfg/yolov3.cfg yolov3.weights /home/pi/proyecto/fotos_autos/image.jpg > /home/pi/proyecto/output.txt;
cat /home/pi/proyecto/output.txt | grep car | wc -l  > /home/pi/proyecto/resultado.txt;
cd ..;
python /home/pi/proyecto/api.py;
