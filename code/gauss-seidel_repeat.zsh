#!/bin/zsh

counter=1
while [[ $counter -le 20 ]]; do
    python laplace.py gauss-seidel -b plane -x 32 -y 32
    (( counter++ ))
done
