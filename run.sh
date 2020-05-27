#!/bin/bash

echo "Preprocessing data"
python ./scripts/preprocess.py

echo "Running voila!!"
voila --port=8000 --no-browser --enable_nbextensions=True 06_GUI.ipynb