#!/usr/bin/env bash


cat ./tmp/* | python ../mapper.py | sort | python ../reducer.py

