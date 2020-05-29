#!/bin/bash

echo "Running jupyter!!"
jupyter notebook --VoilaConfiguration.file_whitelist="['.*\.(png|jpg|gif|svg|mp4|avi|ogg|ttf)']"