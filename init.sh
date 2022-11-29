#!/bin/bash

conda env create -f environment.yml

sudo apt update
sudo apt install build-essential wget


if [ ! -d darknet ];
then
	git clone https://github.com/AlexeyAB/darknet
	cd darknet; make
	cd darknet; wget https://pjreddie.com/media/files/yolov3.weights
fi

