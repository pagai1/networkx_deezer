#!/bin/bash
echo "Berechnungen,Knoten,Kanten,Zeit_NetworkX"
#for lines in 25000 50000 75000 100000 125000 150000 175000 200000 225000 250000 275000 300000 325000 350000 375000 400000 425000 450000 475000 500000 525000 550000 575000 600000 625000 650000 675000 700000 725000 750000 775000 800000 825000 850000 875000 900000 925000 950000 975000 1000000; do
#for lines in 25000 50000 75000 100000 125000 150000 175000 200000 225000 250000 275000 300000 325000 350000 375000 400000 425000 450000 475000 500000 ;do
for lines in 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 2600 2700 2800 2900 3000 3100 3200 3300 3400 3500 3600 3700 3800 3900 4000 4100 4200 4300 4400 4500 4600 4700 4800 4900 5000; do
	/home/pagai/eclipse-workspace/networkx_deezer/eclipse-python-networkx-deezer.py ${lines} $1 $2
done
