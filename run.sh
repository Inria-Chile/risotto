#!/bin/bash

if [ `ls -l datasets | wc -l` = 0 ]
then
    echo "Datatsets folder not found. Downloading datasets and building artifacts. You may go for a coffee, this will take some time..."
    python ./scripts/download.py
fi

echo "Running voila!!"
voila --port=8000 --no-browser --enable_nbextensions=True 06_GUI.ipynb