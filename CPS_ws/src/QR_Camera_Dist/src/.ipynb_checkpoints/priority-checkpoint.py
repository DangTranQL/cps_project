#!/usr/bin/env python3

from queue import PriorityQueue
import csv

q = PriorityQueue()

f= open('/home/jetson/CPS_ws/src/QR_Camera_Dist/src/data.csv', 'r')
rows = csv.reader(f)
for row in rows:
    q.put((int(row[0]),(float(row[1]),float(row[2])),(float(row[3]),float(row[4]),float(row[5]),float(row[6]))))
    f.close()
