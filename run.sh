#!/bin/bash

echo "Preprocessing data"
python ./scripts/preprocess.py

echo "Running voila!!"
voila --port=80 --no-browser --enable_nbextensions=True 06_GUI.ipynb --VoilaConfiguration.file_whitelist="['.*\.(png|jpg|gif|svg|mp4|avi|ogg|ttf)']"