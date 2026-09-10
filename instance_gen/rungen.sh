#!/bin/bash

for i in {1..5}
do
    python3 generator.py f$1.txt ../rand_f$1_$i.txt
done

