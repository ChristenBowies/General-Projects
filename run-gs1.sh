#!/bin/bash

for i in 1000 1000  1500 1500 2000 2000 2500 2500 3000 3000 3500 3500 4000 5000
do
    echo `./gs1.py "$i"` >> data.txt
done

echo `gnuplot model.gpt`
