#!/usr/bin/env bash

cd ~/Codes/dank/forecast-server
git log --format='%ae;%aD' > ./tmp/project-a.log
cd -

cd ~/Codes/dank/danke-spiders
git log --format='%ae;%aD' > ./tmp/project-b.log
cd -

